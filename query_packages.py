import os
import django
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consignment.settings')
django.setup()

# Now import models
from packages.models import Package
from tracking.models import TrackingHistory

print("=== ACTIVE PACKAGES ===")
packages = Package.objects.all()
if packages.exists():
    for p in packages:
        print(f"{p.tracking_number} | Status: {p.status} | {p.sender_city}, {p.sender_country} -> {p.receiver_city}, {p.receiver_country}")
else:
    print("No packages found in database")

print("\n=== CURRENT LOCATIONS ===")
for p in packages:
    latest = TrackingHistory.objects.filter(package=p).order_by("-timestamp").first()
    loc = latest.location if latest else "No tracking"
    print(f"{p.tracking_number}: {loc}")
