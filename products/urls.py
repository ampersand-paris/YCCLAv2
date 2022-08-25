from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import (
    CollectionsView,
    success_view,
    cancel_view,
    CreateCheckoutSessionView,
    # stripe_webhook
)

app_name = "main_app"

urlpatterns = [
    path('success/', success_view, name='success'),
    path('', CollectionsView.as_view(), name='collections'),
    path('cancel/', cancel_view, name='cancel'),
    path('create-checkout-session/<pk>', CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)