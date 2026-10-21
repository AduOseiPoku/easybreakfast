from django.urls import path
from . import views

app_name = 'recommender'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('recommend/', views.recommend_view, name='recommend'),
    path('recipes/', views.all_recipes_view, name='all_recipes'),
    path('recipe/<slug:slug>/', views.recipe_detail_view, name='recipe_detail'),
]
