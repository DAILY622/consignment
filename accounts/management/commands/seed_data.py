from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from accounts.models import User
from packages.models import Package
from tracking.models import TrackingHistory, RouteWaypoint
from consignment.models import SiteSettings


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Initialize SiteSettings
        SiteSettings.objects.get_or_create(pk=1)
        self.stdout.write(self.style.SUCCESS('✅ Site settings initialized'))
        
        # Create admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Admin',
                'last_name': 'User',
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        
        # Create regular user
        user, created = User.objects.get_or_create(
            username='user',
            defaults={
                'email': 'user@example.com',
                'role': 'user',
                'first_name': 'John',
                'last_name': 'Smith',
                'phone': '07700 900000',
                'address': '123 High Street, London',
            }
        )
        if created:
            user.set_password('password')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created regular user'))
        
        # Create driver user
        driver, created = User.objects.get_or_create(
            username='driver',
            defaults={
                'email': 'driver@example.com',
                'role': 'driver',
                'first_name': 'Dave',
                'last_name': 'Driver',
                'phone': '07700 900001',
            }
        )
        if created:
            driver.set_password('driver123')
            driver.save()
            self.stdout.write(self.style.SUCCESS('Created driver user'))
        
        # ============================================
        # CREATE NORWAY → PAKISTAN DEMO PACKAGE
        # ============================================
        erik, created = User.objects.get_or_create(
            username='erik.johansen',
            defaults={
                'email': 'erik@example.no',
                'first_name': 'Erik',
                'last_name': 'Johansen',
            }
        )
        if created:
            erik.set_password('demo123')
            erik.save()
        
        demo_pkg, created = Package.objects.get_or_create(
            tracking_number='DFX-2XWJFI8R',
            defaults={
                'sender': erik,
                'sender_name': 'Erik Johansen',
                'sender_address': 'Karl Johans gate 15',
                'sender_phone': '+47 123 45 678',
                'sender_city': 'Oslo',
                'sender_country': 'Norway',
                'sender_postcode': '0154',
                'receiver_name': 'Ahmed Khan',
                'receiver_address': '45 Mall Road, Gulberg III',
                'receiver_phone': '+92 300 1234567',
                'receiver_city': 'Lahore',
                'receiver_country': 'Pakistan',
                'receiver_postcode': '54000',
                'weight': 2.5,
                'description': 'Electronics and documents',
                'status': 'in_transit',
                'estimated_delivery': timezone.now().date() + timedelta(days=5),
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ Created demo package: DFX-2XWJFI8R'))
            
            # Add tracking history
            tracking_data = [
                ('Package Created', 'Oslo, Norway', 59.9139, 10.7522),
                ('In Transit', 'Gothenburg, Sweden', 57.7089, 11.9746),
                ('In Transit', 'Copenhagen, Denmark', 55.6761, 12.5683),
                ('In Transit', 'Hamburg, Germany', 53.5511, 9.9937),
                ('In Transit', 'Prague, Czech Republic', 50.0755, 14.4378),
                ('In Transit', 'Vienna, Austria', 48.2082, 16.3738),
                ('In Transit', 'Budapest, Hungary', 47.4979, 19.0402),
                ('In Transit', 'Bucharest, Romania', 44.4268, 26.1025),
                ('In Transit', 'Sofia, Bulgaria', 42.6977, 23.3219),
                ('In Transit', 'Istanbul, Turkey', 41.0082, 28.9784),
                ('In Transit', 'Ankara, Turkey', 39.9334, 32.8597),
                ('In Transit', 'Erzurum, Turkey', 39.9055, 41.2658),
                ('In Transit', 'Tabriz, Iran', 38.0962, 46.2738),
                ('In Transit', 'Tehran, Iran', 35.6892, 51.3890),
                ('In Transit', 'Isfahan, Iran', 32.6546, 51.6680),
                ('In Transit', 'Kerman, Iran', 30.2839, 57.0834),
                ('In Transit', 'Zahedan, Iran', 29.4963, 60.8629),
            ]
            
            for status, location, lat, lng in tracking_data:
                TrackingHistory.objects.create(
                    package=demo_pkg,
                    status=status,
                    location=location,
                    latitude=lat,
                    longitude=lng,
                )
            
            # Add route waypoints
            waypoints = [
                (0, 'Kandahar', 31.6289, 65.7372),
                (1, 'Kabul', 34.5553, 69.2075),
                (2, 'Peshawar', 34.0151, 71.5249),
                (3, 'Islamabad', 33.6844, 73.0479),
                (4, 'Kashmir', 34.0837, 74.7973),
                (5, 'Jammu', 32.7266, 74.8570),
                (6, 'Pathankot', 32.2746, 75.6421),
            ]
            
            for order, city, lat, lng in waypoints:
                RouteWaypoint.objects.create(
                    package=demo_pkg,
                    city_name=city,
                    latitude=lat,
                    longitude=lng,
                    order=order,
                    is_passed=False,
                )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Added tracking history and route waypoints'))
        
        # ============================================
        # SAMPLE UK PACKAGES
        # ============================================
        cities = [
            ('London', 'SW1A 1AA', 51.5074, -0.1278),
            ('Manchester', 'M1 1AD', 53.4808, -2.2426),
            ('Birmingham', 'B1 1AA', 52.4862, -1.8904),
            ('Leeds', 'LS1 1UR', 53.8008, -1.5491),
            ('Glasgow', 'G1 1AA', 55.8642, -4.2518),
            ('Edinburgh', 'EH1 1YZ', 55.9533, -3.1883),
            ('Liverpool', 'L1 1JQ', 53.4084, -2.9916),
            ('Bristol', 'BS1 1AA', 51.4545, -2.5879),
            ('Cardiff', 'CF10 1EP', 51.4816, -3.1791),
            ('Belfast', 'BT1 1AA', 54.5973, -5.9301),
        ]
        
        statuses = ['pending', 'processing', 'in_transit', 'out_for_delivery', 'delivered']
        
        for i in range(10):
            sender_city = random.choice(cities)
            receiver_city = random.choice([c for c in cities if c != sender_city])
            status = random.choice(statuses)
            
            package, created = Package.objects.get_or_create(
                tracking_number=f'ECG-DEMO{i:04d}',
                defaults={
                    'sender': user,
                    'sender_name': 'John Smith',
                    'sender_address': f'{random.randint(1, 200)} High Street',
                    'sender_phone': '07700 900000',
                    'sender_city': sender_city[0],
                    'sender_postcode': sender_city[1],
                    'receiver_name': f'Customer {i+1}',
                    'receiver_address': f'{random.randint(1, 200)} Main Road',
                    'receiver_phone': f'07700 90{i:04d}',
                    'receiver_city': receiver_city[0],
                    'receiver_postcode': receiver_city[1],
                    'weight': round(random.uniform(0.5, 25.0), 2),
                    'status': status,
                    'assigned_driver': driver if status in ['in_transit', 'out_for_delivery'] else None,
                    'estimated_delivery': timezone.now().date() + timedelta(days=random.randint(1, 5)),
                }
            )
            
            if created:
                TrackingHistory.objects.create(
                    package=package,
                    status='Package Created',
                    location=f"{sender_city[0]}, {sender_city[1]}",
                    latitude=sender_city[2],
                    longitude=sender_city[3],
                    notes='Shipment registered'
                )
                
                if status != 'pending':
                    TrackingHistory.objects.create(
                        package=package,
                        status='Picked Up',
                        location=f"{sender_city[0]} Depot",
                        latitude=sender_city[2] + 0.01,
                        longitude=sender_city[3] + 0.01,
                    )
                
                if status in ['in_transit', 'out_for_delivery', 'delivered']:
                    TrackingHistory.objects.create(
                        package=package,
                        status='In Transit',
                        location='National Distribution Centre',
                        latitude=52.5,
                        longitude=-1.5,
                    )
                
                if status in ['out_for_delivery', 'delivered']:
                    TrackingHistory.objects.create(
                        package=package,
                        status='Out for Delivery',
                        location=f"{receiver_city[0]} Depot",
                        latitude=receiver_city[2],
                        longitude=receiver_city[3],
                    )
                
                if status == 'delivered':
                    TrackingHistory.objects.create(
                        package=package,
                        status='Delivered',
                        location=f"{receiver_city[0]}, {receiver_city[1]}",
                        latitude=receiver_city[2],
                        longitude=receiver_city[3],
                        notes='Signed by recipient'
                    )
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Database seeded successfully!'))
        self.stdout.write('')
        self.stdout.write('Demo accounts:')
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  User: user / password')
        self.stdout.write('  Driver: driver / driver123')
        self.stdout.write('')
        self.stdout.write('Demo package:')
        self.stdout.write('  Track: /track/?q=DFX-2XWJFI8R')
