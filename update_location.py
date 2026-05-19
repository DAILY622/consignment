import os
import django
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consignment.settings')
django.setup()

from packages.models import Package
from tracking.models import TrackingHistory

print("=== UPDATING PACKAGE LOCATION ===\n")

# Get the first package
package = Package.objects.filter(tracking_number='DFX-2XWJFI8R').first()

if package:
    print(f"📦 Package: {package.tracking_number}")
    print(f"   Current Status: {package.status}")
    
    # Current location (Zahedan, Iran: 29.4963, 60.8629)
    # Destination (Lahore, Pakistan: 31.5497, 74.3436)
    
    # Nearest city along the route: Quetta, Pakistan (30.1798, 66.9750)
    # This is between Zahedan and Lahore
    
    new_location = "Quetta, Pakistan"
    new_lat = 30.1798
    new_lng = 66.9750
    new_status = "In Transit"
    
    print(f"\n🔄 Updating to nearest location:")
    print(f"   Location: {new_location}")
    print(f"   Coordinates: {new_lat}, {new_lng}")
    print(f"   Status: {new_status}")
    
    # Create new tracking entry
    tracking = TrackingHistory.objects.create(
        package=package,
        status=new_status,
        location=new_location,
        latitude=new_lat,
        longitude=new_lng,
        notes="Package moved closer to destination - updated via tracking system",
        timestamp=datetime.now()
    )
    
    # Update package status if needed
    package.status = 'in_transit'
    package.save()
    
    print(f"\n✅ Location updated successfully!")
    print(f"   Tracking ID: {tracking.id}")
    print(f"   Time: {tracking.timestamp}")
    
    # Show route progress
    print(f"\n📍 Route Progress:")
    print(f"   Origin: Oslo, Norway")
    print(f"   Previous: Zahedan, Iran (29.50°N, 60.86°E)")
    print(f"   ➡️  CURRENT: {new_location} ({new_lat}°N, {new_lng}°E)")
    print(f"   Destination: Lahore, Pakistan (31.55°N, 74.34°E)")
    
    # Calculate distances
    from math import radians, cos, sin, asin, sqrt
    
    def haversine(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km
    
    dist_to_destination = haversine(new_lat, new_lng, 31.5497, 74.3436)
    print(f"\n📏 Distance remaining: {dist_to_destination:.1f} km to Lahore")
    
    # List all tracking history
    print(f"\n📋 Complete Tracking History:")
    history = TrackingHistory.objects.filter(package=package).order_by('timestamp')
    for i, event in enumerate(history, 1):
        print(f"   {i}. {event.location} - {event.timestamp.strftime('%b %d, %I:%M %p')}")
else:
    print("❌ Package not found")
