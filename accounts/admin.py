from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from consignment.admin import admin_site
from .models import User


@admin.register(User, site=admin_site)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role_badge', 'phone', 'is_active_icon', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_per_page = 25
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Contact', {
            'fields': ('role', 'phone', 'address'),
            'classes': ('wide',)
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role & Contact', {
            'fields': ('role', 'phone', 'address'),
            'classes': ('wide',)
        }),
    )
    
    def role_badge(self, obj):
        colors = {
            'admin': ('#dc2626', '#fef2f2'),
            'driver': ('#2563eb', '#eff6ff'),
            'user': ('#059669', '#ecfdf5'),
        }
        text_color, bg_color = colors.get(obj.role, ('#6b7280', '#f3f4f6'))
        return format_html(
            '<span style="background:{}; color:{}; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:600;">{}</span>',
            bg_color, text_color, obj.get_role_display()
        )
    role_badge.short_description = 'Role'
    role_badge.admin_order_field = 'role'
    
    def is_active_icon(self, obj):
        if obj.is_active:
            return format_html('<span style="color:#059669;">✓ Active</span>')
        return format_html('<span style="color:#dc2626;">✗ Inactive</span>')
    is_active_icon.short_description = 'Status'
    is_active_icon.admin_order_field = 'is_active'
