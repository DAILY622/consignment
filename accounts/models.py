from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User model with role support"""
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('user', 'Customer'),
        ('driver', 'Driver'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
    
    def is_driver(self):
        return self.role == 'driver'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
