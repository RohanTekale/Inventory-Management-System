from django.urls import path
from rest_framework.routers import DefaultRouter
from inventory.views import PurchaseOrderViewSet, StockTransferViewSet
from inventory.views.analytics import AnalyticsView


router = DefaultRouter()
router.register(r'purchase-orders', PurchaseOrderViewSet, basename='purchase-orders')
router.register(r'stock-transfers', StockTransferViewSet, basename='stock-transfers')


urlpatterns = [
    path('analytics/', AnalyticsView.as_view(), name='analytics'),

] + router.urls


