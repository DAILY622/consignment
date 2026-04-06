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
        ordering = ['-timestamp', '-id']
        verbose_name_plural = 'Tracking histories'
        indexes = [
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.package.tracking_number} - {self.status} at {self.location}"


class RouteWaypoint(models.Model):
    """Admin-editable waypoints for package routes.
    These define the stops the truck will pass through on the map."""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='route_waypoints')
    city_name = models.CharField(max_length=100, help_text="City/location name shown on map")
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    order = models.PositiveIntegerField(default=0, help_text="Order in the route (0 = first stop)")
    is_passed = models.BooleanField(default=False, help_text="Has the truck passed this waypoint?")
    notes = models.CharField(max_length=200, blank=True, help_text="Optional notes for this stop")
    
    class Meta:
        ordering = ['package', 'order']
        verbose_name = 'Route Waypoint'
        verbose_name_plural = 'Route Waypoints'
        unique_together = ['package', 'order']
    
    def __str__(self):
        status = "✓" if self.is_passed else "○"
        return f"{status} {self.city_name} (Stop #{self.order})"
