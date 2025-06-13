from django.db import models
from .inventory import Product, Warehouse

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=50, unique=True, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_orders')
    qunatity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.order_number
    
    class Meta:
        indexes = [
            models.Index(fields=['order_number','status']),
        ]

class StockTransfer(models.Model):
    transfer_number = models.CharField(max_length=50, unique=True, db_index=True)
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='outgoing_transfers')
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='incoming_transfers')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transfers')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.transfer_number