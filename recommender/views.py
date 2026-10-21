from decimal import Decimal, InvalidOperation
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from .models import Recipe, DietaryTag
from .services import BreakfastRecommender


def home_view(request: HttpRequest) -> HttpResponse:
    """Homepage featuring the interactive breakfast recommendation input form."""
    dietary_tags = DietaryTag.objects.all()
    flavor_choices = Recipe.FlavorProfile.choices
    tradition_choices = Recipe.TraditionType.choices
    recent_recipes = Recipe.objects.filter(is_active=True).order_by('cost_per_serving_ghs')[:3]

    context = {
        'dietary_tags': dietary_tags,
        'flavor_choices': flavor_choices,
        'tradition_choices': tradition_choices,
        'recent_recipes': recent_recipes,
        'total_recipes_count': Recipe.objects.filter(is_active=True).count(),
    }
    return render(request, 'recommender/home.html', context)


def recommend_view(request: HttpRequest) -> HttpResponse:
    """Handles recommendation calculation based on budget, time, and food preferences."""
    # Support both GET and POST for shareable recommendation queries
    data = request.POST if request.method == 'POST' else request.GET

    raw_budget = data.get('budget_ghs', '').strip()
    try:
        budget_ghs = Decimal(raw_budget)
        if budget_ghs <= 0:
            budget_ghs = Decimal('40.00')
    except (InvalidOperation, ValueError, TypeError):
        budget_ghs = Decimal('40.00')

    raw_time = data.get('max_time_minutes', '').strip()
    try:
        max_time_minutes = int(raw_time) if raw_time and int(raw_time) > 0 else None
    except ValueError:
        max_time_minutes = None

    raw_servings = data.get('servings', '1').strip()
    try:
        servings = int(raw_servings) if raw_servings and int(raw_servings) > 0 else 1
    except ValueError:
        servings = 1

    flavor_preference = data.get('flavor_preference', 'ALL').strip()
    tradition_type = data.get('tradition_type', 'ALL').strip()
    
    # Retrieve multiple dietary tags
    if request.method == 'POST':
        dietary_slugs = request.POST.getlist('dietary_tags')
    else:
        dietary_slugs = request.GET.getlist('dietary_tags')

    result = BreakfastRecommender.recommend(
        budget_ghs=budget_ghs,
        max_time_minutes=max_time_minutes,
        servings=servings,
        flavor_preference=flavor_preference if flavor_preference != 'ALL' else None,
        dietary_slugs=dietary_slugs,
        tradition_type=tradition_type if tradition_type != 'ALL' else None
    )

    context = {
        'result': result,
        'user_budget_ghs': budget_ghs,
        'max_time_minutes': max_time_minutes,
        'servings': servings,
        'flavor_preference': flavor_preference,
        'tradition_type': tradition_type,
        'selected_dietary_slugs': dietary_slugs,
        'dietary_tags': DietaryTag.objects.all(),
    }

    if request.headers.get('HX-Request') or request.GET.get('partial') == '1' or request.POST.get('partial') == '1':
        return render(request, 'recommender/partials/results_partial.html', context)

    return render(request, 'recommender/results.html', context)


def recipe_detail_view(request: HttpRequest, slug: str) -> HttpResponse:
    """Detailed view for a single Ghanaian breakfast recipe with steps & ingredient checklist."""
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related(
            'dietary_tags',
            'ingredient_groups__ingredients',
            'steps'
        ),
        slug=slug,
        is_active=True
    )
    
    # Servings multiplier (defaults to default_servings or user param)
    servings_param = request.GET.get('servings')
    try:
        servings = int(servings_param) if servings_param and int(servings_param) > 0 else recipe.default_servings
    except ValueError:
        servings = recipe.default_servings

    total_cost_ghs = recipe.calculate_total_cost(servings)

    # Similar recommendations
    related_recipes = Recipe.objects.filter(
        is_active=True
    ).exclude(id=recipe.id).order_by('?')[:2]

    context = {
        'recipe': recipe,
        'servings': servings,
        'total_cost_ghs': total_cost_ghs,
        'related_recipes': related_recipes,
    }
    return render(request, 'recommender/recipe_detail.html', context)


def all_recipes_view(request: HttpRequest) -> HttpResponse:
    """Browse all Ghanaian breakfast options with filters."""
    recipes = Recipe.objects.filter(is_active=True).prefetch_related('dietary_tags')
    
    # Optional sorting
    sort_by = request.GET.get('sort', 'cost_asc')
    if sort_by == 'cost_asc':
        recipes = recipes.order_by('cost_per_serving_ghs')
    elif sort_by == 'cost_desc':
        recipes = recipes.order_by('-cost_per_serving_ghs')
    elif sort_by == 'time_asc':
        recipes = recipes.order_by('total_time_minutes')
    else:
        recipes = recipes.order_by('title')

    context = {
        'recipes': recipes,
        'sort_by': sort_by,
        'total_count': recipes.count(),
        'dietary_tags': DietaryTag.objects.all(),
    }
    return render(request, 'recommender/all_recipes.html', context)
