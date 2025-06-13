from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    details = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} {self.action} {self.model_name} {self.object_id}"
    
    class Meta:
        indexes = [
            models.Index(fields=['timestamp','user']),
        ]