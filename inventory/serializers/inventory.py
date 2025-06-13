from rest_framework import serializers
from inventory.models import Warehouse,Product


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id','name','location','created_at']

class ProductSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),write_only=True, source= 'warehouse'
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'quantity', 'warehouse', 'warehouse_id', 'price', 'reorder_level', 'created_at']