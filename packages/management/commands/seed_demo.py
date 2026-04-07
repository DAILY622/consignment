"""
Management command to seed demo data for DailyFX Delivery.
Run with: python manage.py seed_demo
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from packages.models import Package
from tracking.models import TrackingHistory, RouteWaypoint
from consignment.models import SiteSettings
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds demo data including admin user, demo package, and route waypoints'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding demo data...\n')
        
        # 1. Create or get admin superuser
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@dailyfxdelivery.co.uk',
                'is_staff': True,
                'is_superuser': True,
                'role': 'admin',
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('✅ Created admin user (admin/admin123)'))
        else:
            self.stdout.write('ℹ️  Admin user already exists')
        
        # 2. Create or get demo sender user
        sender, created = User.objects.get_or_create(
            username='erik.johansen',
            defaults={
                'email': 'erik@example.no',
                'first_name': 'Erik',
                'last_name': 'Johansen',
            }
        )
        if created:
            sender.set_password('demo123')
            sender.save()
            self.stdout.write(self.style.SUCCESS('✅ Created demo sender user'))
        
        # 3. Create SiteSettings if not exists
        SiteSettings.objects.get_or_create(pk=1)
        self.stdout.write(self.style.SUCCESS('✅ Site settings initialized'))
        
        # 4. Create demo package (Norway to Pakistan)
        package, created = Package.objects.get_or_create(
            tracking_number='DFX-2XWJFI8R',
            defaults={
                'sender': sender,
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
            self.stdout.write(self.style.SUCCESS(f'✅ Created demo package: {package.tracking_number}'))
            
            # 5. Add tracking history (passed locations)
            tracking_data = [
                ('Package Created', 'Oslo, Norway', 59.9139, 10.7522, 'Shipment registered'),
                ('In Transit', 'Gothenburg, Sweden', 57.7089, 11.9746, 'Crossed into Sweden'),
                ('In Transit', 'Copenhagen, Denmark', 55.6761, 12.5683, 'Denmark hub'),
                ('In Transit', 'Hamburg, Germany', 53.5511, 9.9937, 'German distribution'),
                ('In Transit', 'Prague, Czech Republic', 50.0755, 14.4378, 'Czech transit'),
                ('In Transit', 'Vienna, Austria', 48.2082, 16.3738, 'Austrian hub'),
                ('In Transit', 'Budapest, Hungary', 47.4979, 19.0402, 'Hungary transit'),
                ('In Transit', 'Bucharest, Romania', 44.4268, 26.1025, 'Romanian hub'),
                ('In Transit', 'Sofia, Bulgaria', 42.6977, 23.3219, 'Bulgaria transit'),
                ('In Transit', 'Istanbul, Turkey', 41.0082, 28.9784, 'Major transit hub'),
                ('In Transit', 'Ankara, Turkey', 39.9334, 32.8597, 'Central Turkey'),
                ('In Transit', 'Erzurum, Turkey', 39.9055, 41.2658, 'Eastern Turkey'),
                ('In Transit', 'Tabriz, Iran', 38.0962, 46.2738, 'Entered Iran'),
                ('In Transit', 'Tehran, Iran', 35.6892, 51.3890, 'Tehran hub'),
                ('In Transit', 'Isfahan, Iran', 32.6546, 51.6680, 'Central Iran'),
                ('In Transit', 'Kerman, Iran', 30.2839, 57.0834, 'Southeast Iran'),
                ('In Transit', 'Zahedan, Iran', 29.4963, 60.8629, 'At Pakistan border'),
            ]
            
            base_time = timezone.now() - timedelta(days=10)
            for i, (status, location, lat, lng, notes) in enumerate(tracking_data):
                TrackingHistory.objects.create(
                    package=package,
                    status=status,
                    location=location,
                    latitude=lat,
                    longitude=lng,
                    notes=notes,
                )
                # Manually update timestamp since auto_now_add
                th = package.tracking_history.filter(location=location).first()
                if th:
                    th.timestamp = base_time + timedelta(hours=i*6)
                    th.save(update_fields=['timestamp'])
            
            self.stdout.write(self.style.SUCCESS(f'✅ Added {len(tracking_data)} tracking history entries'))
            
            # 6. Add route waypoints (remaining route)
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
                    package=package,
                    city_name=city,
                    latitude=lat,
                    longitude=lng,
                    order=order,
                    is_passed=False,
                )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Added {len(waypoints)} route waypoints'))
        else:
            self.stdout.write('ℹ️  Demo package already exists')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Demo data seeding complete!'))
        self.stdout.write(f'\n📦 Track package at: /track/?q=DFX-2XWJFI8R')
        self.stdout.write(f'👤 Admin login: admin / admin123\n')
