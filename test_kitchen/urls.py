from django.urls import path

from test_kitchen.views import (
    test_kitchen_list,
    test_kitchen_create,
    edit_test_kitchen_view,
    TestKitchenDetail,
    test_kitchen_delete,
)

app_name = "test_kitchen"

urlpatterns = [
    path('', test_kitchen_list, name='list'),
    path('create/', test_kitchen_create, name='create'),
    path('<pk>/delete/', test_kitchen_delete, name="delete"),
    path('<pk>/', TestKitchenDetail.as_view(), name='post-detail'),
    path('<pk>/update/', edit_test_kitchen_view, name='edit'),
]
