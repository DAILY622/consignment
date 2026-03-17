from django.contrib import admin
from consignment.admin import admin_site
from .models import ProofOfDelivery


class ProofOfDeliveryAdmin(admin.ModelAdmin):
    list_display = ('package', 'driver', 'recipient_name', 'delivered_at')
    list_filter = ('delivered_at', 'driver')
    search_fields = ('package__tracking_number', 'recipient_name', 'driver__username')
    readonly_fields = ('delivered_at',)
    date_hierarchy = 'delivered_at'


admin_site.register(ProofOfDelivery, ProofOfDeliveryAdmin)
