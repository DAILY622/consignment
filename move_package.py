"""
📍 Location Update Tool for Package Tracking
Usage: python move_package.py <tracking_number> <city> <country> <lat> <lng>

Examples:
  python move_package.py DFX-2XWJFI8R "Lahore" "Pakistan" 31.5497 74.3436
  python move_package.py ECG-KPB32BYG "Islamabad" "Pakistan" 33.6844 73.0479
"""

import os
import django
import sys
from datetime import datetime

if len(sys.argv) < 6:
    print(__doc__)
    print("\nQuick Locations for Testing:")
    print("  Quetta, Pakistan: 30.1798, 66.9750")
    print("  Kandahar, Afghanistan: 31.6089, 65.7372")
    print("  Lahore, Pakistan: 31.5497, 74.3436")
    print("  Islamabad, Pakistan: 33.6844, 73.0479")
    print("  Peshawar, Pakistan: 34.0151, 71.5249")
    sys.exit(1)

tracking_number = sys.argv[1]
city = sys.argv[2]
country = sys.argv[3]
lat = float(sys.argv[4])
lng = float(sys.argv[5])

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consignment.settings')
django.setup()

from packages.models import Package
from tracking.models import TrackingHistory

# Find package
package = Package.objects.filter(tracking_number=tracking_number).first()

if not package:
    print(f"❌ Package {tracking_number} not found!")
    sys.exit(1)

location_name = f"{city}, {country}"

print(f"📦 Package: {package.tracking_number}")
print(f"   Status: {package.status}")
print(f"   Route: {package.sender_city}, {package.sender_country} → {package.receiver_city}, {package.receiver_country}")
print(f"\n🔄 Updating to: {location_name}")
print(f"   Coordinates: {lat}, {lng}")

# Create tracking entry
tracking = TrackingHistory.objects.create(
    package=package,
    status="In Transit",
    location=location_name,
    latitude=lat,
    longitude=lng,
    notes=f"Package location updated to {location_name}",
    timestamp=datetime.now()
)

package.status = 'in_transit'
package.save()

print(f"\n✅ Location updated successfully!")
print(f"   Tracking ID: {tracking.id}")
print(f"   Time: {tracking.timestamp.strftime('%b %d, %Y at %I:%M %p')}")

# Calculate distance to destination
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c

dest_coords = {
    'Lahore': (31.5497, 74.3436),
    'Islamabad': (33.6844, 73.0479)
}

dest_city = package.receiver_city
if dest_city in dest_coords:
    dest_lat, dest_lng = dest_coords[dest_city]
    dist = haversine(lat, lng, dest_lat, dest_lng)
    hours = dist / 65
    print(f"\n📏 Distance to {dest_city}: {dist:.1f} km")
    print(f"⏱️  Estimated time: {hours:.1f} hours")

print(f"\n🗺️  View on map:")
print(f"   http://localhost:8000/track/?q={tracking_number}")
