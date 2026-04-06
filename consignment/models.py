from django.db import models
from django.core.cache import cache


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
