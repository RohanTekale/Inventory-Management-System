from celery import shared_task
from inventory.models import PurchaseOrder, Product
from django.core.mail import send_mail
from django.db import models

@shared_task
def process_purchase_order(order_id):
    order = PurchaseOrder.objects.get(id=order_id)
    product = order.product
    if order.status == "APPROVED":
        product.quantity += order.quantity
        product.save()
        order.status = "COMPLETED"
        order.save()

@shared_task
def check_low_stock():
    low_stock_products = Product.objects.filter(quantity__lte=models.F('reorder_level'))
    for product in low_stock_products:
        send_mail(
            'Low Stock Alert',
               f'Product {product.name} (SKU: {product.sku}) is low on stock: {product.quantity} units.',
               'tekalerohan7@gmail.com',
               ['tekalerohan2000@gmail.com'],
               fail_silently=True,
        )