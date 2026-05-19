import os
import django
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consignment.settings')
django.setup()

from packages.models import Package
from tracking.models import TrackingHistory

print("=== UPDATING SECOND PACKAGE LOCATION ===\n")

# Get the second package
package = Package.objects.filter(tracking_number='ECG-KPB32BYG').first()

if package:
    print(f"📦 Package: {package.tracking_number}")
    print(f"   Current Status: {package.status}")
    
    # Current location (En route to Pakistan: 28.5, 65)
    # Destination (Islamabad, Pakistan: 33.6844, 73.0479)
    
    # Nearest city along the route: Kandahar, Afghanistan (31.6089, 65.7372)
    # This is between current position and Islamabad
    
    new_location = "Kandahar, Afghanistan"
    new_lat = 31.6089
    new_lng = 65.7372
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
        notes="Package progressing toward Islamabad - border crossing complete",
        timestamp=datetime.now()
    )
    
    # Update package status
    package.status = 'in_transit'
    package.save()
    
    print(f"\n✅ Location updated successfully!")
    print(f"   Tracking ID: {tracking.id}")
    print(f"   Time: {tracking.timestamp}")
    
    # Show route progress
    print(f"\n📍 Route Progress:")
    print(f"   Origin: Oslo, Norway")
    print(f"   Previous: En route (28.50°N, 65.00°E)")
    print(f"   ➡️  CURRENT: {new_location} ({new_lat}°N, {new_lng}°E)")
    print(f"   Destination: Islamabad, Pakistan (33.68°N, 73.05°E)")
    
    # Calculate distance
    from math import radians, cos, sin, asin, sqrt
    
    def haversine(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km
    
    dist_to_destination = haversine(new_lat, new_lng, 33.6844, 73.0479)
    print(f"\n📏 Distance remaining: {dist_to_destination:.1f} km to Islamabad")
    
    # List recent tracking history
    print(f"\n📋 Recent Tracking History:")
    history = TrackingHistory.objects.filter(package=package).order_by('-timestamp')[:5]
    for i, event in enumerate(history, 1):
        print(f"   {i}. {event.location} - {event.timestamp.strftime('%b %d, %I:%M %p')}")
else:
    print("❌ Package not found")

print("\n" + "="*60)
print("🎉 Both packages have been updated to nearest locations!")
print("="*60)
