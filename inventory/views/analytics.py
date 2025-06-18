from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F
from inventory.models import Product, PurchaseOrder
from inventory.permissions import InventoryPermission
from django.db import models

class AnalyticsView(APIView):
    permission_classes = [InventoryPermission]

    def get(self, request):
        total_products = Product.objects.count()
        low_stock = Product.objects.filter(quantity__lte=models.F('reorder_level')).count()
        total_orders = PurchaseOrder.objects.count()
        pending_orders = PurchaseOrder.objects.filter(status='PENDING').count()

        data = {
            'total_products': total_products,
            'low_stock': low_stock,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
        }
        return Response(data, status=status.HTTP_200_OK)


