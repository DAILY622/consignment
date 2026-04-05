from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
import secrets
import string


def generate_tracking_number():
    """Generate unique tracking number like DFX-XXXXXXXX using cryptographic randomness."""
    alphabet = string.ascii_uppercase + string.digits
    chars = ''.join(secrets.choice(alphabet) for _ in range(8))
    return f"DFX-{chars}"


# Global city coordinates for international shipping
GLOBAL_CITY_COORDS = {
    # Norway
    'Oslo': [59.9139, 10.7522], 'Bergen': [60.3913, 5.3221], 'Trondheim': [63.4305, 10.3951],
    'Stavanger': [58.9700, 5.7331], 'Kristiansand': [58.1599, 8.0182],
    # Pakistan
    'Karachi': [24.8607, 67.0011], 'Lahore': [31.5497, 74.3436], 'Islamabad': [33.6844, 73.0479],
    'Rawalpindi': [33.5651, 73.0169], 'Faisalabad': [31.4504, 73.1350], 'Peshawar': [34.0151, 71.5249],
    # UK
    'London': [51.5074, -0.1278], 'Manchester': [53.4808, -2.2426], 'Birmingham': [52.4862, -1.8904],
    'Leeds': [53.8008, -1.5491], 'Glasgow': [55.8642, -4.2518], 'Edinburgh': [55.9533, -3.1883],
    'Liverpool': [53.4084, -2.9916], 'Bristol': [51.4545, -2.5879], 'Cardiff': [51.4816, -3.1791],
    # Europe
    'Paris': [48.8566, 2.3522], 'Berlin': [52.5200, 13.4050], 'Amsterdam': [52.3676, 4.9041],
    'Brussels': [50.8503, 4.3517], 'Madrid': [40.4168, -3.7038], 'Rome': [41.9028, 12.4964],
    'Vienna': [48.2082, 16.3738], 'Prague': [50.0755, 14.4378], 'Warsaw': [52.2297, 21.0122],
    'Stockholm': [59.3293, 18.0686], 'Copenhagen': [55.6761, 12.5683], 'Helsinki': [60.1699, 24.9384],
    # Americas
    'New York': [40.7128, -74.0060], 'Los Angeles': [34.0522, -118.2437], 'Chicago': [41.8781, -87.6298],
    'Toronto': [43.6532, -79.3832], 'Vancouver': [49.2827, -123.1207], 'Mexico City': [19.4326, -99.1332],
    # Asia
    'Dubai': [25.2048, 55.2708], 'Singapore': [1.3521, 103.8198], 'Hong Kong': [22.3193, 114.1694],
    'Tokyo': [35.6762, 139.6503], 'Seoul': [37.5665, 126.9780], 'Mumbai': [19.0760, 72.8777],
    'Delhi': [28.7041, 77.1025], 'Bangkok': [13.7563, 100.5018], 'Jakarta': [-6.2088, 106.8456],
    # Australia/Oceania
    'Sydney': [-33.8688, 151.2093], 'Melbourne': [-37.8136, 144.9631], 'Auckland': [-36.8485, 174.7633],
    # Africa
    'Cairo': [30.0444, 31.2357], 'Lagos': [6.5244, 3.3792], 'Johannesburg': [-26.2041, 28.0473],
    'Nairobi': [-1.2921, 36.8219], 'Cape Town': [-33.9249, 18.4241],
}


class Package(models.Model):
    """Main package/shipment model - supports international shipping"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    tracking_number = models.CharField(max_length=20, unique=True, default=generate_tracking_number)
    
    # Sender info (international)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_packages')
    sender_name = models.CharField(max_length=100)
    sender_address = models.TextField()
    sender_phone = models.CharField(max_length=20)
    sender_city = models.CharField(max_length=100)
    sender_country = models.CharField(max_length=100, default='United Kingdom')
    sender_postcode = models.CharField(max_length=20)
    
    # Receiver info (international)
    receiver_name = models.CharField(max_length=100)
    receiver_address = models.TextField()
    receiver_phone = models.CharField(max_length=20)
    receiver_city = models.CharField(max_length=100)
    receiver_country = models.CharField(max_length=100, default='United Kingdom')
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
