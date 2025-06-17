from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50,db_index=True)
    quantity = models.PositiveIntegerField(default=0)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['sku', 'warehouse']),
        ]