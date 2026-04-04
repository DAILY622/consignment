"""
Management command to create a demo package from Norway to Pakistan.
Run on Render: python manage.py create_demo_package
"""
from django.core.management.base import BaseCommand
from accounts.models import User
from packages.models import Package
from tracking.models import TrackingHistory
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Create a demo package from Norway to Pakistan (in_transit status with car icon)'

    def handle(self, *args, **options):
        # Get or create admin user
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user = User.objects.first()
        
        if not user:
            self.stdout.write(self.style.ERROR('No users found. Create a user first.'))
            return

        # Check if demo package already exists
        existing = Package.objects.filter(
            sender_city='Oslo',
            receiver_city='Islamabad',
            status='in_transit'
        ).first()
        
        if existing:
            self.stdout.write(self.style.WARNING(
                f'Demo package already exists: {existing.tracking_number}'
            ))
            return

        # Create Norway to Pakistan package
        pkg = Package.objects.create(
            sender=user,
            sender_name='Erik Nordmann',
            sender_address='Karl Johans gate 15',
            sender_phone='+4712345678',
            sender_city='Oslo',
            sender_country='Norway',
            sender_postcode='0154',
            receiver_name='Ahmed Khan',
            receiver_address='Faisal Avenue, F-7',
            receiver_phone='+923001234567',
            receiver_city='Islamabad',
            receiver_country='Pakistan',
            receiver_postcode='44000',
            weight=2.5,
            description='Electronics and documents - International Express',
            status='in_transit',
            estimated_delivery=date.today() + timedelta(days=5)
        )

        # Create tracking history showing the journey
        TrackingHistory.objects.create(
            package=pkg,
            status='Package Created',
            location='Oslo, Norway',
            latitude=59.9139,
            longitude=10.7522,
            notes='Shipment registered at Oslo distribution center'
        )

        TrackingHistory.objects.create(
            package=pkg,
            status='Processing',
            location='Oslo Airport, Gardermoen',
            latitude=60.1939,
            longitude=11.1004,
            notes='Package processed for international shipping'
        )

        TrackingHistory.objects.create(
            package=pkg,
            status='In Transit',
            location='Frankfurt, Germany - Transit Hub',
            latitude=50.0379,
            longitude=8.5622,
            notes='Package in transit through European hub'
        )

        TrackingHistory.objects.create(
            package=pkg,
            status='In Transit',
            location='Dubai, UAE - Transit Hub',
            latitude=25.2532,
            longitude=55.3657,
            notes='Package arrived at Dubai transit facility'
        )

        # Current location - on the road between Dubai and Pakistan
        TrackingHistory.objects.create(
            package=pkg,
            status='In Transit',
            location='En route to Pakistan',
            latitude=28.5,
            longitude=65.0,
            notes='Package on delivery vehicle heading to destination'
        )

        self.stdout.write(self.style.SUCCESS(
            f'✅ Created demo package: {pkg.tracking_number}'
        ))
        self.stdout.write(f'   From: {pkg.sender_city}, {pkg.sender_country}')
        self.stdout.write(f'   To: {pkg.receiver_city}, {pkg.receiver_country}')
        self.stdout.write(f'   Status: {pkg.status} (shows 🚗 car icon on map)')
        self.stdout.write(f'\n   Track at: /track/?q={pkg.tracking_number}')
