from django.urls import path
from accounts.views import (
    account_view,
    edit_account_view,
    edit_recipe_collection_view
)

app_name = "accounts"

urlpatterns = [
    path('<user_id>/', account_view, name="view"),
    path('<user_id>/edit/', edit_account_view, name="edit"),
    path('update/<pk>/', edit_recipe_collection_view, name="edit-recipe")
]