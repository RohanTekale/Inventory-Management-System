import pytest
from  django.test import TestCase
from inventory.models import Warehouse, Product
from django.contrib.auth.models import User, Group


@pytest.mark.django_db
class TestWarehouseModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin_group = Group.objects.create(name= 'Admin')
        self.user.groups.add(self.admin_group)
        self.warehouse = Warehouse.objects.create(name='Test Warehouse', location="Pune")
        self.product = Product.objects.create(name='Test Product', sku="TST123", quantity=10,warehouse=self.warehouse,price=999.99)

    def test_warehouse_str(self):
        assert str(self.warehouse) == "Test Warehouse"

    def test_product_str(self):
        assert str(self.product) == "Test Product"