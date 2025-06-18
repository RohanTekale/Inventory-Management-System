from django.urls import path
from inventory.views.user import UserCreateView



urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user-create'),
]

