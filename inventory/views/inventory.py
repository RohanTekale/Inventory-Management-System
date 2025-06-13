from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from inventory.models import Warehouse, Product
from inventory.serializers import WarehouseSerializer, ProductSerializer
from inventory.permissions import InventoryPermission


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [InventoryPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'location']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [InventoryPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sku', 'warehouse', 'quantity']
    ordering_fields = ['price','quantity']