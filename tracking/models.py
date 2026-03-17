from django.db import models
from packages.models import Package


class TrackingHistory(models.Model):
    """Track package location and status changes"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='tracking_history')
    status = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Tracking histories'
    
    def __str__(self):
        return f"{self.package.tracking_number} - {self.status} at {self.location}"
