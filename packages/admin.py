from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.html import format_html
from django.utils import timezone
from consignment.admin import admin_site
from .models import Package
from tracking.models import TrackingHistory, RouteWaypoint


class TrackingHistoryInline(admin.TabularInline):
    model = TrackingHistory
    extra = 0
    readonly_fields = ('timestamp',)
    fields = ('status', 'location', 'latitude', 'longitude', 'notes', 'timestamp')
    classes = ('collapse',)
    verbose_name = "Tracking Update"
    verbose_name_plural = "📍 Tracking History"


class RouteWaypointInline(admin.TabularInline):
    """Inline for editing the truck's route waypoints"""
    model = RouteWaypoint
    extra = 1
    fields = ('order', 'city_name', 'latitude', 'longitude', 'is_passed', 'notes')
    ordering = ['order']
    verbose_name = "Route Waypoint"
    verbose_name_plural = "🗺️ Route Waypoints (Define where truck passes through)"


@admin.register(Package, site=admin_site)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('tracking_link', 'sender_info', 'receiver_info', 'status_badge', 'driver_info', 'location_btn', 'created_date')
    list_filter = ('status', 'created_at', 'sender_city', 'receiver_city', 'assigned_driver')
    search_fields = ('tracking_number', 'sender__username', 'receiver_name', 'sender_name', 'receiver_city')
    readonly_fields = ('tracking_number', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_per_page = 25
    list_select_related = ('sender', 'assigned_driver')
    save_on_top = True
    
    inlines = [RouteWaypointInline, TrackingHistoryInline]
    
    fieldsets = (
        ('📦 Package Tracking', {
            'fields': ('tracking_number', 'status', 'assigned_driver', 'estimated_delivery'),
            'classes': ('wide',),
        }),
        ('📤 Sender Information', {
            'fields': ('sender', 'sender_name', 'sender_phone', 'sender_address', ('sender_city', 'sender_country', 'sender_postcode')),
            'classes': ('wide',),
        }),
        ('📥 Receiver Information', {
            'fields': ('receiver_name', 'receiver_phone', 'receiver_address', ('receiver_city', 'receiver_country', 'receiver_postcode')),
            'classes': ('wide',),
        }),
        ('📐 Package Dimensions', {
            'fields': (('weight', 'length', 'width', 'height'), 'description'),
            'classes': ('collapse', 'wide'),
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['mark_processing', 'mark_in_transit', 'mark_out_for_delivery', 'mark_delivered', 'mark_cancelled']
    
    def tracking_link(self, obj):
        url = reverse('admin:packages_package_change', args=[obj.pk])
        return format_html(
            '<a href="{}" style="font-weight:600; color:#4f46e5;">{}</a>',
            url, obj.tracking_number
        )
    tracking_link.short_description = 'Tracking #'
    tracking_link.admin_order_field = 'tracking_number'
    
    def sender_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small style="color:#6b7280;">{}</small>',
            obj.sender_name, obj.sender_city
        )
    sender_info.short_description = 'From'
    
    def receiver_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small style="color:#6b7280;">{}</small>',
            obj.receiver_name, obj.receiver_city
        )
    receiver_info.short_description = 'To'
    
    def driver_info(self, obj):
        if obj.assigned_driver:
            return format_html(
                '<span style="color:#059669;">🚚 {}</span>',
                obj.assigned_driver.username
            )
        return format_html('<span style="color:#9ca3af;">— Unassigned</span>')
    driver_info.short_description = 'Driver'
    driver_info.admin_order_field = 'assigned_driver'
    
    def created_date(self, obj):
        return format_html(
            '<span title="{}">{}</span>',
            obj.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            obj.created_at.strftime('%b %d, %Y')
        )
    created_date.short_description = 'Created'
    created_date.admin_order_field = 'created_at'
    
    def status_badge(self, obj):
        colors = {
            'pending': ('#f59e0b', '#fffbeb'),
            'processing': ('#3b82f6', '#eff6ff'),
            'in_transit': ('#8b5cf6', '#f5f3ff'),
            'out_for_delivery': ('#ec4899', '#fdf2f8'),
            'delivered': ('#10b981', '#ecfdf5'),
            'cancelled': ('#ef4444', '#fef2f2'),
        }
        text_color, bg_color = colors.get(obj.status, ('#6b7280', '#f3f4f6'))
        return format_html(
            '<span style="background:{}; color:{}; padding:5px 12px; border-radius:20px; font-size:11px; font-weight:600; white-space:nowrap;">{}</span>',
            bg_color, text_color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def location_btn(self, obj):
        url = reverse('admin:package_update_location', args=[obj.pk])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary" style="font-size:11px;">📍 Update</a>',
            url
        )
    location_btn.short_description = 'Location'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:package_id>/update-location/', self.admin_site.admin_view(self.update_location_view), name='package_update_location'),
        ]
        return custom_urls + urls
    
    def update_location_view(self, request, package_id):
        if not request.user.has_perm('packages.change_package'):
            messages.error(request, 'You do not have permission to update package locations.')
            return redirect('admin:packages_package_changelist')
        package = get_object_or_404(Package, pk=package_id)
        tracking_history = package.tracking_history.all()[:10]
        
        if request.method == 'POST':
            status = request.POST.get('status')
            location = request.POST.get('location')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            notes = request.POST.get('notes', '')
            
            package.status = status
            package.save()
            
            TrackingHistory.objects.create(
                package=package,
                status=package.get_status_display(),
                location=location,
                latitude=latitude if latitude else None,
                longitude=longitude if longitude else None,
                notes=notes
            )
            
            messages.success(request, f'✓ Location updated for {package.tracking_number}')
            return redirect('admin:packages_package_change', package_id)
        
        context = {
            'package': package,
            'tracking_history': tracking_history,
            'title': f'Update Location - {package.tracking_number}',
            'opts': self.model._meta,
            'has_view_permission': True,
        }
        return render(request, 'admin/packages/update_location.html', context)
    
    @admin.action(description='⏳ Mark as Processing')
    def mark_processing(self, request, queryset):
        count = queryset.update(status='processing')
        for pkg in queryset:
            TrackingHistory.objects.create(package=pkg, status='Processing', location='Warehouse - Processing')
        messages.success(request, f'✓ {count} package(s) marked as Processing')
    
    @admin.action(description='🚚 Mark as In Transit')
    def mark_in_transit(self, request, queryset):
        count = queryset.update(status='in_transit')
        for pkg in queryset:
            TrackingHistory.objects.create(package=pkg, status='In Transit', location='Distribution Centre')
        messages.success(request, f'✓ {count} package(s) marked as In Transit')
    
    @admin.action(description='📍 Mark as Out for Delivery')
    def mark_out_for_delivery(self, request, queryset):
        count = queryset.update(status='out_for_delivery')
        for pkg in queryset:
            TrackingHistory.objects.create(package=pkg, status='Out for Delivery', location=f'{pkg.receiver_city} Local Depot')
        messages.success(request, f'✓ {count} package(s) marked as Out for Delivery')
    
    @admin.action(description='✅ Mark as Delivered')
    def mark_delivered(self, request, queryset):
        count = queryset.update(status='delivered')
        for pkg in queryset:
            TrackingHistory.objects.create(package=pkg, status='Delivered', location=f'{pkg.receiver_city}, {pkg.receiver_postcode}')
        messages.success(request, f'✓ {count} package(s) marked as Delivered')
    
    @admin.action(description='❌ Mark as Cancelled')
    def mark_cancelled(self, request, queryset):
        count = queryset.update(status='cancelled')
        for pkg in queryset:
            TrackingHistory.objects.create(package=pkg, status='Cancelled', location='Cancelled by Admin')
        messages.success(request, f'✓ {count} package(s) cancelled')
