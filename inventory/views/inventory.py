from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from inventory.models import Warehouse, Product, AuditLog
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
    ordering_fields = ['price', 'quantity']

    @action(detail=False, methods=['post'], url_path='bulk')
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic():
                # Use bulk_create for efficiency
                products = Product.objects.bulk_create([
                    Product(
                        name=item['name'],
                        sku=item['sku'],
                        quantity=item['quantity'],
                        warehouse=item['warehouse'],
                        price=item['price'],
                        reorder_level=item['reorder_level']
                    ) for item in serializer.validated_data
                ])
                # Manually create AuditLog entries
                if request.user.is_authenticated:
                    AuditLog.objects.bulk_create([
                        AuditLog(
                            user=request.user,
                            action='CREATE',
                            model_name='Product',
                            object_id=str(product.id),
                            details={'data': str(product.__dict__)}
                        ) for product in products
                    ])
                # Re-fetch for response to include serialized data
                serializer = self.get_serializer(products, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)