from django.contrib import admin
from django.utils import timezone


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
