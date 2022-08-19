from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import (
    recipe_search,
    home_screen_view,
    summer_2022_view,
    RecipeDetail,
)

from products.views import (
    stripe_webhook
)

app_name = "main_app"

urlpatterns = [
    path('', home_screen_view, name='about'),
    path('recipes/', recipe_search, name='recipes'),
    path('summer2022/', summer_2022_view, name='summer'),
    path('recipes/<pk>/', RecipeDetail.as_view(), name='recipe-detail'),
    path('webhook/', stripe_webhook, name="stripe-webhook"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)