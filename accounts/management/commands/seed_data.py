from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from accounts.models import User
from packages.models import Package
from tracking.models import TrackingHistory


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
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
        
        # Sample UK cities with coordinates
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
        
        # Create sample packages
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
                # Add tracking history
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
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('')
        self.stdout.write('Demo accounts:')
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  User: user / password')
        self.stdout.write('  Driver: driver / driver123')
