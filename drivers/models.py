from django.db import models
from django.conf import settings
from packages.models import Package


class ProofOfDelivery(models.Model):
    """Proof of delivery with photo and signature"""
    package = models.OneToOneField(Package, on_delete=models.CASCADE, related_name='proof_of_delivery')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deliveries')
    
    recipient_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='delivery_photos/', null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)
    notes = models.TextField(blank=True)
    
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    delivered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Proofs of delivery'
    
    def __str__(self):
        return f"POD for {self.package.tracking_number}"
