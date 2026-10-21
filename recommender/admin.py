from django.contrib import admin
from django.utils.html import format_html
from .models import (
    DietaryTag,
    IngredientPrice,
    Recipe,
    IngredientGroup,
    RecipeIngredient,
    InstructionStep
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ('item_name', 'quantity', 'ingredient_price', 'portion_cost_ghs', 'substitution_note', 'is_optional', 'order')


class IngredientGroupInline(admin.StackedInline):
    model = IngredientGroup
    extra = 1
    show_change_link = True


class InstructionStepInline(admin.TabularInline):
    model = InstructionStep
    extra = 1
    fields = ('step_number', 'heading', 'instruction', 'timer_minutes')


@admin.register(DietaryTag)
class DietaryTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(IngredientPrice)
class IngredientPriceAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'formatted_price', 'market_source', 'last_updated')
    list_editable = ('price_ghs',) if False else ()
    search_fields = ('name', 'market_source')
    list_filter = ('market_source',)

    def formatted_price(self, obj):
        return format_html('<strong style="color: #ea580c;">GH₵ {:.2f}</strong>', obj.price_ghs)
    formatted_price.short_description = "Market Price (GH₵)"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'twi_name',
        'formatted_cost',
        'total_time_minutes',
        'flavor_profile',
        'tradition_type',
        'difficulty',
        'is_active'
    )
    list_filter = ('tradition_type', 'flavor_profile', 'difficulty', 'is_active', 'dietary_tags')
    search_fields = ('title', 'twi_name', 'tagline', 'cultural_story')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('dietary_tags',)
    inlines = [InstructionStepInline, IngredientGroupInline]
    
    fieldsets = (
        ("Basic Information", {
            'fields': (
                'title',
                'slug',
                'twi_name',
                'tagline',
                'cultural_story',
                'hero_image_url',
                'is_active'
            )
        }),
        ("Cost & Budgeting (Ghana Cedis)", {
            'description': "Set the estimated cost per serving. You can enter a base cost or a manual street-price override.",
            'fields': (
                ('cost_per_serving_ghs', 'cost_override_ghs', 'default_servings'),
            )
        }),
        ("Timing & Effort", {
            'fields': (
                ('prep_time_minutes', 'cook_time_minutes', 'total_time_minutes'),
                ('difficulty', 'flavor_profile', 'tradition_type'),
            )
        }),
        ("Dietary & Categories", {
            'fields': ('dietary_tags',)
        }),
    )

    def formatted_cost(self, obj):
        return format_html(
            '<span style="background-color: #ffedd5; color: #c2410c; padding: 3px 8px; border-radius: 9999px; font-weight: 600;">GH₵ {:.2f}</span>',
            obj.effective_cost_per_serving
        )
    formatted_cost.short_description = "Cost / Serving"


@admin.register(IngredientGroup)
class IngredientGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'recipe', 'order')
    list_filter = ('recipe',)
    inlines = [RecipeIngredientInline]
