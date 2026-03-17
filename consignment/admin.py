from django.contrib.admin import AdminSite
from django.utils import timezone
from datetime import timedelta


class ConsignmentAdminSite(AdminSite):
    site_header = '🚚 E-Cognite Admin'
    site_title = 'E-Cognite Delivery'
    index_title = 'Dashboard'
    
    def index(self, request, extra_context=None):
        from packages.models import Package
        
        today = timezone.now().date()
        
        extra_context = extra_context or {}
        extra_context['total_packages'] = Package.objects.count()
        extra_context['pending'] = Package.objects.filter(status='pending').count()
        extra_context['processing'] = Package.objects.filter(status='processing').count()
        extra_context['in_transit'] = Package.objects.filter(status='in_transit').count()
        extra_context['out_for_delivery'] = Package.objects.filter(status='out_for_delivery').count()
        extra_context['delivered_today'] = Package.objects.filter(status='delivered', updated_at__date=today).count()
        extra_context['delivered_all'] = Package.objects.filter(status='delivered').count()
        extra_context['recent_packages'] = Package.objects.all()[:10]
        extra_context['active_packages'] = Package.objects.exclude(status__in=['delivered', 'cancelled'])[:20]
        
        return super().index(request, extra_context)


admin_site = ConsignmentAdminSite(name='admin')
