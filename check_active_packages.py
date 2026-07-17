import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consignment.settings')
django.setup()

from packages.models import Package

# Get all active packages in transit
active_packages = Package.objects.filter(
    status__in=['in_transit', 'out_for_delivery']
).order_by('-created_at')

print(f"\n{'='*70}")
print(f"ACTIVE PACKAGES IN TRANSIT: {active_packages.count()}")
print(f"{'='*70}\n")

if active_packages.count() == 0:
    print("No packages currently in transit.")
    print("\nTo add sample data, run: python manage.py seed_data")
else:
    for package in active_packages:
        print(f"Tracking: {package.tracking_number}")
        print(f"   Status: {package.get_status_display()}")
        print(f"   From: {package.sender_name} ({package.origin_city}, {package.origin_country})")
        print(f"   To: {package.recipient_name} ({package.destination_city}, {package.destination_country})")
        print(f"   Weight: {package.weight}kg")
        print(f"   Created: {package.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"   {'-'*68}\n")

# Overall statistics
all_packages = Package.objects.all()
print(f"\n{'='*70}")
print(f"OVERALL STATISTICS")
print(f"{'='*70}")
print(f"Total packages: {all_packages.count()}")
print(f"Pending: {all_packages.filter(status='pending').count()}")
print(f"In Transit: {all_packages.filter(status='in_transit').count()}")
print(f"Out for Delivery: {all_packages.filter(status='out_for_delivery').count()}")
print(f"Delivered: {all_packages.filter(status='delivered').count()}")
print(f"{'='*70}\n")
