from decimal import Decimal
from typing import List, Optional, Dict, Any
from django.db.models import QuerySet
from .models import Recipe, DietaryTag


class RecommendationResult:
    def __init__(
        self,
        top_recipe: Optional[Recipe] = None,
        top_score: float = 0.0,
        top_reason: str = "",
        alternates: List[Dict[str, Any]] = None,
        is_fallback: bool = False,
        fallback_gap_ghs: Decimal = Decimal('0.00'),
        user_budget_ghs: Decimal = Decimal('0.00'),
        servings: int = 1,
        total_matches_count: int = 0
    ):
        self.top_recipe = top_recipe
        self.top_score = top_score
        self.top_reason = top_reason
        self.alternates = alternates or []
        self.is_fallback = is_fallback
        self.fallback_gap_ghs = fallback_gap_ghs
        self.user_budget_ghs = user_budget_ghs
        self.servings = servings
        self.total_matches_count = total_matches_count

    @property
    def has_recommendation(self) -> bool:
        return self.top_recipe is not None

    @property
    def top_total_cost(self) -> Decimal:
        if self.top_recipe:
            return self.top_recipe.calculate_total_cost(self.servings)
        return Decimal('0.00')

    @property
    def top_surplus_ghs(self) -> Decimal:
        if self.top_recipe:
            return max(Decimal('0.00'), self.user_budget_ghs - self.top_total_cost)
        return Decimal('0.00')

    @property
    def budget_utilization_percent(self) -> int:
        if self.user_budget_ghs and self.user_budget_ghs > 0 and self.top_recipe:
            pct = int((self.top_total_cost / self.user_budget_ghs) * 100)
            return min(100, max(0, pct))
        return 0

    @property
    def budget_surplus_percent(self) -> int:
        if self.user_budget_ghs and self.user_budget_ghs > 0:
            return max(0, 100 - self.budget_utilization_percent)
        return 0


