from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from recommender.models import (
    DietaryTag,
    IngredientPrice,
    Recipe,
    IngredientGroup,
    RecipeIngredient,
    InstructionStep
)


class Command(BaseCommand):
    help = "Seeds all 40 authentic Ghanaian breakfast foods with realistic Ghana Cedis (GH₵) costs"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Dietary Tags..."))
        tags_data = [
            ("Vegetarian", "vegetarian", "🌱"),
            ("Vegan", "vegan", "🌿"),
            ("Gluten-Free", "gluten-free", "🌾"),
            ("Dairy-Free", "dairy-free", "🥛"),
            ("Pescatarian", "pescatarian", "🐟"),
            ("High-Protein", "high-protein", "⚡"),
            ("Quick & Easy", "quick-easy", "⏱️"),
        ]
        tags = {}
        for name, slug, icon in tags_data:
            tag, _ = DietaryTag.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'icon': icon}
            )
            tags[slug] = tag

        self.stdout.write(self.style.NOTICE("Seeding Ingredient Market Prices (Accra Benchmarks)..."))
        market_prices = [
            ("Corn flour", "1 kg", Decimal("20.00")),
            ("Peanut flour", "500g", Decimal("25.00")),
            ("Evaporated milk (Ideal tin)", "160g tin", Decimal("14.00")),
            ("Peanut butter (groundnut paste)", "medium jar", Decimal("30.00")),
            ("Plantains (ripe yellow)", "finger", Decimal("6.00")),
            ("Fresh ginger & garlic", "bundle", Decimal("10.00")),
            ("Eggs (fresh farm)", "piece", Decimal("3.50")),
            ("Sugar bread loaf", "large loaf", Decimal("18.00")),
            ("Tea bread loaf", "medium loaf", Decimal("10.00")),
            ("Butter bread loaf", "large loaf", Decimal("20.00")),
            ("Milo chocolate malt", "tin", Decimal("45.00")),
            ("Fonio grain", "500g bag", Decimal("40.00")),
            ("Coconut milk", "can", Decimal("25.00")),
            ("Black-eyed peas", "1 kg", Decimal("30.00")),
            ("Jasmine rice", "1 kg", Decimal("35.00")),
            ("Waakye leaves (sorghum)", "bunch", Decimal("8.00")),
            ("Cassava flour", "1 kg", Decimal("22.00")),
            ("Puna yam tuber", "medium tuber", Decimal("35.00")),
            ("Fermented corn dough", "1 kg", Decimal("15.00")),
            ("Millet grain", "1 kg", Decimal("25.00")),
            ("Hominy / Dried white corn", "1 kg", Decimal("22.00")),
            ("Tapioca pearls", "500g pack", Decimal("20.00")),
            ("Canned sardines in oil", "tin", Decimal("15.00")),
            ("Canned corned beef", "tin", Decimal("45.00")),
            ("Red palm oil (Zomi)", "1 bottle", Decimal("30.00")),
            ("Fresh garden eggs", "bundle", Decimal("15.00")),
            ("Kontomire (cocoyam leaves)", "bundle", Decimal("10.00")),
            ("Turkey tail (Chofi/Tsofi)", "pack", Decimal("35.00")),
            ("Fresh Wagashi cheese", "block", Decimal("25.00")),
            ("Tigernuts (fresh/dried)", "1 bowl", Decimal("20.00")),
            ("Grape-Nuts cereal", "box", Decimal("65.00")),
            ("Egusi melon seeds", "cup", Decimal("20.00")),
            ("Oats", "500g bag", Decimal("28.00")),
            ("Pink guavas / pulp", "500g", Decimal("35.00")),
            ("Butter (unsalted)", "250g block", Decimal("45.00")),
            ("White stone-ground grits", "500g bag", Decimal("40.00")),
            ("Fresh large prawns/shrimp", "500g", Decimal("95.00")),
            ("Sea scallops (U10)", "portion", Decimal("160.00")),
            ("Piri piri chilies / sauce", "jar", Decimal("25.00")),
        ]
        for name, unit, price in market_prices:
            IngredientPrice.objects.update_or_create(
                name=name,
                defaults={
                    'unit': unit,
                    'price_ghs': price,
                    'market_source': "Accra / Makola Market Benchmark"
                }
            )

        self.stdout.write(self.style.NOTICE("Seeding 40 Ghanaian Breakfast Recipes..."))

        # Catalog: 10 original from book + 30 new Ghanaian breakfast items
        recipes_data = [
            # 1. Ablemamu
            {
                "title": "Ablemamu (Tom Brown Porridge)",
                "twi_name": "Ablemamu",
                "tagline": "Comforting, nutty roasted corn and peanut flour morning porridge",
                "cultural_story": "Across the diaspora you'll see a lot of breakfast porridges: cream of wheat, farina, grits. Tom Brown is how a lot of Ghanaians start their day. This comforting meal is made with toasted corn flour spiced with ginger and thickened with evaporated milk, sugar, and peanut butter.",
                "prep_time_minutes": 5, "cook_time_minutes": 15, "total_time_minutes": 20,
                "default_servings": 4, "cost_per_serving_ghs": Decimal("15.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["quick-easy"]],
                "groups": [
                    {"name": "Porridge Base", "ingredients": [("Corn flour", "1 1/4 cups", Decimal("4.50")), ("Peanut flour", "1/2 cup", Decimal("3.00")), ("Palm sugar or brown sugar", "1/2 cup", Decimal("2.00")), ("Evaporated milk", "1 cup", Decimal("3.50")), ("Creamy peanut butter", "1 tablespoon", Decimal("1.00")), ("Ground cinnamon & ginger", "1/2 tsp each", Decimal("1.00"))]},
                    {"name": "Toppings", "ingredients": [("Sweet cherries or berries", "1 cup", Decimal("3.00")), ("Roasted peanuts", "3 tablespoons", Decimal("1.00"))]}
                ],
                "steps": [(1, "Toast the Flours", "Toast corn and peanut flour in oven or dry pan until golden and fragrant, 10 minutes.", 10), (2, "Simmer with Water", "Whisk with 2 cups water in pot and simmer over medium heat until thickened, 7-10 minutes.", 8), (3, "Enrich & Sweeten", "Stir in sugar, evaporated milk, peanut butter, cinnamon, and nutmeg.", 3), (4, "Garnish & Serve", "Serve hot with cherries, crunchy peanuts, and warm evaporated milk.", 0)]
            },

            # 2. Kelewele
            {
                "title": "Kelewele & Roasted Peanuts",
                "twi_name": "Kelewele",
                "tagline": "Spiced ginger fried ripe plantains served with crunchy roasted groundnuts",
                "cultural_story": "A quintessential Ghanaian street food that makes a wonderful energizing morning snack. Ripe yellow plantains are tossed in a pungent paste of ginger, chili, and spices, then fried until caramelized and served with peanuts.",
                "prep_time_minutes": 15, "cook_time_minutes": 5, "total_time_minutes": 20,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("20.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_SAVORY, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegan"], tags["vegetarian"], tags["gluten-free"], tags["quick-easy"]],
                "groups": [
                    {"name": "Spiced Plantains", "ingredients": [("Ripe yellow plantains", "3 fingers", Decimal("12.00")), ("Fresh ginger & garlic", "pureed", Decimal("3.00")), ("Paprika, cayenne, nutmeg", "1 tbsp blend", Decimal("2.00")), ("Peanut oil", "for frying", Decimal("4.00"))]},
                    {"name": "Garnish", "ingredients": [("Roasted groundnuts", "1/2 cup", Decimal("3.00"))]}
                ],
                "steps": [(1, "Blend Spices", "Blend ginger, onion, and garlic with 2 tbsp water into a smooth paste.", 3), (2, "Cube & Marinate", "Cube plantains and toss in spice paste for 10 minutes.", 10), (3, "Fry Golden", "Fry in 350°F oil until deeply golden and crispy, about 5 minutes.", 5), (4, "Serve", "Drain on paper towels and serve with roasted peanuts.", 0)]
            },

            # 3. Sugar Bread with Fried Eggs & Milo
            {
                "title": "Sugar Bread with Fried Eggs & Milo",
                "twi_name": "Paanoo ne Nkesua",
                "tagline": "Accra's beloved everyday breakfast: sweet pillowy toast, fried eggs, and warm frothed Milo",
                "cultural_story": "A classic morning staple across Accra. Fluffy, slightly sweet Ghanaian sugar bread toasted in butter, paired with fresh fried eggs and a steaming mug of frothed Milo chocolate malt drink.",
                "prep_time_minutes": 5, "cook_time_minutes": 10, "total_time_minutes": 15,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("25.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_SAVORY, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["quick-easy"], tags["high-protein"]],
                "groups": [
                    {"name": "Toast & Eggs", "ingredients": [("Ghanaian Sugar bread", "4 thick slices", Decimal("8.00")), ("Fresh eggs", "4 large", Decimal("14.00")), ("Butter", "2 tbsp", Decimal("4.00"))]},
                    {"name": "Milo Drink", "ingredients": [("Milo powder", "2 tbsp", Decimal("6.00")), ("Milk", "1 1/2 cups", Decimal("8.00"))]}
                ],
                "steps": [(1, "Toast Bread", "Griddle thick slices of sugar bread in butter until golden on both sides.", 4), (2, "Fry Eggs", "Fry eggs sunny-side up or scrambled with sea salt and pepper.", 4), (3, "Froth Milo", "Whisk Milo into hot steaming milk until foamy.", 3), (4, "Serve", "Serve warm toast topped with eggs alongside hot Milo.", 0)]
            },

            # 4. Spiced Fonio Porridge
            {
                "title": "Spiced Fonio Porridge with Coconut",
                "twi_name": "Fonio Porridge",
                "tagline": "Ancient West African grain simmered with warm spices and luscious coconut cream",
                "cultural_story": "Fonio is an ancient grain cultivated in West Africa for millennia. Cooked with cinnamon, cardamom, and coconut milk, it forms a light, nutty, and highly digestible breakfast cereal.",
                "prep_time_minutes": 5, "cook_time_minutes": 10, "total_time_minutes": 15,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("30.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegan"], tags["vegetarian"], tags["gluten-free"], tags["dairy-free"], tags["quick-easy"]],
                "groups": [
                    {"name": "Porridge", "ingredients": [("Fonio grain", "1 cup", Decimal("20.00")), ("Cinnamon, cardamom, cloves", "whole spices", Decimal("4.00")), ("Coconut milk", "1 can", Decimal("18.00")), ("Agave or honey", "2 tbsp", Decimal("4.00"))]},
                    {"name": "Fruit", "ingredients": [("Mango or banana slices", "1 cup", Decimal("8.00")), ("Toasted coconut flakes", "2 tbsp", Decimal("3.00"))]}
                ],
                "steps": [(1, "Toast Spices", "Toast whole spices in pot, add water and bring to a boil.", 3), (2, "Simmer Fonio", "Whisk in fonio and simmer for 5 minutes until water is absorbed.", 5), (3, "Cream with Coconut", "Stir in coconut milk and agave, simmering gently until velvety.", 5), (4, "Serve", "Top with fresh tropical mango and coconut flakes.", 0)]
            },

            # 5. Traditional Waakye Morning Plate
            {
                "title": "Traditional Waakye Morning Plate",
                "twi_name": "Waakye",
                "tagline": "The king of Ghanaian morning fuel: burgundy rice and beans with rich red stew, boiled egg, and spicy shito",
                "cultural_story": "The ultimate Ghanaian breakfast powerhouse. Rice and black-eyed peas boiled with dried sorghum leaves for their signature burgundy hue, served with spiced tomato red stew, gari, boiled eggs, and black shito.",
                "prep_time_minutes": 15, "cook_time_minutes": 30, "total_time_minutes": 45,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("40.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.MEDIUM, "tags": [tags["vegetarian"], tags["gluten-free"], tags["high-protein"]],
                "groups": [
                    {"name": "Waakye", "ingredients": [("Jasmine rice & black-eyed peas", "1.5 cups total", Decimal("18.00")), ("Waakye sorghum leaves", "4 leaves", Decimal("3.00")), ("Coconut oil & salt", "2 tbsp", Decimal("4.00"))]},
                    {"name": "Accompaniments", "ingredients": [("Waakye tomato-ginger red stew", "1 cup", Decimal("12.00")), ("Farm eggs", "2 boiled", Decimal("7.00")), ("Moistened Gari", "1/2 cup", Decimal("2.00")), ("Shito pepper sauce", "2 tbsp", Decimal("6.00"))]}
                ],
                "steps": [(1, "Boil Beans with Leaves", "Simmer soaked beans with waakye leaves until water is deep red, 20 mins.", 20), (2, "Cook Rice", "Add rinsed rice to red water and simmer covered on low for 17 mins.", 17), (3, "Warm Accompaniments", "Warm red stew and moisten gari with a spoonful of stew.", 5), (4, "Assemble", "Plate rice and beans, ladle red stew, add halved boiled eggs, gari, and shito.", 0)]
            },

            # 6. Cassava Pancakes with Malted Crumble
            {
                "title": "Cassava Pancakes with Malted Barley Crumble",
                "twi_name": "Cassava Pancakes",
                "tagline": "Crisp-edged gluten-friendly cassava griddle cakes crowned with buttery malted crumble",
                "cultural_story": "A modern diaspora twist on pancakes. Naturally gluten-friendly cassava flour produces a light griddle cake with crispy edges, crowned by a crunchy malted Grape-Nuts crumble.",
                "prep_time_minutes": 15, "cook_time_minutes": 15, "total_time_minutes": 30,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("45.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.NEA_ONNIM,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"]],
                "groups": [
                    {"name": "Crumble", "ingredients": [("Grape-Nuts cereal", "3/4 cup", Decimal("15.00")), ("Butter & brown sugar", "4 tbsp butter", Decimal("8.00")), ("Maple syrup & cinnamon", "blend", Decimal("5.00"))]},
                    {"name": "Pancakes", "ingredients": [("Cassava flour & cornmeal", "1.5 cups", Decimal("14.00")), ("Milk, eggs, vanilla", "wet mix", Decimal("15.00")), ("Baking powder & butter", "enrichment", Decimal("8.00"))]}
                ],
                "steps": [(1, "Make Crumble", "Mix Grape-Nuts, melted butter, brown sugar, and cinnamon until crumbly.", 5), (2, "Make Batter", "Whisk cassava flour with milk, eggs, and melted butter; rest 5 minutes.", 5), (3, "Griddle", "Ladle 1/4-cup portions onto buttered skillet, cooking until golden, 2 mins per side.", 6), (4, "Garnish", "Stack high and top with malted crumble, butter, and maple syrup.", 0)]
            },

            # 7. Egusi & Coconut Granola
            {
                "title": "Egusi and Coconut Granola",
                "twi_name": "Egusi Granola",
                "tagline": "Golden baked oats and West African egusi melon seeds with coconut nectar and fresh thyme",
                "cultural_story": "Nutty West African egusi seeds roasted with rolled oats, almonds, virgin coconut oil, and aromatic fresh thyme for an incredible morning parfait topper.",
                "prep_time_minutes": 15, "cook_time_minutes": 15, "total_time_minutes": 30,
                "default_servings": 4, "cost_per_serving_ghs": Decimal("45.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.NEA_ONNIM,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegan"], tags["vegetarian"], tags["dairy-free"]],
                "groups": [
                    {"name": "Granola Mix", "ingredients": [("Rolled oats & egusi seeds", "1.5 cups", Decimal("25.00")), ("Almonds & flaxseeds", "1/2 cup", Decimal("16.00")), ("Coconut oil & nectar", "liquid glaze", Decimal("18.00")), ("Fresh thyme & vanilla", "dash", Decimal("5.00"))]}
                ],
                "steps": [(1, "Mix", "Toss dry oats, seeds, and thyme with warm melted coconut oil and nectar.", 5), (2, "Bake", "Spread on sheet and bake at 300°F for 25 mins until fragrant and golden.", 25), (3, "Serve", "Cool and serve with yogurt, fresh papaya, or cold milk.", 0)]
            },

            # 8. Biscuits with Guava Thyme Jam
            {
                "title": "Biscuits with Guava Thyme Jam",
                "twi_name": "Guava Butter Biscuits",
                "tagline": "Flaky layered southern-style buttermilk biscuits paired with tropical guava-thyme preserves",
                "cultural_story": "Southern laminated biscuits paired with sweet, floral tropical pink guava preserves steeped with fresh Caribbean thyme and lime.",
                "prep_time_minutes": 25, "cook_time_minutes": 20, "total_time_minutes": 45,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("55.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_SAVORY, "tradition_type": Recipe.TraditionType.NEA_ONNIM,
                "difficulty": Recipe.Difficulty.MEDIUM, "tags": [tags["vegetarian"]],
                "groups": [
                    {"name": "Guava Jam", "ingredients": [("Ripe pink guavas", "2 cups", Decimal("22.00")), ("Thyme, bay leaves, lime", "aromatics", Decimal("6.00")), ("Sugar", "1 cup", Decimal("4.00"))]},
                    {"name": "Biscuits", "ingredients": [("Flour, butter, buttermilk", "biscuit dough", Decimal("48.00")), ("Leaveners & salt", "dash", Decimal("4.00"))]}
                ],
                "steps": [(1, "Make Jam", "Simmer chopped guava with thyme, sugar, and lime until thick, 20 mins.", 20), (2, "Laminate Dough", "Cut cold butter into flour, add buttermilk, fold 3 times and stamp rounds.", 12), (3, "Bake Biscuits", "Bake at 425°F for 15 mins until golden and towering.", 15), (4, "Assemble", "Split warm biscuits and slather with butter and guava jam.", 0)]
            },

            # 9. Roasted Banana Grits with Shrimp
            {
                "title": "Roasted Banana Grits with Seasoned Shrimp",
                "twi_name": "Banana Grits ne Mmɔre",
                "tagline": "Created for East End Bistro: caramelized banana stone-ground grits with garlic-seared shrimp",
                "cultural_story": "Born in Ghana for Accra's East End Bistro. Roasted whole bananas develop a buttery caramel depth that elevates stone-ground grits, crowned with spice-seared fresh prawns.",
                "prep_time_minutes": 15, "cook_time_minutes": 25, "total_time_minutes": 40,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("85.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_SAVORY, "tradition_type": Recipe.TraditionType.NEA_ONNIM,
                "difficulty": Recipe.Difficulty.MEDIUM, "tags": [tags["pescatarian"], tags["high-protein"]],
                "groups": [
                    {"name": "Banana Grits", "ingredients": [("Roasted bananas", "2 pureed", Decimal("6.00")), ("Stone-ground grits", "1 cup", Decimal("18.00")), ("Milk, cream, stock", "2 cups", Decimal("22.00")), ("Mascarpone & butter", "4 tbsp", Decimal("16.00"))]},
                    {"name": "Seared Prawns", "ingredients": [("Large prawns", "8 fresh", Decimal("55.00")), ("All-Day Seasoning Blend", "1 tbsp", Decimal("4.00")), ("Scallions", "garnish", Decimal("3.00"))]}
                ],
                "steps": [(1, "Roast Bananas", "Roast whole bananas in peel at 400°F until dark; peel and puree.", 15), (2, "Simmer Grits", "Cook grits in milk and stock for 20 mins. Fold in banana puree and mascarpone.", 20), (3, "Sear Shrimp", "Sear seasoned prawns in hot skillet with garlic for 3 minutes.", 3), (4, "Serve", "Ladle hot grits into bowls, top with prawns and scallions.", 0)]
            },

            # 10. Eggs Benedict with Scallops & Piri Piri
            {
                "title": "Eggs Benedict with Scallops & Piri Piri Hollandaise",
                "twi_name": "Eggs Benedict Piri Piri",
                "tagline": "Opulent brunch showstopper: seared sea scallops, poached eggs, and fiery citrus piri piri hollandaise",
                "cultural_story": "Top Chef showcase brunch: sweet seared sea scallops and runny poached eggs over toasted English muffins, draped in spicy bird's-eye chili piri piri hollandaise.",
                "prep_time_minutes": 15, "cook_time_minutes": 20, "total_time_minutes": 35,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("140.00"),
                "flavor_profile": Recipe.FlavorProfile.RICH_OPULENT, "tradition_type": Recipe.TraditionType.NEA_ONNIM,
                "difficulty": Recipe.Difficulty.ADVANCED, "tags": [tags["pescatarian"], tags["high-protein"]],
                "groups": [
                    {"name": "Hollandaise", "ingredients": [("Egg yolks & lemon juice", "emulsion", Decimal("18.00")), ("Melted butter", "1.25 cups", Decimal("30.00")), ("Piri Piri sauce", "1/4 cup", Decimal("15.00"))]},
                    {"name": "Scallops & Toast", "ingredients": [("Large sea scallops", "4 U10 scallops", Decimal("130.00")), ("Eggs for poaching", "4 eggs", Decimal("14.00")), ("English muffins & spinach", "base", Decimal("18.00"))]}
                ],
                "steps": [(1, "Hollandaise", "Blend egg yolks and lemon; slowly drizzle warm melted butter until thick; fold in piri piri.", 8), (2, "Poach Eggs", "Poach fresh eggs in vinegar whirlpool for 3 minutes.", 4), (3, "Sear Scallops", "Sear dry scallops in smoking hot pan 4 mins for golden crust.", 5), (4, "Assemble", "Layer muffins with spinach, scallops, poached eggs, and generous hollandaise.", 0)]
            },

            # -------------------------------------------------------------
            # 30 NEW AUTHENTIC GHANAIAN BREAKFAST FOODS
            # -------------------------------------------------------------

            # 11. Hausa Koko with Koose
            {
                "title": "Hausa Koko with Koose",
                "twi_name": "Hausa Koko ne Koose",
                "tagline": "Ghana's iconic spicy fermented millet porridge paired with golden crunchy bean fritters",
                "cultural_story": "The defining street breakfast of Ghana. Smooth, dark millet porridge infused with ginger, black pepper, cloves, and grains of Selim, balanced by hot, airy black-eyed pea fritters (koose) with crunchy edges.",
                "prep_time_minutes": 10, "cook_time_minutes": 15, "total_time_minutes": 25,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("12.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegan"], tags["vegetarian"], tags["high-protein"], tags["quick-easy"]],
                "groups": [
                    {"name": "Spiced Koko", "ingredients": [("Fermented millet dough", "1 cup", Decimal("6.00")), ("Spices (ginger, cloves, grains of Selim)", "blend", Decimal("3.00")), ("Brown sugar to taste", "2 tbsp", Decimal("2.00"))]},
                    {"name": "Koose", "ingredients": [("Whipped black-eyed pea paste with onions and chili", "8 fritters", Decimal("8.00")), ("Vegetable oil", "for frying", Decimal("4.00"))]}
                ],
                "steps": [(1, "Strain & Boil", "Dissolve millet dough in cold water, strain through sieve. Boil water with spices, then whisk in millet paste.", 8), (2, "Thicken", "Simmer on low heat while stirring continuously until glossy and thick.", 5), (3, "Fry Koose", "Drop spoonfuls of aerated bean batter into hot oil; fry until golden brown.", 6), (4, "Serve", "Ladle hot koko into bowls, sweeten with sugar, and serve with hot koose.", 0)]
            },

            # 12. Oblayo with Coconut & Milk
            {
                "title": "Oblayo (Hominy Corn Porridge)",
                "twi_name": "Oblayo",
                "tagline": "Sweet, chewy cracked white maize porridge topped with fresh grated coconut and milk",
                "cultural_story": "A cherished heritage porridge made from coarse hominy maize. The cracked corn kernels soften into a satisfying chewy texture, served warm with sugar, evaporated milk, and freshly grated coconut.",
                "prep_time_minutes": 5, "cook_time_minutes": 25, "total_time_minutes": 30,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("15.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["gluten-free"]],
                "groups": [
                    {"name": "Oblayo Porridge", "ingredients": [("Cracked hominy maize", "1 cup soaked", Decimal("8.00")), ("Sea salt", "pinch", Decimal("0.50")), ("Water", "4 cups", Decimal("0.50"))]},
                    {"name": "Toppings", "ingredients": [("Evaporated milk", "1/2 cup", Decimal("6.00")), ("Grated fresh coconut", "3 tbsp", Decimal("4.00")), ("Sugar", "to taste", Decimal("2.00"))]}
                ],
                "steps": [(1, "Simmer Hominy", "Boil soaked hominy with a pinch of salt until kernels are tender and chewy, about 25 mins.", 25), (2, "Thicken", "Mash a few kernels against the side of the pot to naturally thicken the broth.", 3), (3, "Serve", "Ladle into bowls, sweeten with sugar, add a splash of milk, and heap with freshly grated coconut.", 0)]
            },

            # 13. Rice Porridge (Rice Koko)
            {
                "title": "Rice Porridge (Rice Koko)",
                "twi_name": "Emo Koko",
                "tagline": "Velvety, slow-simmered white rice porridge with evaporated milk and nutmeg",
                "cultural_story": "Light, gentle on the stomach, and deeply comforting. Jasmine rice is simmered until broken down into a soft, creamy porridge, fragrant with freshly grated nutmeg and evaporated milk.",
                "prep_time_minutes": 5, "cook_time_minutes": 20, "total_time_minutes": 25,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("12.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["gluten-free"], tags["quick-easy"]],
                "groups": [
                    {"name": "Rice Porridge", "ingredients": [("Jasmine or white rice", "1 cup", Decimal("7.00")), ("Nutmeg & salt", "pinch", Decimal("1.00")), ("Evaporated milk & sugar", "swirl", Decimal("6.00"))]}
                ],
                "steps": [(1, "Boil Rice", "Boil rice with 4 cups water and a pinch of salt until soft and broken down, 20 mins.", 20), (2, "Whisk Smooth", "Whisk briskly to create a silky, smooth porridge texture.", 2), (3, "Serve", "Pour into bowls, sprinkle nutmeg, and swirl in evaporated milk and sugar.", 0)]
            },

            # 14. Ghanaian Morning Oats with Groundnuts
            {
                "title": "Ghanaian Morning Oats with Groundnuts",
                "twi_name": "Oats ne Nkatie",
                "tagline": "Creamy rolled oats simmered with nutmeg, swirled with Ideal milk and roasted peanuts",
                "cultural_story": "The quickest Ghanaian boarding school and home staple. Oats cooked thick, seasoned with sweet nutmeg, and crowned with crunchy salted roasted groundnuts for protein and texture.",
                "prep_time_minutes": 2, "cook_time_minutes": 8, "total_time_minutes": 10,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("14.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["quick-easy"]],
                "groups": [
                    {"name": "Oats Base", "ingredients": [("Rolled oats", "1 cup", Decimal("8.00")), ("Nutmeg & salt", "pinch", Decimal("1.00")), ("Evaporated milk & sugar", "rich pour", Decimal("7.00"))]},
                    {"name": "Crunch", "ingredients": [("Roasted salted groundnuts", "1/4 cup", Decimal("3.00"))]}
                ],
                "steps": [(1, "Cook Oats", "Boil 2 cups water, stir in oats and a pinch of salt. Simmer 5 mins until thick.", 5), (2, "Season", "Stir in freshly grated nutmeg.", 1), (3, "Garnish", "Ladle into bowls, pour over evaporated milk, sweeten, and top with roasted peanuts.", 0)]
            },

            # 15. Mpampa (Corn Dough Porridge)
            {
                "title": "Mpampa (Fermented Corn Dough Porridge)",
                "twi_name": "Mpampa",
                "tagline": "Traditional tangy fermented corn porridge with sweet evaporated milk and nutmeg",
                "cultural_story": "A classic morning comfort across southern Ghana. Made from smooth fermented white corn dough with a light natural sour tang, balanced with warm spices and sweetened condensed milk.",
                "prep_time_minutes": 5, "cook_time_minutes": 10, "total_time_minutes": 15,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("10.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["gluten-free"], tags["quick-easy"]],
                "groups": [
                    {"name": "Mpampa", "ingredients": [("Fermented white corn dough", "1 cup", Decimal("5.00")), ("Water & salt", "3 cups", Decimal("0.50")), ("Nutmeg, sugar, evaporated milk", "enrichment", Decimal("6.00"))]}
                ],
                "steps": [(1, "Dissolve Dough", "Mix fermented corn dough with water and strain through a fine sieve.", 3), (2, "Cook", "Cook over medium heat, whisking constantly until thick, translucent, and glossy, 8-10 mins.", 9), (3, "Serve", "Pour hot into bowls, sweeten with sugar, add nutmeg, and swirl in evaporated milk.", 0)]
            },

            # 16. Tapioca Porridge
            {
                "title": "Tapioca Porridge",
                "twi_name": "Tapioca",
                "tagline": "Translucent cassava pearls simmered in sweet milk with fresh nutmeg",
                "cultural_story": "Tapioca pearls made from pure cassava starch expand into tender, clear beads as they simmer, yielding a light and delicate porridge beloved for breakfast in Ghana.",
                "prep_time_minutes": 5, "cook_time_minutes": 10, "total_time_minutes": 15,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("15.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["gluten-free"], tags["quick-easy"]],
                "groups": [
                    {"name": "Tapioca", "ingredients": [("Tapioca pearls", "1/2 cup", Decimal("8.00")), ("Water & pinch salt", "3 cups", Decimal("0.50")), ("Evaporated milk & sugar", "to taste", Decimal("7.00")), ("Grated nutmeg", "pinch", Decimal("1.00"))]}
                ],
                "steps": [(1, "Boil Tapioca", "Bring water to boil, stir in tapioca pearls and simmer until pearls turn clear and translucent, 10 mins.", 10), (2, "Enrich", "Stir in pinch of salt and grated nutmeg.", 1), (3, "Serve", "Ladle into bowls with a generous pour of evaporated milk and sugar.", 0)]
            },

            # 17. Wheat Meal / Farina Morning Porridge
            {
                "title": "Wheat Meal (Farina) Morning Porridge",
                "twi_name": "Wheat Porridge",
                "tagline": "Smooth semolina wheat breakfast porridge with evaporated milk and toasted seeds",
                "cultural_story": "A hearty warm breakfast staple popular in Ghanaian homes. Fine wheat semolina cooks quickly into a smooth cereal, enriched with canned milk and brown sugar.",
                "prep_time_minutes": 3, "cook_time_minutes": 7, "total_time_minutes": 10,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("12.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["quick-easy"]],
                "groups": [
                    {"name": "Wheat Base", "ingredients": [("Wheat farina / semolina", "1 cup", Decimal("7.00")), ("Evaporated milk & sugar", "to taste", Decimal("6.00")), ("Nutmeg & cinnamon", "dash", Decimal("1.00"))]}
                ],
                "steps": [(1, "Whisk into Water", "Whisk farina into boiling water to prevent lumps; simmer 5 mins until thick.", 5), (2, "Season", "Add nutmeg, salt, and cinnamon.", 1), (3, "Serve", "Serve hot with milk and sugar.", 0)]
            },

            # 18. Akple Koko / Sorghum Morning Porridge
            {
                "title": "Akple Koko (Red Sorghum Porridge)",
                "twi_name": "Sorghum Koko",
                "tagline": "Nutritious red sorghum morning porridge rich in minerals with groundnut dust",
                "cultural_story": "Sorghum is an ancient climate-resilient grain grown in northern Ghana. Ground into a ruby-hued flour, it makes a nutrient-dense, comforting morning porridge.",
                "prep_time_minutes": 5, "cook_time_minutes": 15, "total_time_minutes": 20,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("12.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegan"], tags["vegetarian"], tags["gluten-free"]],
                "groups": [
                    {"name": "Sorghum", "ingredients": [("Red sorghum flour", "1 cup", Decimal("6.00")), ("Ginger & cloves", "spices", Decimal("2.00")), ("Roasted groundnut powder & sugar", "topping", Decimal("5.00"))]}
                ],
                "steps": [(1, "Mix & Cook", "Mix sorghum flour with cold water, pour into boiling spiced water, whisking until thick, 12 mins.", 12), (2, "Garnish", "Serve warm dusted with roasted groundnut powder and sugar.", 0)]
            },

            # 19. Chibom (Ghanaian Fried Egg & Bread Sandwich)
            {
                "title": "Chibom (Ghanaian Fried Egg & Bread Sandwich)",
                "twi_name": "Chibom",
                "tagline": "Street-side butter bread stuffed with fluffy fried eggs, onions, tomatoes, and sardine oil",
                "cultural_story": "Ghana's answer to the breakfast sub. Freshly baked sweet butter bread sliced open and loaded with a hot omelette studded with diced red onions, fresh tomatoes, and green pepper.",
                "prep_time_minutes": 5, "cook_time_minutes": 5, "total_time_minutes": 10,
                "default_servings": 1, "cost_per_serving_ghs": Decimal("22.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["high-protein"], tags["quick-easy"]],
                "groups": [
                    {"name": "Sandwich", "ingredients": [("Ghanaian butter bread loaf", "1 loaf", Decimal("10.00")), ("Fresh eggs", "3 eggs", Decimal("10.50")), ("Red onion, tomato, chili", "chopped", Decimal("4.00")), ("Margarine or butter", "for frying", Decimal("3.00"))]}
                ],
                "steps": [(1, "Whisk Eggs", "Beat eggs with diced onions, tomatoes, scotch bonnet, and salt.", 2), (2, "Fry Omelette", "Melt butter in skillet, pour eggs and fry until golden on both sides.", 4), (3, "Stuff Bread", "Split fresh bread, slide in the piping-hot omelette, press down, and enjoy.", 0)]
            },

            # 20. Crusty Tea Bread with Blue Band & Sardines
            {
                "title": "Crusty Tea Bread with Blue Band & Sardines",
                "twi_name": "Tea Bread ne Sardines",
                "tagline": "Crusty Ghanaian tea bread spread with salted margarine and loaded with spicy sardines",
                "cultural_story": "The morning savior when you are running out the door. Fresh crusty tea bread, spread thick with Blue Band margarine, packed with canned sardines seasoned with black pepper and raw onions.",
                "prep_time_minutes": 5, "cook_time_minutes": 0, "total_time_minutes": 5,
                "default_servings": 1, "cost_per_serving_ghs": Decimal("18.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["pescatarian"], tags["high-protein"], tags["quick-easy"]],
                "groups": [
                    {"name": "Ingredients", "ingredients": [("Fresh crusty tea bread", "1 loaf", Decimal("8.00")), ("Canned sardines in spiced oil", "1 tin", Decimal("15.00")), ("Blue Band margarine", "generous spread", Decimal("3.00")), ("Sliced red onion & black pepper", "optional", Decimal("1.00"))]}
                ],
                "steps": [(1, "Slice Bread", "Slice tea bread lengthwise.", 1), (2, "Spread & Fill", "Spread with Blue Band, lay seasoned sardines inside, top with onion slices, and press closed.", 2)]
            },

            # 21. Bofrot (Nutmeg Puff-Puff)
            {
                "title": "Bofrot (Nutmeg Puff-Puff with Spiced Sugar)",
                "twi_name": "Bofrot",
                "tagline": "Golden-brown pillowy yeast doughnuts with freshly grated nutmeg and cinnamon-sugar",
                "cultural_story": "At every Ghanaian get-together or morning corner, aunties fry fresh bofrot. Hot, pillowy, dark caramel-colored spheres of yeasted dough with hints of nutmeg rolled in cinnamon sugar.",
                "prep_time_minutes": 15, "cook_time_minutes": 10, "total_time_minutes": 25,
                "default_servings": 4, "cost_per_serving_ghs": Decimal("12.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.MEDIUM, "tags": [tags["vegetarian"]],
                "groups": [
                    {"name": "Dough", "ingredients": [("All-purpose flour & yeast", "2 cups", Decimal("10.00")), ("Sugar & milk", "wet mix", Decimal("8.00")), ("Nutmeg & salt", "pinch", Decimal("1.50")), ("Oil for frying", "3 cups", Decimal("8.00"))]},
                    {"name": "Spiced Sugar", "ingredients": [("Cinnamon & sugar", "coating", Decimal("2.00"))]}
                ],
                "steps": [(1, "Rise Dough", "Whisk yeast, warm milk, flour, sugar, and nutmeg into a batter; proof until doubled.", 15), (2, "Fry", "Drop spoonfuls into 350°F oil and fry until golden brown all over, 5 mins.", 5), (3, "Toss Sugar", "Toss warm bofrot in cinnamon-nutmeg sugar and serve.", 0)]
            },

            # 22. Pinkaso (Savory Spiced Ring Dumplings)
            {
                "title": "Pinkaso (Savory Spiced Ring Dumplings)",
                "twi_name": "Pinkaso",
                "tagline": "Crispy fried savory flour rings flavored with ginger, onions, and hot pepper",
                "cultural_story": "A classic savory fried accompaniment to morning Hausa Koko. Lightly fermented flour dough seasoned with ginger, onion, and chili, shaped into rings with a hole in the center and fried crisp.",
                "prep_time_minutes": 10, "cook_time_minutes": 10, "total_time_minutes": 20,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("10.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegan"], tags["vegetarian"], tags["quick-easy"]],
                "groups": [
                    {"name": "Dough", "ingredients": [("Flour & baking powder", "1.5 cups", Decimal("8.00")), ("Ginger, onion, scotch bonnet", "pureed", Decimal("4.00")), ("Frying oil", "2 cups", Decimal("6.00"))]}
                ],
                "steps": [(1, "Knead Spiced Dough", "Mix flour with pureed ginger, onion, chili, salt, and water into a soft dough.", 5), (2, "Shape & Fry", "Wet hands, take a ball, poke hole in middle and drop in hot oil; fry until golden and crisp.", 6), (3, "Serve", "Dip into hot spiced porridge or eat warm.", 0)]
            },

            # 23. Tatale (Spiced Ripe Plantain Pancakes)
            {
                "title": "Tatale (Spiced Ripe Plantain Pancakes)",
                "twi_name": "Tatale",
                "tagline": "Golden shallow-fried ripe plantain and fermented corn dough cakes spiced with ginger",
                "cultural_story": "A brilliant zero-waste Ghanaian morning dish. Very ripe plantains are mashed and combined with fermented corn dough, fresh ginger, and peppers, then griddled into tender, sweet-savory cakes.",
                "prep_time_minutes": 10, "cook_time_minutes": 10, "total_time_minutes": 20,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("18.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_SAVORY, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegan"], tags["vegetarian"], tags["gluten-free"]],
                "groups": [
                    {"name": "Batter", "ingredients": [("Overripe plantains", "2 fingers mashed", Decimal("8.00")), ("Fermented corn dough or flour", "1/2 cup", Decimal("4.00")), ("Grated ginger, onion, cayenne", "spices", Decimal("3.00")), ("Palm oil or vegetable oil", "for shallow frying", Decimal("4.00"))]}
                ],
                "steps": [(1, "Mash & Mix", "Mash overripe plantains with fork; mix in corn dough, grated ginger, onion, and cayenne.", 5), (2, "Pan-Fry", "Heat oil in skillet; ladle batter into small rounds and fry until dark golden, 3 mins per side.", 6), (3, "Serve", "Serve hot with roasted peanuts or Bambara groundnut stew.", 0)]
            },

            # 24. Ghanaian Flaky Meat Pie
            {
                "title": "Ghanaian Flaky Meat Pie",
                "twi_name": "Meat Pie",
                "tagline": "Flaky golden shortcrust pastry filled with savory spiced ground beef, carrots, and potatoes",
                "cultural_story": "Every bakery and street corner in Accra has warm meat pies ready by 7 AM. Golden, flaky buttery pastry wrapped around seasoned minced beef with hints of nutmeg and curry.",
                "prep_time_minutes": 20, "cook_time_minutes": 20, "total_time_minutes": 40,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("20.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.MEDIUM, "tags": [tags["high-protein"]],
                "groups": [
                    {"name": "Pastry", "ingredients": [("Flour, cold butter, ice water", "crust", Decimal("16.00"))]},
                    {"name": "Filling", "ingredients": [("Minced ground beef", "250g", Decimal("22.00")), ("Onion, carrots, potatoes", "diced", Decimal("6.00")), ("Curry, thyme, nutmeg", "seasoning", Decimal("2.00"))]}
                ],
                "steps": [(1, "Cook Filling", "Brown ground beef with onions, diced carrots, potatoes, and curry powder; cool.", 10), (2, "Roll Pastry", "Roll out buttery dough, cut into circles, fill with beef, and crimp edges with fork.", 10), (3, "Bake", "Brush with egg wash and bake at 375°F for 20 mins until deep golden.", 20)]
            },

            # 25. Gob3 (Red Red / Beans & Gari)
            {
                "title": "Gob3 (Red Red Beans, Gari, Plantain & Zomi)",
                "twi_name": "Gob3",
                "tagline": "The legendary street fuel: tender black-eyed peas in red palm oil with sweet fried plantains and gari",
                "cultural_story": "Affectionately known as Gob3, this is the champion meal for workers and students across Ghana. Slow-simmered cowpeas stewed with aromatics in red palm oil (zomi), served with fried ripe plantains and gari.",
                "prep_time_minutes": 10, "cook_time_minutes": 25, "total_time_minutes": 35,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("25.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_SAVORY, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["vegan"], tags["high-protein"]],
                "groups": [
                    {"name": "Beans Stew", "ingredients": [("Black-eyed peas", "1.5 cups cooked", Decimal("10.00")), ("Zomi (red palm oil)", "3 tbsp", Decimal("6.00")), ("Tomato paste, onion, pepper", "sauce base", Decimal("6.00"))]},
                    {"name": "Sides", "ingredients": [("Ripe plantains", "2 fried", Decimal("10.00")), ("Gari", "1/2 cup", Decimal("2.00")), ("Boiled egg", "optional", Decimal("3.50"))]}
                ],
                "steps": [(1, "Make Zomi Sauce", "Heat red palm oil; fry chopped onions until fragrant, add tomato paste and chili.", 6), (2, "Stew Beans", "Stir in tender cooked black-eyed peas and simmer until thick and savory.", 10), (3, "Fry Plantains", "Fry salted ripe plantain slices until caramelized.", 6), (4, "Assemble", "Spoon beans over gari, crown with sweet fried plantains and boiled egg.", 0)]
            },

            # 26. Ga Kenkey with Fried Fish, Pepper & Shito
            {
                "title": "Ga Kenkey with Fried Fish, Pepper & Shito",
                "twi_name": "Komie (Ga Kenkey)",
                "tagline": "Steamed fermented corn dumpling with crispy fried fish, crushed fresh pepper, and black shito",
                "cultural_story": "A coastal morning staple. Fermented white corn dough steamed in cornhusks until dense and sour, eaten with hands by pinching a piece and scooping up spicy crushed raw tomato-pepper sauce and whole fried fish.",
                "prep_time_minutes": 10, "cook_time_minutes": 15, "total_time_minutes": 25,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("30.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.MEDIUM, "tags": [tags["pescatarian"], tags["high-protein"]],
                "groups": [
                    {"name": "Kenkey & Fish", "ingredients": [("Ga Kenkey balls", "2 balls", Decimal("16.00")), ("Fried freshwater fish (tilapia/red fish)", "2 pieces", Decimal("28.00"))]},
                    {"name": "Sauces", "ingredients": [("Raw pepper sauce (tomato, onion, scotch bonnet crushed in asanka)", "1 bowl", Decimal("8.00")), ("Shito pepper condiment", "2 tbsp", Decimal("6.00"))]}
                ],
                "steps": [(1, "Steam Kenkey", "Steam pre-made kenkey until piping hot.", 10), (2, "Fry Fish", "Fry seasoned fish until crisp on outside and tender within.", 8), (3, "Grind Fresh Pepper", "In an asanka or mortar, grind fresh scotch bonnets, onion, tomato, and sea salt.", 4), (4, "Serve", "Unwrap hot kenkey and serve with fish, fresh pepper, and shito.", 0)]
            },

            # 27. Ampesi (Boiled Yam with Kontomire Egg Stew)
            {
                "title": "Ampesi (Boiled Yam with Kontomire Egg Stew)",
                "twi_name": "Ampesi ne Kontomire",
                "tagline": "Steamed puna yam wedges served with rich cocoyam greens stew, smoked fish, and boiled eggs",
                "cultural_story": "A classic Sunday morning breakfast. Thick cuts of white puna yam boiled with salt, accompanied by an earthy cocoyam leaf (kontomire) stew enriched with red palm oil, koobi (salted fish), and boiled eggs.",
                "prep_time_minutes": 15, "cook_time_minutes": 25, "total_time_minutes": 40,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("35.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.MEDIUM, "tags": [tags["high-protein"], tags["gluten-free"]],
                "groups": [
                    {"name": "Boiled Yam", "ingredients": [("Puna yam slices", "4 thick pieces", Decimal("18.00")), ("Sea salt", "water", Decimal("0.50"))]},
                    {"name": "Kontomire Stew", "ingredients": [("Kontomire or spinach", "1 bunch", Decimal("10.00")), ("Red palm oil & onions", "sauce base", Decimal("8.00")), ("Smoked mackerel or koobi", "flaked", Decimal("15.00")), ("Boiled eggs", "2 eggs", Decimal("7.00"))]}
                ],
                "steps": [(1, "Boil Yam", "Peel yam, cut into wedges, boil in salted water until fork-tender, 18 mins.", 18), (2, "Cook Greens", "Steam kontomire until wilted; blend or crush in asanka.", 5), (3, "Stew Sauce", "Heat palm oil, sauté onions and smoked fish, add crushed greens and simmer.", 10), (4, "Plate", "Serve boiled yam alongside rich kontomire stew with halved boiled eggs.", 0)]
            },

            # 28. Boiled Sweet Potatoes with Sardine & Egg Sauce
            {
                "title": "Boiled Sweet Potatoes with Sardine & Egg Sauce",
                "twi_name": "Santew ne Nkesua",
                "tagline": "Tender boiled sweet potatoes paired with a savory scrambled egg, tomato, and sardine sauce",
                "cultural_story": "A fast and colorful morning plate. Sweet orange or white sweet potatoes boiled tender, balanced with a savory scramble of eggs, canned sardines, tomatoes, and spicy scotch bonnet.",
                "prep_time_minutes": 10, "cook_time_minutes": 15, "total_time_minutes": 25,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("24.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_SAVORY, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["pescatarian"], tags["high-protein"], tags["gluten-free"], tags["quick-easy"]],
                "groups": [
                    {"name": "Sweet Potatoes", "ingredients": [("Sweet potatoes", "3 medium peeled", Decimal("12.00")), ("Salted water", "pinch", Decimal("0.50"))]},
                    {"name": "Egg & Sardine Sauce", "ingredients": [("Fresh eggs", "3 eggs", Decimal("10.50")), ("Canned sardines", "1 tin", Decimal("15.00")), ("Tomatoes & onions", "diced", Decimal("5.00")), ("Vegetable oil", "2 tbsp", Decimal("3.00"))]}
                ],
                "steps": [(1, "Boil Potatoes", "Cut sweet potatoes into rounds and boil until tender, 12 mins.", 12), (2, "Sauté Sauce", "Sauté onions and tomatoes in oil until softened; stir in flaked sardines and beat in eggs.", 6), (3, "Serve", "Plate tender sweet potatoes and top with hot sardine-egg scramble.", 0)]
            },

            # 29. Fried Puna Yam with Chofi (Turkey Tail) & Shito
            {
                "title": "Fried Puna Yam with Chofi (Turkey Tail) & Shito",
                "twi_name": "Yam Chips ne Tsofi",
                "tagline": "Crisp white yam steak fries served with spicy fried turkey tail and black shito",
                "cultural_story": "Street-style indulgence. Thick-cut puna yam fries crispy on the outside and fluffy inside, served with deeply seasoned, crispy fried turkey tail (tsofi) and pungent black pepper shito.",
                "prep_time_minutes": 10, "cook_time_minutes": 15, "total_time_minutes": 25,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("32.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["gluten-free"]],
                "groups": [
                    {"name": "Yam Chips", "ingredients": [("Puna yam", "peeled and sliced into steak fries", Decimal("18.00")), ("Oil for frying", "3 cups", Decimal("10.00"))]},
                    {"name": "Chofi & Sauce", "ingredients": [("Seasoned turkey tail (tsofi)", "fried crispy", Decimal("25.00")), ("Shito & fresh green pepper sauce", "condiments", Decimal("6.00"))]}
                ],
                "steps": [(1, "Soak Yam", "Soak yam slices in salted water for 10 mins; pat completely dry.", 10), (2, "Fry", "Fry yam in hot 375°F oil until crisp and pale golden; fry seasoned turkey tail until crispy.", 8), (3, "Serve", "Drain on paper towels, sprinkle sea salt, and serve with shito.", 0)]
            },

            # 30. Boiled Yam with Garden Egg Stew
            {
                "title": "Boiled Yam with Garden Egg Stew",
                "twi_name": "Yam ne Asadua Stew",
                "tagline": "Steamed puna yam accompanied by a rich, earthy African garden egg and smoked fish stew",
                "cultural_story": "African garden eggs (mini round eggplants) are boiled, skinned, and mashed into a deeply savory red palm oil stew with smoked mackerel and aromatics, paired with steamed white yam.",
                "prep_time_minutes": 15, "cook_time_minutes": 20, "total_time_minutes": 35,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("32.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.MEDIUM, "tags": [tags["gluten-free"]],
                "groups": [
                    {"name": "Yam", "ingredients": [("Puna yam slices", "4 thick cuts", Decimal("18.00"))]},
                    {"name": "Garden Egg Stew", "ingredients": [("Garden eggs", "6 boiled and mashed", Decimal("10.00")), ("Red palm oil", "3 tbsp", Decimal("6.00")), ("Smoked mackerel & onions", "flavor base", Decimal("16.00"))]}
                ],
                "steps": [(1, "Boil Yam & Garden Eggs", "Boil yam in one pot; boil garden eggs in another until soft, 15 mins.", 15), (2, "Mash Garden Eggs", "Peel garden eggs and mash with fork or in asanka.", 3), (3, "Simmer Stew", "Heat palm oil, sauté onions and smoked mackerel, add mashed garden eggs and simmer 8 mins.", 8), (4, "Serve", "Serve hot steamed yam topped with savory garden egg sauce.", 0)]
            },

            # 31. Fried Plantains with Corned Beef Stew
            {
                "title": "Fried Plantains with Corned Beef Stew",
                "twi_name": "Kokoode ne Corned Beef",
                "tagline": "Caramelized sweet fried plantains with rich tomato-rosemary corned beef stew",
                "cultural_story": "A classic weekend luxury in many Ghanaian homes. Sweet caramelized ripe plantains paired with a savory, rosemary-infused corned beef stew bursting with tomatoes and onions.",
                "prep_time_minutes": 10, "cook_time_minutes": 15, "total_time_minutes": 25,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("38.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_SAVORY, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["gluten-free"]],
                "groups": [
                    {"name": "Plantains", "ingredients": [("Ripe yellow plantains", "3 fingers", Decimal("12.00")), ("Oil for frying", "2 cups", Decimal("6.00"))]},
                    {"name": "Corned Beef Stew", "ingredients": [("Canned corned beef", "1 tin", Decimal("42.00")), ("Tomatoes, onion, rosemary, chili", "sauce", Decimal("8.00"))]}
                ],
                "steps": [(1, "Sauté Stew", "Sauté onions, tomatoes, and rosemary in oil; add corned beef and break up with spoon; simmer 8 mins.", 8), (2, "Fry Plantains", "Fry plantain slices until caramelized and golden, 5 mins.", 5), (3, "Serve", "Plate sweet plantains alongside hot savory corned beef stew.", 0)]
            },

            # 32. Tubani (Steamed Bean Pudding)
            {
                "title": "Tubani (Steamed Bean Pudding with Pepper & Oil)",
                "twi_name": "Tubani",
                "tagline": "Northern Ghanaian steamed black-eyed pea pudding served with spiced pepper powder and warm oil",
                "cultural_story": "A celebrated dish from northern Ghana. Black-eyed pea flour whipped with water and a touch of saltpeter, steamed in leaves or ramekins until soft and cake-like, dressed with warm oil and ground hot pepper.",
                "prep_time_minutes": 10, "cook_time_minutes": 25, "total_time_minutes": 35,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("15.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.MEDIUM, "tags": [tags["vegan"], tags["vegetarian"], tags["gluten-free"], tags["high-protein"]],
                "groups": [
                    {"name": "Tubani Batter", "ingredients": [("Cowpea/black-eyed pea flour", "1.5 cups", Decimal("10.00")), ("Saltpeter/potash pinch", "dash", Decimal("1.00")), ("Water", "whipped", Decimal("0.50"))]},
                    {"name": "Dressing", "ingredients": [("Warm vegetable oil or shea butter", "2 tbsp", Decimal("4.00")), ("Ground dry pepper & sliced raw onions", "garnish", Decimal("3.00"))]}
                ],
                "steps": [(1, "Whip Batter", "Whip bean flour with water and saltpeter until fluffy and aerated.", 5), (2, "Steam", "Wrap in leaves or grease ramekins; steam over boiling water for 25 mins until set.", 25), (3, "Garnish", "Unwrap, drizzle with warm oil, and dust generously with ground pepper and onion rings.", 0)]
            },

            # 33. Steamed Hot Milo with Ideal Milk & Sugar Bread
            {
                "title": "Steamed Hot Milo with Ideal Milk & Sugar Bread",
                "twi_name": "Milo Drink ne Paanoo",
                "tagline": "The national morning chocolate malt beverage frothed with evaporated milk and sweet bread",
                "cultural_story": "Milo is a staple in every Ghanaian household. Stirred into boiling water, whipped with thick Ideal evaporated milk, and served with thick slices of sweet sugar bread for dipping.",
                "prep_time_minutes": 2, "cook_time_minutes": 3, "total_time_minutes": 5,
                "default_servings": 1, "cost_per_serving_ghs": Decimal("12.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["quick-easy"]],
                "groups": [
                    {"name": "Beverage", "ingredients": [("Milo powder", "3 heaping tbsp", Decimal("6.00")), ("Ideal evaporated milk", "1/2 cup", Decimal("5.00")), ("Sugar bread slice", "thick slice for dipping", Decimal("4.00"))]}
                ],
                "steps": [(1, "Mix Milo", "Stir Milo into 1 cup boiling water.", 2), (2, "Add Milk", "Pour in evaporated milk and whisk until rich and frothy.", 1), (3, "Enjoy", "Serve with thick sweet sugar bread to dip into the hot mug.", 0)]
            },

            # 34. Spiced Ghanaian Black Tea with Milk
            {
                "title": "Spiced Ghanaian Black Tea with Milk",
                "twi_name": "Tea",
                "tagline": "Rich Lipton black tea steeped with cinnamon bark and nutmeg, finished with creamy evaporated milk",
                "cultural_story": "Tea in Ghana is an event. Strong black tea steeped with whole cinnamon sticks and grated nutmeg, topped generously with canned evaporated milk and sugar.",
                "prep_time_minutes": 2, "cook_time_minutes": 5, "total_time_minutes": 7,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("10.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["quick-easy"]],
                "groups": [
                    {"name": "Tea", "ingredients": [("Black tea bags (Lipton)", "2 bags", Decimal("3.00")), ("Cinnamon stick & nutmeg", "spices", Decimal("2.00")), ("Evaporated milk & sugar", "pour", Decimal("6.00"))]}
                ],
                "steps": [(1, "Steep", "Boil water with cinnamon stick; steep tea bags 4 minutes.", 4), (2, "Milk & Spice", "Remove tea bags, stir in evaporated milk, sugar, and fresh nutmeg.", 2), (3, "Serve", "Pour into mugs and enjoy warm.", 0)]
            },

            # 35. Brukina (Millet & Yogurt Morning Smoothie)
            {
                "title": "Brukina (Millet & Yogurt Morning Smoothie)",
                "twi_name": "Brukina",
                "tagline": "Wholesome Northern Ghanaian smoothie of steamed millet pearls and sweet creamy milk yogurt",
                "cultural_story": "A refreshing Northern Ghanaian staple. Ground millet is rolled into tiny pearls, steamed until soft, and suspended in cold sweet yogurt with vanilla and nutmeg.",
                "prep_time_minutes": 5, "cook_time_minutes": 0, "total_time_minutes": 5,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("15.00"),
                "flavor_profile": Recipe.FlavorProfile.LIGHT_FRESH, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["gluten-free"], tags["quick-easy"]],
                "groups": [
                    {"name": "Brukina", "ingredients": [("Steamed millet pearls", "1 cup", Decimal("8.00")), ("Whole milk yogurt", "2 cups", Decimal("16.00")), ("Sugar & vanilla extract", "sweetener", Decimal("3.00")), ("Fresh nutmeg", "grated", Decimal("1.00"))]}
                ],
                "steps": [(1, "Blend & Combine", "Whisk whole milk yogurt with sugar, vanilla, and grated nutmeg.", 3), (2, "Stir Pearls", "Fold in the chilled steamed millet pearls.", 2), (3, "Serve", "Serve chilled in glasses as a high-energy morning breakfast drink.", 0)]
            },

            # 36. Asana (Caramelized Fermented Corn Drink)
            {
                "title": "Asana (Caramelized Fermented Corn Drink)",
                "twi_name": "Asana",
                "tagline": "Traditional sweet fermented crushed corn drink with caramel notes and a splash of milk",
                "cultural_story": "Made by boiling crushed fermented white corn until flavorful, then combining it with deeply caramelized sugar syrup. Served chilled with a layer of evaporated milk.",
                "prep_time_minutes": 5, "cook_time_minutes": 15, "total_time_minutes": 20,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("12.00"),
                "flavor_profile": Recipe.FlavorProfile.LIGHT_FRESH, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["gluten-free"]],
                "groups": [
                    {"name": "Asana", "ingredients": [("Crushed fermented corn water", "2 cups", Decimal("6.00")), ("Caramelized sugar syrup", "1/2 cup", Decimal("4.00")), ("Evaporated milk & ice", "to finish", Decimal("5.00"))]}
                ],
                "steps": [(1, "Caramelize Sugar", "Melt sugar in pot until deep amber caramel; carefully add boiling water to form syrup.", 5), (2, "Mix with Corn", "Combine caramel syrup with strained fermented corn broth; chill.", 10), (3, "Serve", "Pour over ice and top with a splash of evaporated milk.", 0)]
            },

            # 37. Koose (Golden Black-Eyed Pea Fritters)
            {
                "title": "Koose (Golden Black-Eyed Pea Fritters)",
                "twi_name": "Koose",
                "tagline": "Airy, golden-brown whipped cowpea fritters seasoned with ginger and scotch bonnet",
                "cultural_story": "Soaked black-eyed peas pureed with fresh ginger, onions, and scotch bonnet peppers, vigorously whipped to incorporate air, and spooned into hot oil to yield crispy, golden fritters.",
                "prep_time_minutes": 10, "cook_time_minutes": 8, "total_time_minutes": 18,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("10.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegan"], tags["vegetarian"], tags["gluten-free"], tags["high-protein"], tags["quick-easy"]],
                "groups": [
                    {"name": "Batter", "ingredients": [("Soaked black-eyed peas", "1.5 cups blended", Decimal("8.00")), ("Ginger, onion, chili, salt", "pureed", Decimal("3.00")), ("Vegetable oil", "for frying", Decimal("6.00"))]}
                ],
                "steps": [(1, "Whip Batter", "Blend soaked peas with aromatics; whip with wooden spoon for 5 mins to trap air.", 5), (2, "Fry", "Drop spoonfuls into hot 360°F oil and fry until golden on both sides, 4 mins.", 4), (3, "Serve", "Drain on paper towels and eat warm with porridge or alone.", 0)]
            },

            # 38. Fried Wagashi (Fulani Cheese) with Suya Pepper
            {
                "title": "Fried Wagashi (Fulani Cheese) with Suya Pepper",
                "twi_name": "Wagashi",
                "tagline": "Pan-seared squeaky artisanal cow's milk cheese dusted with spicy roasted peanut suya seasoning",
                "cultural_story": "Artisanal West African cheese crafted by the Fulani people. It doesn't melt when cooked, forming a crisp golden exterior and squeaky, savory bite when dusted with spicy peanut suya powder.",
                "prep_time_minutes": 3, "cook_time_minutes": 7, "total_time_minutes": 10,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("22.00"),
                "flavor_profile": Recipe.FlavorProfile.SAVORY_SPICED, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.EASY, "tags": [tags["vegetarian"], tags["gluten-free"], tags["high-protein"], tags["quick-easy"]],
                "groups": [
                    {"name": "Cheese & Spice", "ingredients": [("Fresh Wagashi cheese", "250g sliced", Decimal("25.00")), ("Suya spice blend (roasted peanut & pepper)", "2 tbsp", Decimal("5.00")), ("Vegetable oil", "2 tbsp for searing", Decimal("3.00"))]}
                ],
                "steps": [(1, "Slice", "Slice wagashi into 1/2-inch thick slabs.", 2), (2, "Sear", "Heat oil in skillet; sear cheese slabs for 2-3 minutes per side until golden and crispy.", 5), (3, "Dust & Serve", "Dust immediately with suya spice and serve hot.", 0)]
            },

            # 39. Atadwe Milk (Tigernut Pudding)
            {
                "title": "Atadwe Milk (Tigernut Pudding)",
                "twi_name": "Atadwe Milk",
                "tagline": "Naturally sweet, creamy tigernut and jasmine rice pudding with nutmeg and caramel",
                "cultural_story": "Tigernuts (earth almonds) are indigenous to Africa. Ground with jasmine rice and strained through cloth, the milk is gently heated until it naturally thickens into a caramel-scented pudding.",
                "prep_time_minutes": 10, "cook_time_minutes": 15, "total_time_minutes": 25,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("18.00"),
                "flavor_profile": Recipe.FlavorProfile.SWEET_WARM, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.MEDIUM, "tags": [tags["vegetarian"], tags["gluten-free"]],
                "groups": [
                    {"name": "Pudding", "ingredients": [("Tigernuts & jasmine rice", "soaked & pureed", Decimal("16.00")), ("Sugar & warm water", "caramel syrup", Decimal("4.00")), ("Nutmeg & vanilla", "dash", Decimal("2.00")), ("Evaporated milk", "splash", Decimal("4.00"))]}
                ],
                "steps": [(1, "Extract Milk", "Blend soaked tigernuts and rice with water; squeeze through cheesecloth to extract milk.", 8), (2, "Simmer", "Heat tigernut milk in saucepan over medium-low, whisking constantly until thick, 10 mins.", 10), (3, "Fold Caramel", "Stir in caramel syrup, nutmeg, and evaporated milk.", 2), (4, "Serve", "Serve warm or chilled in glasses.", 0)]
            },

            # 40. Apapransa
            {
                "title": "Apapransa (Roasted Corn Flour in Palm Nut Soup)",
                "twi_name": "Apapransa",
                "tagline": "Heritage weekend celebration dish: roasted corn meal stirred into rich palm nut soup with crab",
                "cultural_story": "A celebrated Ga and Akan heritage meal. Toasted, fragrant roasted corn flour (tombrown flour) is vigorously stirred into simmering, earthy palm nut soup with smoked fish and crab.",
                "prep_time_minutes": 15, "cook_time_minutes": 25, "total_time_minutes": 40,
                "default_servings": 2, "cost_per_serving_ghs": Decimal("45.00"),
                "flavor_profile": Recipe.FlavorProfile.RICH_OPULENT, "tradition_type": Recipe.TraditionType.SANKOFA,
                "difficulty": Recipe.Difficulty.ADVANCED, "tags": [tags["pescatarian"], tags["high-protein"]],
                "groups": [
                    {"name": "Base", "ingredients": [("Roasted corn flour", "1.5 cups", Decimal("12.00")), ("Palm nut soup concentrate", "2 cups", Decimal("24.00")), ("Smoked fish & crab", "proteins", Decimal("35.00")), ("Prekese & spices", "aromatics", Decimal("5.00"))]}
                ],
                "steps": [(1, "Boil Soup", "Simmer palm nut soup with smoked fish and crab until fragrant and oil rises, 15 mins.", 15), (2, "Stir in Flour", "Gradually sprinkle in roasted corn flour while stirring vigorously with wooden spatula to prevent lumps.", 10), (3, "Mash & Fold", "Mash and fold until smooth, thick, and pulling from the sides of the pot.", 5), (4, "Serve", "Mound into bowls, top with whole cooked crab, and serve piping hot.", 0)]
            },
        ]

        for r_data in recipes_data:
            recipe, created = Recipe.objects.update_or_create(
                slug=slugify(r_data["title"]),
                defaults={
                    "title": r_data["title"],
                    "twi_name": r_data.get("twi_name", ""),
                    "tagline": r_data["tagline"],
                    "cultural_story": r_data["cultural_story"],
                    "prep_time_minutes": r_data["prep_time_minutes"],
                    "cook_time_minutes": r_data["cook_time_minutes"],
                    "total_time_minutes": r_data["total_time_minutes"],
                    "default_servings": r_data["default_servings"],
                    "cost_per_serving_ghs": r_data["cost_per_serving_ghs"],
                    "flavor_profile": r_data["flavor_profile"],
                    "tradition_type": r_data["tradition_type"],
                    "difficulty": r_data["difficulty"],
                    "is_active": True,
                }
            )

            # Assign tags
            recipe.dietary_tags.set(r_data["tags"])

            # Clean and re-seed groups and ingredients
            recipe.ingredient_groups.all().delete()
            for g_idx, g_data in enumerate(r_data["groups"]):
                group = IngredientGroup.objects.create(
                    recipe=recipe,
                    name=g_data["name"],
                    order=g_idx
                )
                for ing_idx, ing_item in enumerate(g_data["ingredients"]):
                    item_name = ing_item[0]
                    quantity = ing_item[1]
                    portion_cost = ing_item[2] if len(ing_item) > 2 else Decimal("0.00")
                    note = ing_item[3] if len(ing_item) > 3 else ""
                    is_opt = ing_item[4] if len(ing_item) > 4 else False
                    RecipeIngredient.objects.create(
                        group=group,
                        item_name=item_name,
                        quantity=quantity,
                        portion_cost_ghs=portion_cost,
                        substitution_note=note,
                        is_optional=is_opt,
                        order=ing_idx
                    )

            # Clean and re-seed steps
            recipe.steps.all().delete()
            for s_num, s_heading, s_instruction, s_timer in r_data["steps"]:
                InstructionStep.objects.create(
                    recipe=recipe,
                    step_number=s_num,
                    heading=s_heading,
                    instruction=s_instruction,
                    timer_minutes=s_timer if s_timer > 0 else None
                )

            status = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"  [OK] {status}: {recipe.title} (GHS {recipe.cost_per_serving_ghs:.2f})"))

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(recipes_data)} Ghanaian breakfast recipes with Ghana Cedis pricing!"))
