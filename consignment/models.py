from django.db import models
from django.core.cache import cache
from django.core.validators import MinValueValidator, MaxValueValidator


class SiteSettings(models.Model):
    """Singleton model for site-wide settings including pricing.
    Admin can edit these values from the admin panel."""
    
    # Pricing - Base rates by delivery speed
    price_standard = models.DecimalField(
        max_digits=6, decimal_places=2, default=3.49,
        help_text="Standard delivery base price (2-3 days)"
    )
    price_next_day = models.DecimalField(
        max_digits=6, decimal_places=2, default=5.99,
        help_text="Next day delivery base price"
    )
    price_same_day = models.DecimalField(
        max_digits=6, decimal_places=2, default=12.99,
        help_text="Same day delivery base price"
    )
    
    # Weight tier pricing (per weight bracket)
    price_weight_1kg = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, help_text="Additional cost for 0-1kg")
    price_weight_5kg = models.DecimalField(max_digits=6, decimal_places=2, default=1.00, help_text="Additional cost for 1-5kg")
    price_weight_10kg = models.DecimalField(max_digits=6, decimal_places=2, default=2.50, help_text="Additional cost for 5-10kg")
    price_weight_20kg = models.DecimalField(max_digits=6, decimal_places=2, default=4.50, help_text="Additional cost for 10-20kg")
    price_weight_30kg = models.DecimalField(max_digits=6, decimal_places=2, default=6.00, help_text="Additional cost for 20-30kg")
    price_weight_50kg = models.DecimalField(max_digits=6, decimal_places=2, default=11.50, help_text="Additional cost for 30-50kg")
    
    # Add-on services
    price_insurance = models.DecimalField(max_digits=6, decimal_places=2, default=2.99, help_text="Additional insurance")
    price_signature = models.DecimalField(max_digits=6, decimal_places=2, default=1.50, help_text="Signature required")
    price_photo_proof = models.DecimalField(max_digits=6, decimal_places=2, default=3.99, help_text="Photo proof of delivery")
    price_saturday = models.DecimalField(max_digits=6, decimal_places=2, default=4.99, help_text="Saturday delivery")
    
    # Coverage amounts
    coverage_standard = models.DecimalField(max_digits=8, decimal_places=2, default=50.00, help_text="Standard coverage amount (£)")
    coverage_next_day = models.DecimalField(max_digits=8, decimal_places=2, default=100.00, help_text="Next day coverage amount (£)")
    
    # ===== MAP CUSTOMIZATION SETTINGS =====
    # Route line colors (hex)
    map_route_traveled_color = models.CharField(
        max_length=7, default='#3b82f6',
        help_text="Color for traveled route line (hex, e.g. #3b82f6 = blue)"
    )
    map_route_remaining_color = models.CharField(
        max_length=7, default='#ef4444',
        help_text="Color for remaining route line (hex, e.g. #ef4444 = red)"
    )
    
    # Route line thickness
    map_route_traveled_width = models.PositiveIntegerField(
        default=6, validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Width of traveled route line (1-20 pixels)"
    )
    map_route_remaining_width = models.PositiveIntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Width of remaining route line (1-20 pixels)"
    )
    
    # Marker sizes
    map_marker_truck_size = models.PositiveIntegerField(
        default=60, validators=[MinValueValidator(30), MaxValueValidator(100)],
        help_text="Truck marker size (30-100 pixels)"
    )
    map_marker_waypoint_size = models.PositiveIntegerField(
        default=6, validators=[MinValueValidator(3), MaxValueValidator(15)],
        help_text="Waypoint dot size (3-15 pixels)"
    )
    map_marker_passed_size = models.PositiveIntegerField(
        default=6, validators=[MinValueValidator(3), MaxValueValidator(15)],
        help_text="Passed checkpoint dot size (3-15 pixels)"
    )
    
    # Marker colors
    map_marker_passed_color = models.CharField(
        max_length=7, default='#22c55e',
        help_text="Color for passed waypoint dots (hex, e.g. #22c55e = green)"
    )
    map_marker_upcoming_color = models.CharField(
        max_length=7, default='#ef4444',
        help_text="Color for upcoming waypoint dots (hex, e.g. #ef4444 = red)"
    )
    map_marker_truck_color = models.CharField(
        max_length=7, default='#dc2626',
        help_text="Truck marker background color (hex)"
    )
    
    # Opacity/brightness (0.1 to 1.0)
    map_route_opacity = models.DecimalField(
        max_digits=2, decimal_places=1, default=1.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(1.0)],
        help_text="Route line opacity (0.1 = faint, 1.0 = full brightness)"
    )
    map_marker_opacity = models.DecimalField(
        max_digits=2, decimal_places=1, default=1.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(1.0)],
        help_text="Marker opacity (0.1 = faint, 1.0 = full brightness)"
    )
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton)
        self.pk = 1
        super().save(*args, **kwargs)
        # Clear cache when settings change
        cache.delete('site_settings')
    
    @classmethod
    def get_settings(cls):
        """Get or create site settings with caching."""
        settings = cache.get('site_settings')
        if settings is None:
            settings, _ = cls.objects.get_or_create(pk=1)
            cache.set('site_settings', settings, 300)  # Cache for 5 minutes
        return settings
    
    def __str__(self):
        return "Site Settings"
