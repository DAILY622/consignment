from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from consignment.admin import admin_site
from .models import TrackingHistory, RouteWaypoint


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
        url = reverse('admin:packages_package_change', args=[obj.package.pk])
        return format_html(
            '<a href="{}" style="font-weight:600; color:#4f46e5;">{}</a>',
            url, obj.package.tracking_number
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


class RouteWaypointInline(admin.TabularInline):
    """Inline for editing route waypoints directly from Package admin"""
    model = RouteWaypoint
    extra = 1
    fields = ('order', 'city_name', 'latitude', 'longitude', 'is_passed', 'notes')
    ordering = ['order']
    classes = ('collapse',)
    verbose_name = "Route Waypoint"
    verbose_name_plural = "🗺️ Route Waypoints (Admin can edit the truck's path)"


@admin.register(RouteWaypoint, site=admin_site)
class RouteWaypointAdmin(admin.ModelAdmin):
    """Admin for managing route waypoints - defines where truck passes through"""
    list_display = ('package_link', 'order', 'city_name', 'coordinates', 'is_passed', 'status_badge', 'notes')
    list_filter = ('is_passed', 'package__status')
    search_fields = ('package__tracking_number', 'city_name', 'notes')
    list_editable = ('order', 'city_name', 'is_passed')
    list_per_page = 50
    list_select_related = ('package',)
    ordering = ('package', 'order')
    
    fieldsets = (
        ('📦 Package', {
            'fields': ('package',),
        }),
        ('📍 Waypoint Details', {
            'fields': ('city_name', ('latitude', 'longitude'), 'order', 'is_passed', 'notes'),
            'description': 'Define the stops where the truck will pass through on the map.',
        }),
    )
    
    def package_link(self, obj):
        url = reverse('admin:packages_package_change', args=[obj.package.pk])
        return format_html(
            '<a href="{}" style="font-weight:600; color:#4f46e5;">{}</a>',
            url, obj.package.tracking_number
        )
    package_link.short_description = 'Package'
    package_link.admin_order_field = 'package__tracking_number'
    
    def coordinates(self, obj):
        return format_html(
            '<a href="https://www.google.com/maps?q={},{}" target="_blank" style="color:#059669;">{:.4f}, {:.4f}</a>',
            obj.latitude, obj.longitude, obj.latitude, obj.longitude
        )
    coordinates.short_description = 'Coordinates'
    
    def status_badge(self, obj):
        if obj.is_passed:
            return format_html(
                '<span style="background:#dcfce7; color:#166534; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:600;">✓ Passed</span>'
            )
        return format_html(
            '<span style="background:#fef3c7; color:#92400e; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:600;">○ Upcoming</span>'
        )
    status_badge.short_description = 'Status'
