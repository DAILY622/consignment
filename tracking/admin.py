from django.contrib import admin
from django.utils.html import format_html
from consignment.admin import admin_site
from .models import TrackingHistory


@admin.register(TrackingHistory, site=admin_site)
class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = ('package_link', 'status_display', 'location', 'coordinates', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('package__tracking_number', 'location', 'notes', 'status')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    list_per_page = 30
    list_select_related = ('package',)
    ordering = ('-timestamp',)
    
    fieldsets = (
        ('📦 Package', {
            'fields': ('package',),
        }),
        ('📍 Location Update', {
            'fields': ('status', 'location', ('latitude', 'longitude'), 'notes'),
        }),
        ('🕐 Timestamp', {
            'fields': ('timestamp',),
            'classes': ('collapse',),
        }),
    )
    
    def package_link(self, obj):
        return format_html(
            '<a href="/admin/packages/package/{}/change/" style="font-weight:600; color:#4f46e5;">{}</a>',
            obj.package.pk, obj.package.tracking_number
        )
    package_link.short_description = 'Package'
    package_link.admin_order_field = 'package__tracking_number'
    
    def status_display(self, obj):
        status_icons = {
            'Pending': '⏳',
            'Processing': '⚙️',
            'In Transit': '🚚',
            'Out for Delivery': '📍',
            'Delivered': '✅',
            'Cancelled': '❌',
        }
        icon = status_icons.get(obj.status, '📦')
        return format_html('<span>{} {}</span>', icon, obj.status)
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'
    
    def coordinates(self, obj):
        if obj.latitude and obj.longitude:
            return format_html(
                '<a href="https://www.google.com/maps?q={},{}" target="_blank" style="color:#059669;">🗺️ View Map</a>',
                obj.latitude, obj.longitude
            )
        return format_html('<span style="color:#9ca3af;">—</span>')
    coordinates.short_description = 'Map'
