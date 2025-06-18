import pytest
from django.test import TestCase
from inventory.models import PurchaseOrder, Product, Warehouse
from inventory.tasks import process_purchase_order

@pytest.mark.django_db
class TestOrders(TestCase):
    def setUp(self):
        self.warehouse = Warehouse.objects.create(name='Test Warehouse',location="Pune")
        self.product = Product.objects.create(name="Laptop", sku="LAP123", quantity=10, warehouse=self.warehouse, price=999.99)
        self.order = PurchaseOrder.objects.create(order_number="PO123", product=self.product, quantity=5, status="PENDING")

    def test_order_processing(self):
        self.order.status = "APPROVED"
        self.order.save()
        process_purchase_order(self.order.id)
        self.product.refresh_from_db()
        self.order.refresh_from_db()
        assert self.product.quantity == 15
        assert self.order.status == "COMPLETED"