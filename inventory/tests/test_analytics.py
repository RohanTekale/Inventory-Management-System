import pytest
from django.test import TestCase, Client
from django.urls import reverse
from inventory.models import Product, Warehouse
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
class TestAnalytics(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.manager_group = Group.objects.create(name='Manager')
        self.user.groups.add(self.manager_group)
        
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        
        self.warehouse = Warehouse.objects.create(name="Main Warehouse", location="New York")
        Product.objects.create(
            name="Laptop", sku="LAP123", quantity=5, warehouse=self.warehouse, price=999.99, reorder_level=10
        )

    def test_analytics_view(self):
        # Set the Authorization header with the JWT token
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'

        # Optionally use reverse() if URL name is known
        response = self.client.get('/api/v1/analytics/')
        assert response.status_code == 200
        assert response.json()['low_stock'] == 1
