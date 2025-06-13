from django.urls import path
from rest_framework.routers import DefaultRouter
from inventory.views.inventory import WarehouseViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'products', ProductViewSet, basename='product')


urlpatterns = router.urls