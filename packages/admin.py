from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.html import format_html
from consignment.admin import admin_site
from .models import Package
from tracking.models import TrackingHistory


class TrackingHistoryInline(admin.TabularInline):
    model = TrackingHistory
    extra = 0
    readonly_fields = ('timestamp',)
    fields = ('status', 'location', 'latitude', 'longitude', 'notes', 'timestamp')


class PackageAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'sender', 'receiver_name', 'receiver_city', 'status_badge', 'assigned_driver', 'location_btn', 'created_at')
    list_filter = ('status', 'created_at', 'sender_city', 'receiver_city')
    search_fields = ('tracking_number', 'sender__username', 'receiver_name', 'sender_name')
    readonly_fields = ('tracking_number', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    inlines = [TrackingHistoryInline]
    
    fieldsets = (
        ('Tracking', {
            'fields': ('tracking_number', 'status', 'assigned_driver', 'estimated_delivery')
        }),
        ('Sender Information', {
            'fields': ('sender', 'sender_name', 'sender_address', 'sender_city', 'sender_postcode', 'sender_phone')
        }),
        ('Receiver Information', {
            'fields': ('receiver_name', 'receiver_address', 'receiver_city', 'receiver_postcode', 'receiver_phone')
        }),
        ('Package Details', {
            'fields': ('weight', 'length', 'width', 'height', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_in_transit', 'mark_out_for_delivery', 'mark_delivered', 'mark_cancelled']
    
    def status_badge(self, obj):
        colors = {
            'pending': '#fef3c7',
            'processing': '#dbeafe',
            'in_transit': '#e0e7ff',
            'out_for_delivery': '#fce7f3',
            'delivered': '#d1fae5',
            'cancelled': '#fee2e2',
        }
        text_colors = {
            'pending': '#92400e',
            'processing': '#1e40af',
            'in_transit': '#3730a3',
            'out_for_delivery': '#9d174d',
            'delivered': '#065f46',
            'cancelled': '#991b1b',
        }
        return format_html(
            '<span style="background:{}; color:{}; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600;">{}</span>',
            colors.get(obj.status, '#f3f4f6'),
            text_colors.get(obj.status, '#374151'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def location_btn(self, obj):
        return format_html(
            '<a href="{}/update-location/" style="background:#4f46e5; color:white; padding:6px 12px; border-radius:6px; text-decoration:none; font-size:12px;">📍 Update Location</a>',
            obj.pk
        )
    location_btn.short_description = 'Location'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:package_id>/update-location/', self.admin_site.admin_view(self.update_location_view), name='package_update_location'),
        ]
        return custom_urls + urls
    
    def update_location_view(self, request, package_id):
        package = get_object_or_404(Package, pk=package_id)
        tracking_history = package.tracking_history.all()[:10]
        
        if request.method == 'POST':
            status = request.POST.get('status')
            location = request.POST.get('location')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            notes = request.POST.get('notes', '')
            
            # Update package status
            package.status = status
            package.save()
            
            # Create tracking history entry
            TrackingHistory.objects.create(
                package=package,
                status=package.get_status_display(),
                location=location,
                latitude=latitude if latitude else None,
                longitude=longitude if longitude else None,
                notes=notes
            )
            
            messages.success(request, f'Location updated for {package.tracking_number}')
            return redirect('admin:packages_package_change', package_id)
        
        context = {
            'package': package,
            'tracking_history': tracking_history,
            'title': f'Update Location - {package.tracking_number}',
            'opts': self.model._meta,
            'has_view_permission': True,
        }
        return render(request, 'admin/packages/update_location.html', context)
    
    @admin.action(description='Mark selected as In Transit')
    def mark_in_transit(self, request, queryset):
        count = queryset.update(status='in_transit')
        for pkg in queryset:
            TrackingHistory.objects.create(package=pkg, status='In Transit', location='Distribution Centre')
        messages.success(request, f'{count} package(s) marked as In Transit')
    
    @admin.action(description='Mark selected as Out for Delivery')
    def mark_out_for_delivery(self, request, queryset):
        count = queryset.update(status='out_for_delivery')
        for pkg in queryset:
            TrackingHistory.objects.create(package=pkg, status='Out for Delivery', location=f'{pkg.receiver_city} Local Depot')
        messages.success(request, f'{count} package(s) marked as Out for Delivery')
    
    @admin.action(description='Mark selected as Delivered')
    def mark_delivered(self, request, queryset):
        count = queryset.update(status='delivered')
        for pkg in queryset:
            TrackingHistory.objects.create(package=pkg, status='Delivered', location=f'{pkg.receiver_city}, {pkg.receiver_postcode}')
        messages.success(request, f'{count} package(s) marked as Delivered')
    
    @admin.action(description='Mark selected as Cancelled')
    def mark_cancelled(self, request, queryset):
        count = queryset.update(status='cancelled')
        messages.success(request, f'{count} package(s) cancelled')


admin_site.register(Package, PackageAdmin)
