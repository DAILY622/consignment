from django.contrib import admin
from django.utils.html import format_html
from consignment.admin import admin_site
from .models import ProofOfDelivery


@admin.register(ProofOfDelivery, site=admin_site)
class ProofOfDeliveryAdmin(admin.ModelAdmin):
    list_display = ('package_link', 'driver_info', 'recipient_name', 'proof_status', 'location_link', 'delivered_at')
    list_filter = ('delivered_at', 'driver')
    search_fields = ('package__tracking_number', 'recipient_name', 'driver__username')
    readonly_fields = ('delivered_at', 'photo_preview', 'signature_preview')
    date_hierarchy = 'delivered_at'
    list_per_page = 25
    list_select_related = ('package', 'driver')
    
    fieldsets = (
        ('📦 Delivery Details', {
            'fields': ('package', 'driver', 'recipient_name'),
        }),
        ('📸 Proof of Delivery', {
            'fields': ('photo', 'photo_preview', 'signature', 'signature_preview'),
            'classes': ('wide',),
        }),
        ('📍 Location', {
            'fields': (('latitude', 'longitude'), 'notes'),
        }),
        ('🕐 Timestamp', {
            'fields': ('delivered_at',),
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
    
    def driver_info(self, obj):
        return format_html(
            '<span style="color:#2563eb;">🚚 {}</span>',
            obj.driver.username
        )
    driver_info.short_description = 'Driver'
    driver_info.admin_order_field = 'driver__username'
    
    def proof_status(self, obj):
        has_photo = bool(obj.photo)
        has_signature = bool(obj.signature)
        
        if has_photo and has_signature:
            return format_html('<span style="color:#059669;">✓ Complete</span>')
        elif has_photo or has_signature:
            return format_html('<span style="color:#f59e0b;">⚠ Partial</span>')
        return format_html('<span style="color:#dc2626;">✗ Missing</span>')
    proof_status.short_description = 'Proof'
    
    def location_link(self, obj):
        if obj.latitude and obj.longitude:
            return format_html(
                '<a href="https://www.google.com/maps?q={},{}" target="_blank" style="color:#059669;">🗺️ Map</a>',
                obj.latitude, obj.longitude
            )
        return format_html('<span style="color:#9ca3af;">—</span>')
    location_link.short_description = 'Location'
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width:200px; max-height:150px; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1);" />',
                obj.photo.url
            )
        return format_html('<span style="color:#9ca3af;">No photo uploaded</span>')
    photo_preview.short_description = 'Photo Preview'
    
    def signature_preview(self, obj):
        if obj.signature:
            return format_html(
                '<img src="{}" style="max-width:200px; max-height:100px; border-radius:8px; border:1px solid #e5e7eb;" />',
                obj.signature.url
            )
        return format_html('<span style="color:#9ca3af;">No signature uploaded</span>')
    signature_preview.short_description = 'Signature Preview'
