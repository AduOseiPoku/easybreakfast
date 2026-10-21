import uuid
from decimal import Decimal
from django.db import models
from django.utils.text import slugify


class DietaryTag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)
    icon = models.CharField(max_length=20, blank=True, help_text="e.g. 🌱, 🌾, 🐟")

    class Meta:
        ordering = ['name']
        verbose_name = 'Dietary Tag'
        verbose_name_plural = 'Dietary Tags'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.icon} {self.name}" if self.icon else self.name


class IngredientPrice(models.Model):
    name = models.CharField(max_length=120, unique=True)
    unit = models.CharField(max_length=50, help_text="e.g. piece, 1kg, 160g tin, cup")
    price_ghs = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        help_text="Standard market price in Ghana Cedis (GH₵)"
    )
    market_source = models.CharField(max_length=120, default="Accra / Makola Market Benchmark")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ingredient Market Price'
        verbose_name_plural = 'Ingredient Market Prices'

    def __str__(self):
        return f"{self.name} — GH₵ {self.price_ghs:.2f} per {self.unit}"


class Recipe(models.Model):
    class FlavorProfile(models.TextChoices):
        SWEET_WARM = 'SWEET_WARM', 'Warm & Sweet'
        SAVORY_SPICED = 'SAVORY_SPICED', 'Savory & Spiced'
        SWEET_SAVORY = 'SWEET_SAVORY', 'Sweet & Savory Combo'
        LIGHT_FRESH = 'LIGHT_FRESH', 'Light & Fresh'
        RICH_OPULENT = 'RICH_OPULENT', 'Rich & Opulent'

    class TraditionType(models.TextChoices):
        SANKOFA = 'SANKOFA', 'Sankofa (Traditional Ghanaian Heritage)'
        NEA_ONNIM = 'NEA_ONNIM', 'Nea Onnim (Modern Diaspora Twist)'

    class Difficulty(models.TextChoices):
        EASY = 'EASY', 'Easy & Quick'
        MEDIUM = 'MEDIUM', 'Medium'
        ADVANCED = 'ADVANCED', 'Weekend Project'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    twi_name = models.CharField(max_length=100, blank=True, help_text="Traditional Twi name if applicable")
    tagline = models.CharField(max_length=255, help_text="Vibrant one-line description")
    cultural_story = models.TextField(help_text="Chef Eric Adjepong's story and cultural note from Ghana to the World")
    
    prep_time_minutes = models.PositiveIntegerField(help_text="Prep time in minutes")
    cook_time_minutes = models.PositiveIntegerField(help_text="Cook time in minutes")
    total_time_minutes = models.PositiveIntegerField(help_text="Total elapsed time in minutes")
    default_servings = models.PositiveIntegerField(default=2)

    cost_per_serving_ghs = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Estimated base cost per serving in Ghana Cedis (GH₵)"
    )
    cost_override_ghs = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional manual override for serving cost in GH₵"
    )

    flavor_profile = models.CharField(
        max_length=20,
        choices=FlavorProfile.choices,
        default=FlavorProfile.SWEET_WARM
    )
    tradition_type = models.CharField(
        max_length=20,
        choices=TraditionType.choices,
        default=TraditionType.SANKOFA
    )
    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.EASY
    )
    
    dietary_tags = models.ManyToManyField(DietaryTag, blank=True, related_name='recipes')
    hero_image_url = models.URLField(blank=True, help_text="Image URL or placeholder asset")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['cost_per_serving_ghs', 'title']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.total_time_minutes:
            self.total_time_minutes = self.prep_time_minutes + self.cook_time_minutes
        super().save(*args, **kwargs)

    @property
    def effective_cost_per_serving(self) -> Decimal:
        if self.cost_override_ghs is not None and self.cost_override_ghs > 0:
            return self.cost_override_ghs
        return self.cost_per_serving_ghs

    def calculate_total_cost(self, servings: int = 1) -> Decimal:
        return self.effective_cost_per_serving * Decimal(servings)

    def __str__(self):
        return f"{self.title} (GH₵ {self.effective_cost_per_serving:.2f})"


class IngredientGroup(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient_groups')
    name = models.CharField(max_length=120, default="Ingredients", help_text="e.g. Porridge Base, Crumble, Hollandaise")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Ingredient Section'
        verbose_name_plural = 'Ingredient Sections'

    def __str__(self):
        return f"{self.recipe.title} → {self.name}"


class RecipeIngredient(models.Model):
    group = models.ForeignKey(IngredientGroup, on_delete=models.CASCADE, related_name='ingredients')
    item_name = models.CharField(max_length=150)
    quantity = models.CharField(max_length=80, help_text="e.g. 1 1/4 cups, 2 large, 1 tin")
    ingredient_price = models.ForeignKey(
        IngredientPrice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipe_usages',
        help_text="Optional link to market price item"
    )
    portion_cost_ghs = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Estimated portion cost in GH₵ for this recipe"
    )
    substitution_note = models.CharField(
        max_length=200,
        blank=True,
        help_text="e.g. Japanese eggplant if garden eggs unavailable"
    )
    is_optional = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipe Ingredients'

    def __str__(self):
        return f"{self.quantity} {self.item_name}"


class InstructionStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    heading = models.CharField(max_length=120, blank=True, help_text="e.g. Toast the Flours, Simmer & Thicken")
    instruction = models.TextField()
    timer_minutes = models.PositiveIntegerField(null=True, blank=True, help_text="Optional timer duration")

    class Meta:
        ordering = ['step_number']
        verbose_name = 'Instruction Step'
        verbose_name_plural = 'Instruction Steps'

    def __str__(self):
        return f"Step {self.step_number}: {self.heading or self.recipe.title}"
