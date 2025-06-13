from django.urls import path, include

urlpatterns = [
    path('', include('inventory.urls.inventory')),
    path('', include('inventory.urls.order')),
]