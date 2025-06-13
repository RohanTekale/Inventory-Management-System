from rest_framework import serializers
from inventory.models import PurchaseOrder, StockTransfer, Product, Warehouse
from .inventory import ProductSerializer

class PurchaseOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),write_only =True, source='product'
    )

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'order_number', 'product', 'product_id', 'quantity', 'status', 'created_at', 'updated_at']


class StockTransferSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),write_only =True, source='product'
    )
    from_warehouse = serializers.PrimaryKeyRelatedField(
        queryset = Warehouse.objects.all(), write_only = True
    )
    to_warehouse = serializers.PrimaryKeyRelatedField(
        queryset = Warehouse.objects.all(), write_only = True
    )

    class Meta:
        model = StockTransfer
        fields = ['id', 'transfer_number', 'from_warehouse', 'to_warehouse', 'product', 'product_id', 'quantity', 'created_at']