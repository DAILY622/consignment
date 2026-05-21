#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consignment.settings')
django.setup()

from packages.models import Package
from tracking.models import TrackingHistory, RouteWaypoint

# Find packages from Norway to Pakistan
packages = Package.objects.filter(
    sender_country='Norway',
    receiver_country='Pakistan'
).order_by('-created_at')

if packages.exists():
    for pkg in packages:
        print('='*60)
        print(f'Package Details:')
        print(f'Tracking Number: {pkg.tracking_number}')
        print(f'Status: {pkg.status}')
        print(f'Service: {pkg.service}')
        print(f'Weight: {pkg.weight}kg')
        print(f'Dimensions: {pkg.length}x{pkg.width}x{pkg.height} cm')
        print(f'Price: NOK {pkg.price}')
        print(f'')
        print(f'Sender:')
        print(f'  Name: {pkg.sender_name}')
        print(f'  Address: {pkg.sender_address}')
        print(f'  City: {pkg.sender_city}')
        print(f'  Postal Code: {pkg.sender_postal_code}')
        print(f'  Country: {pkg.sender_country}')
        print(f'  Phone: {pkg.sender_phone}')
        print(f'  Email: {pkg.sender_email}')
        print(f'')
        print(f'Receiver:')
        print(f'  Name: {pkg.receiver_name}')
        print(f'  Address: {pkg.receiver_address}')
        print(f'  City: {pkg.receiver_city}')
        print(f'  Postal Code: {pkg.receiver_postal_code}')
        print(f'  Country: {pkg.receiver_country}')
        print(f'  Phone: {pkg.receiver_phone}')
        print(f'  Email: {pkg.receiver_email}')
        print(f'')
        print(f'Created: {pkg.created_at}')
        print(f'Updated: {pkg.updated_at}')
        print(f'User: {pkg.user.username if pkg.user else "Guest"}')
        print(f'')
        
        # Get tracking history
        tracking = TrackingHistory.objects.filter(package=pkg).order_by('timestamp')
        if tracking.exists():
            print(f'Tracking History:')
            for t in tracking:
                print(f'  [{t.timestamp}] {t.status} - {t.location}')
                if t.description:
                    print(f'    {t.description}')
        print('='*60)
        print()
else:
    print('No packages found from Norway to Pakistan')
    print()
    print('Recent packages in database:')
    all_packages = Package.objects.all().order_by('-created_at')[:10]
    if all_packages.exists():
        for pkg in all_packages:
            print(f'  {pkg.tracking_number}: {pkg.sender_country} → {pkg.receiver_country} ({pkg.status})')
    else:
        print('  No packages in database')
