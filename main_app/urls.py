from django.urls import path
from .views import (
    recipe_search,
    home_screen_view,
    summer_2022_view,
    RecipeDetail,
)

app_name = "main_app"

urlpatterns = [
    path('', home_screen_view, name='about'),
    path('recipes/', recipe_search, name='recipes'),
    path('summer2022/', summer_2022_view, name='summer'),
    path('recipes/<pk>/', RecipeDetail.as_view(), name='recipe-detail'),
]
