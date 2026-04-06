from django.contrib import admin
from django.utils import timezone
from .models import SiteSettings


class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin configuration for site-wide settings (singleton)."""
    
    list_display = ('__str__', 'price_standard', 'price_next_day', 'price_same_day', 'updated_at')
    
    fieldsets = (
        ('💰 Base Delivery Prices', {
            'fields': (('price_standard', 'price_next_day', 'price_same_day'),),
            'description': 'Base prices for each delivery speed tier'
        }),
        ('⚖️ Weight Surcharges', {
            'fields': (
                ('price_weight_1kg', 'price_weight_5kg', 'price_weight_10kg'),
                ('price_weight_20kg', 'price_weight_30kg', 'price_weight_50kg'),
            ),
            'classes': ('collapse',),
            'description': 'Additional charges based on package weight brackets'
        }),
        ('✨ Add-on Services', {
            'fields': (('price_insurance', 'price_signature'), ('price_photo_proof', 'price_saturday')),
            'classes': ('collapse',),
        }),
        ('🛡️ Coverage Amounts', {
            'fields': (('coverage_standard', 'coverage_next_day'),),
            'classes': ('collapse',),
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance (singleton)
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of settings
        return False


class ConsignmentAdminSite(admin.AdminSite):
    site_header = '🚚 DailyFX Delivery Logistics'
    site_title = 'DailyFX Delivery Delivery'
    index_title = 'Dashboard'
    
    def index(self, request, extra_context=None):
        from packages.models import Package
        from accounts.models import User
        
        today = timezone.now().date()
        
        extra_context = extra_context or {}
        extra_context['total_packages'] = Package.objects.count()
        extra_context['pending'] = Package.objects.filter(status='pending').count()
        extra_context['processing'] = Package.objects.filter(status='processing').count()
        extra_context['in_transit'] = Package.objects.filter(status='in_transit').count()
        extra_context['out_for_delivery'] = Package.objects.filter(status='out_for_delivery').count()
        extra_context['delivered_today'] = Package.objects.filter(status='delivered', updated_at__date=today).count()
        extra_context['delivered_all'] = Package.objects.filter(status='delivered').count()
        extra_context['total_users'] = User.objects.count()
        extra_context['total_drivers'] = User.objects.filter(role='driver').count()
        extra_context['recent_packages'] = Package.objects.all()[:10]
        extra_context['active_packages'] = Package.objects.exclude(status__in=['delivered', 'cancelled'])[:20]
        
        return super().index(request, extra_context)


# Create custom admin site instance
admin_site = ConsignmentAdminSite(name='admin')

# Register SiteSettings with the custom admin site
admin_site.register(SiteSettings, SiteSettingsAdmin)
