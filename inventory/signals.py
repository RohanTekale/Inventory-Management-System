from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from inventory.models import AuditLog, Warehouse, Product, PurchaseOrder, StockTransfer
from django.contrib.auth.models import User

@receiver(post_save, sender=Warehouse)
@receiver(post_save, sender=Product)
@receiver(post_save, sender=PurchaseOrder)
@receiver(post_save, sender=StockTransfer)
def log_save(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    AuditLog.objects.create(
        user=instance._request_user if hasattr(instance, '_request_user') else None,
        action=action,
        model_name=sender.__name__,
        object_id=str(instance.id),
        details={'data': str(instance.__dict__)}
    )

@receiver(post_delete, sender=Warehouse)
@receiver(post_delete, sender=Product)
@receiver(post_delete, sender=PurchaseOrder)
@receiver(post_delete, sender=StockTransfer)
def log_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        user=instance._request_user if hasattr(instance, '_request_user') else None,
        action='DELETE',
        model_name=sender.__name__,
        object_id=str(instance.id),
        details={'data': str(instance.__dict__)}
    )