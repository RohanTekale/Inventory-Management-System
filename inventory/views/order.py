from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.db.models import F
from inventory.models import PurchaseOrder, StockTransfer, AuditLog, Product
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

    @action(detail=False, methods=['post'], url_path='bulk')
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic():
                orders = PurchaseOrder.objects.bulk_create([
                    PurchaseOrder(
                        order_number=item['order_number'],
                        product=item['product'],
                        quantity=item['quantity'],
                        status=item['status']
                    ) for item in serializer.validated_data
                ])
                if request.user.is_authenticated:
                    AuditLog.objects.bulk_create([
                        AuditLog(
                            user=request.user,
                            action='CREATE',
                            model_name='PurchaseOrder',
                            object_id=str(order.id),
                            details={'data': str(order.__dict__)}
                        ) for order in orders
                    ])
                for order in orders:
                    process_purchase_order.delay(order.id)
                serializer = self.get_serializer(orders, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    permission_classes = [OrderPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['transfer_number', 'from_warehouse', 'to_warehouse']

    @action(detail=False, methods=['post'], url_path='bulk')
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic():
                # First create StockTransfer entries
                transfers = StockTransfer.objects.bulk_create([
                    StockTransfer(
                        transfer_number=item['transfer_number'],
                        from_warehouse=item['from_warehouse'],
                        to_warehouse=item['to_warehouse'],
                        product=item['product'],
                        quantity=item['quantity']
                    ) for item in serializer.validated_data
                ])

                # Then handle product quantity adjustments
                for item in serializer.validated_data:
                    product = item['product']  # Product object
                    from_warehouse = item['from_warehouse']
                    to_warehouse = item['to_warehouse']
                    quantity = item['quantity']

                    # Decrease quantity in 'from_warehouse'
                    Product.objects.filter(
                        id=product.id,
                        warehouse=from_warehouse
                    ).update(quantity=F('quantity') - quantity)

                    # Check if same SKU exists in 'to_warehouse'
                    existing_product = Product.objects.filter(
                        sku=product.sku,
                        warehouse=to_warehouse
                    ).first()

                    if existing_product:
                        # Update existing product in 'to_warehouse'
                        Product.objects.filter(id=existing_product.id).update(
                            quantity=F('quantity') + quantity
                        )
                    else:
                        # Create new product entry for 'to_warehouse'
                        Product.objects.create(
                            name=product.name,
                            sku=product.sku,
                            price=product.price,
                            reorder_level=product.reorder_level,
                            quantity=quantity,
                            warehouse=to_warehouse
                        )

                # Log Audit if user authenticated
                if request.user.is_authenticated:
                    AuditLog.objects.bulk_create([
                        AuditLog(
                            user=request.user,
                            action='CREATE',
                            model_name='StockTransfer',
                            object_id=str(transfer.id),
                            details={'data': str(transfer.__dict__)}
                        ) for transfer in transfers
                    ])

                serializer = self.get_serializer(transfers, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
