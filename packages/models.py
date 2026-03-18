from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
import secrets
import string


def generate_tracking_number():
    """Generate unique tracking number like ECG-XXXXXXXX using cryptographic randomness."""
    alphabet = string.ascii_uppercase + string.digits
    chars = ''.join(secrets.choice(alphabet) for _ in range(8))
    return f"ECG-{chars}"


class Package(models.Model):
    """Main package/shipment model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    tracking_number = models.CharField(max_length=20, unique=True, default=generate_tracking_number)
    
    # Sender info
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_packages')
    sender_name = models.CharField(max_length=100)
    sender_address = models.TextField()
    sender_phone = models.CharField(max_length=20)
    sender_city = models.CharField(max_length=100)
    sender_postcode = models.CharField(max_length=20)
    
    # Receiver info
    receiver_name = models.CharField(max_length=100)
    receiver_address = models.TextField()
    receiver_phone = models.CharField(max_length=20)
    receiver_city = models.CharField(max_length=100)
    receiver_postcode = models.CharField(max_length=20)
    
    # Package details
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weight in kg",
                                  validators=[MinValueValidator(0.01)])
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                  validators=[MinValueValidator(0)])
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                  validators=[MinValueValidator(0)])
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                  validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    
    # Status and assignment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_packages'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['receiver_city']),
            models.Index(fields=['tracking_number']),
        ]
    
    def __str__(self):
        return f"{self.tracking_number} - {self.receiver_name}"
    
    def get_latest_location(self):
        latest = self.tracking_history.order_by('-timestamp').first()
        return latest if latest else None
