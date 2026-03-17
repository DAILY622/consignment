from django.contrib import admin
from consignment.admin import admin_site
from .models import TrackingHistory


class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = ('package', 'status', 'location', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('package__tracking_number', 'location', 'notes')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'


admin_site.register(TrackingHistory, TrackingHistoryAdmin)