class BreakfastRecommender:
    """
    Multi-Criteria Decision Engine for Ghanaian Breakfast recommendations.
    Scores candidates deterministically based on:
      1. Exact numeric budget in Ghana Cedis (GH₵) (40 pts max)
      2. Available preparation time (30 pts max)
      3. Flavor / Craving preference (20 pts max)
      4. Cultural & Dietary alignment (10 pts max)
    """

    @classmethod
    def recommend(
        cls,
        budget_ghs: Decimal,
        max_time_minutes: Optional[int] = None,
        servings: int = 1,
        flavor_preference: Optional[str] = None,
        dietary_slugs: Optional[List[str]] = None,
        tradition_type: Optional[str] = None,
    ) -> RecommendationResult:
        if servings < 1:
            servings = 1

        queryset = Recipe.objects.filter(is_active=True).prefetch_related(
            'dietary_tags',
            'ingredient_groups__ingredients',
            'steps'
        )

        # Apply strict dietary filters if provided
        if dietary_slugs:
            for tag_slug in dietary_slugs:
                if tag_slug.strip():
                    queryset = queryset.filter(dietary_tags__slug=tag_slug.strip())

        recipes = list(queryset)

        if not recipes:
            # If dietary tag filtered out everything, fetch all active recipes for fallback
            recipes = list(Recipe.objects.filter(is_active=True).prefetch_related('dietary_tags'))

        # Check affordability
        affordable_candidates = [
            r for r in recipes
            if r.calculate_total_cost(servings) <= budget_ghs
        ]

        # Handle case where budget is lower than any available option
        if not affordable_candidates and recipes:
            # Sort by total cost ascending to find closest affordable option
            recipes.sort(key=lambda r: r.calculate_total_cost(servings))
            closest_recipe = recipes[0]
            closest_cost = closest_recipe.calculate_total_cost(servings)
            gap = closest_cost - budget_ghs

            reason = (
                f"Your budget of GH₵ {budget_ghs:.2f} is slightly under our most affordable breakfast, "
                f"but '{closest_recipe.title}' is just GH₵ {gap:.2f} away at GH₵ {closest_cost:.2f}. "
                f"It is a hearty, beloved Ghanaian morning classic!"
            )

            # Alternate runner-ups
            alternates = []
            for alt in recipes[1:4]:
                alt_cost = alt.calculate_total_cost(servings)
                alternates.append({
                    'recipe': alt,
                    'score': 70.0,
                    'cost_ghs': alt_cost,
                    'surplus_ghs': Decimal('0.00'),
                    'gap_ghs': alt_cost - budget_ghs,
                    'reason': f"Costs GH₵ {alt_cost:.2f} (GH₵ {alt_cost - budget_ghs:.2f} above target)."
                })

            return RecommendationResult(
                top_recipe=closest_recipe,
                top_score=75.0,
                top_reason=reason,
                alternates=alternates,
                is_fallback=True,
                fallback_gap_ghs=gap,
                user_budget_ghs=budget_ghs,
                servings=servings,
                total_matches_count=0
            )

        # We have affordable candidates! Score them
        scored_candidates = []
        for recipe in affordable_candidates:
            score, reason = cls._score_recipe(
                recipe=recipe,
                budget_ghs=budget_ghs,
                max_time_minutes=max_time_minutes,
                servings=servings,
                flavor_preference=flavor_preference,
                tradition_type=tradition_type
            )
            cost = recipe.calculate_total_cost(servings)
            surplus = budget_ghs - cost
            scored_candidates.append({
                'recipe': recipe,
                'score': score,
                'cost_ghs': cost,
                'surplus_ghs': surplus,
                'gap_ghs': Decimal('0.00'),
                'reason': reason
            })

        # Sort by highest score first
        scored_candidates.sort(key=lambda x: x['score'], reverse=True)

        top_match = scored_candidates[0]
        alternates = scored_candidates[1:4]

        return RecommendationResult(
            top_recipe=top_match['recipe'],
            top_score=top_match['score'],
            top_reason=top_match['reason'],
            alternates=alternates,
            is_fallback=False,
            fallback_gap_ghs=Decimal('0.00'),
            user_budget_ghs=budget_ghs,
            servings=servings,
            total_matches_count=len(scored_candidates)
        )

    @classmethod
    def _score_recipe(
        cls,
        recipe: Recipe,
        budget_ghs: Decimal,
        max_time_minutes: Optional[int],
        servings: int,
        flavor_preference: Optional[str],
        tradition_type: Optional[str]
    ) -> tuple[float, str]:
        score = 0.0
        reasons = []

        total_cost = recipe.calculate_total_cost(servings)
        surplus = budget_ghs - total_cost

        # 1. Budget Score (up to 40 points)
        # Optimal utilization: Fits comfortably under budget, leaving sensible change
        if budget_ghs > Decimal('0.00'):
            ratio = float(total_cost / budget_ghs)
            # If it uses between 40% and 95% of budget, high efficiency
            if 0.35 <= ratio <= 0.95:
                budget_score = 40.0
                reasons.append(f"Comfortably fits within your GH₵ {budget_ghs:.2f} budget with GH₵ {surplus:.2f} to spare")
            elif ratio < 0.35:
                # Highly economical option!
                budget_score = 36.0
                reasons.append(f"Super budget-friendly: saves you GH₵ {surplus:.2f} from your GH₵ {budget_ghs:.2f} budget")
            else:
                # Close to 100% of budget
                budget_score = 34.0
                reasons.append(f"Maximizes your budget at GH₵ {total_cost:.2f}")
        else:
            budget_score = 30.0

        score += budget_score

        # 2. Time Score (up to 30 points)
        recipe_time = recipe.total_time_minutes
        if max_time_minutes is not None and max_time_minutes > 0:
            if recipe_time <= max_time_minutes:
                # Closer to max_time without exceeding it is efficient, but fast is always great
                time_efficiency = 1.0 - (max_time_minutes - recipe_time) / (max_time_minutes * 2)
                time_score = 30.0 * time_efficiency
                reasons.append(f"ready in {recipe_time} mins (within your {max_time_minutes} min window)")
            else:
                # Exceeds user time limit - penalize proportionally
                over_mins = recipe_time - max_time_minutes
                time_score = max(5.0, 30.0 - (over_mins * 1.5))
                reasons.append(f"takes {recipe_time} mins")
        else:
            time_score = 25.0
            reasons.append(f"ready in {recipe_time} mins")

        score += time_score

        # 3. Flavor / Craving Match (up to 20 points)
        if flavor_preference and flavor_preference != 'ALL':
            if recipe.flavor_profile == flavor_preference:
                flavor_score = 20.0
                reasons.append(f"delivers the {recipe.get_flavor_profile_display()} taste you crave")
            elif (
                (flavor_preference in ('SWEET_WARM', 'SAVORY_SPICED') and recipe.flavor_profile == 'SWEET_SAVORY') or
                (flavor_preference == 'SWEET_SAVORY' and recipe.flavor_profile in ('SWEET_WARM', 'SAVORY_SPICED'))
            ):
                flavor_score = 14.0
                reasons.append(f"complements your mood with {recipe.get_flavor_profile_display()} notes")
            else:
                flavor_score = 8.0
        else:
            flavor_score = 15.0

        score += flavor_score

        # 4. Heritage & Tradition alignment (up to 10 points)
        if tradition_type and tradition_type != 'ALL':
            if recipe.tradition_type == tradition_type:
                trad_score = 10.0
                if tradition_type == Recipe.TraditionType.SANKOFA:
                    reasons.append("honoring timeless Ghanaian breakfast heritage")
                else:
                    reasons.append("featuring an innovative Ghanaian diaspora twist")
            else:
                trad_score = 5.0
        else:
            trad_score = 8.0

        score += trad_score

        # Construct final polished explanation sentence
        summary_reason = "Recommended because it " + ", ".join(reasons) + "."
        return round(min(100.0, score), 1), summary_reason
