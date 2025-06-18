from rest_framework import serializers
from inventory.models import PurchaseOrder, StockTransfer, Product, Warehouse
from .inventory import ProductSerializer

class PurchaseOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source='product'
    )

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'order_number', 'product', 'product_id', 'quantity', 'status', 'created_at', 'updated_at']

    def validate_order_number(self, value):
        if self.instance is None and PurchaseOrder.objects.filter(order_number=value).exists():
            raise serializers.ValidationError("Order number must be unique.")
        return value

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be positive."})
        if data.get('status') not in [choice[0] for choice in PurchaseOrder.STATUS_CHOICES]:
            raise serializers.ValidationError({"status": "Invalid status."})
        return data

class StockTransferSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source='product'
    )
    from_warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), write_only=True
    )
    to_warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), write_only=True
    )

    class Meta:
        model = StockTransfer
        fields = ['id', 'transfer_number', 'from_warehouse', 'to_warehouse', 'product', 'product_id', 'quantity', 'created_at']

    def validate_transfer_number(self, value):
        if self.instance is None and StockTransfer.objects.filter(transfer_number=value).exists():
            raise serializers.ValidationError("Transfer number must be unique.")
        return value

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be positive."})
        if data['from_warehouse'] == data['to_warehouse']:
            raise serializers.ValidationError("From and to warehouses cannot be the same.")
        product = data['product']
        from_warehouse = data['from_warehouse']
        try:
            product_instance = Product.objects.get(id=product.id, warehouse=from_warehouse)
            if product_instance.quantity < data['quantity']:
                raise serializers.ValidationError("Insufficient stock in from_warehouse.")
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found in from_warehouse.")
        return data