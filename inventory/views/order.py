from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from inventory.models import PurchaseOrder, StockTransfer
from inventory.serializers import PurchaseOrderSerializer, StockTransferSerializer
from inventory.permissions import OrderPermission
from inventory.tasks import process_purchase_order

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [OrderPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order_number', 'status']
    search_fields = ['order_number']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        instance = serializer.save()
        process_purchase_order.delay(instance.id)

class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    permission_classes = [OrderPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['transfer_number', 'from_warehouse', 'to_warehouse']