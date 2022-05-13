from django.urls import path
from test_kitchen.views import (
    test_kitchen_list,
    test_kitchen_create
)

app_name = "test_kitchen"

urlpatterns = [
    path('', test_kitchen_list, name='list'),
    path('create/', test_kitchen_create, name='create'),

]
