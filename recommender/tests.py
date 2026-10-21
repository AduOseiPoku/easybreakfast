from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from recommender.models import Recipe, DietaryTag
from recommender.services import BreakfastRecommender


class BreakfastRecommenderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Seed tags
        self.veg_tag = DietaryTag.objects.create(name="Vegetarian", slug="vegetarian")
        self.vegan_tag = DietaryTag.objects.create(name="Vegan", slug="vegan")

        # Seed test recipes
        self.r1 = Recipe.objects.create(
            title="Ablemamu (Tom Brown Porridge)",
            tagline="Quick porridge",
            cultural_story="Story...",
            prep_time_minutes=5,
            cook_time_minutes=15,
            total_time_minutes=20,
            cost_per_serving_ghs=Decimal("15.00"),
            flavor_profile=Recipe.FlavorProfile.SWEET_WARM,
            tradition_type=Recipe.TraditionType.SANKOFA,
            is_active=True
        )
        self.r1.dietary_tags.add(self.veg_tag)

        self.r2 = Recipe.objects.create(
            title="Eggs Benedict with Scallops & Piri Piri",
            tagline="Opulent brunch",
            cultural_story="Story...",
            prep_time_minutes=15,
            cook_time_minutes=20,
            total_time_minutes=35,
            cost_per_serving_ghs=Decimal("140.00"),
            flavor_profile=Recipe.FlavorProfile.RICH_OPULENT,
            tradition_type=Recipe.TraditionType.NEA_ONNIM,
            is_active=True
        )

    def test_recommender_filters_by_budget(self):
        """User with GH₵ 30 budget should receive Ablemamu (GH₵ 15) and NOT Scallop Benedict (GH₵ 140)."""
        result = BreakfastRecommender.recommend(
            budget_ghs=Decimal("30.00"),
            max_time_minutes=30,
            servings=1
        )
        self.assertTrue(result.has_recommendation)
        self.assertEqual(result.top_recipe.id, self.r1.id)
        self.assertFalse(result.is_fallback)
        self.assertEqual(result.top_surplus_ghs, Decimal("15.00"))

    def test_recommender_handles_low_budget_gracefully(self):
        """User with GH₵ 8 budget should get closest fallback with helpful explanation."""
        result = BreakfastRecommender.recommend(
            budget_ghs=Decimal("8.00"),
            servings=1
        )
        self.assertTrue(result.has_recommendation)
        self.assertTrue(result.is_fallback)
        self.assertEqual(result.fallback_gap_ghs, Decimal("7.00"))

    def test_home_page_loads(self):
        response = self.client.get(reverse('recommender:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What Should I Eat for Breakfast?")

    def test_recommend_view_post(self):
        response = self.client.post(reverse('recommender:recommend'), {
            'budget_ghs': '45',
            'max_time_minutes': '30',
            'servings': '1',
            'flavor_preference': 'ALL'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ablemamu")

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recommender:recipe_detail', kwargs={'slug': self.r1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.r1.title)
        self.assertContains(response, "Ingredients Checklist")
        self.assertContains(response, "Preparation & Cooking Steps")

    def test_all_recipes_view(self):
        response = self.client.get(reverse('recommender:all_recipes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All Ghanaian Breakfast Recipes")
