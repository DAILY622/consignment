from django.test import TestCase
from django.contrib.auth import get_user_model
from packages.models import Package
from .models import TrackingHistory

User = get_user_model()


class TrackingHistoryModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='trackuser', email='track@example.com', password='pass1234'
        )
        self.package = Package.objects.create(
            sender=self.user,
            sender_name='Test Sender',
            sender_address='1 Sender St',
            sender_phone='07700900000',
            sender_city='London',
            sender_postcode='SW1A 1AA',
            receiver_name='Test Receiver',
            receiver_address='2 Receiver Rd',
            receiver_phone='07700900001',
            receiver_city='Manchester',
            receiver_postcode='M1 1AE',
            weight=1.5,
        )

    def test_create_tracking_entry(self):
        entry = TrackingHistory.objects.create(
            package=self.package,
            status='In Transit',
            location='Birmingham Hub',
            notes='Arrived at sorting facility',
        )
        self.assertEqual(entry.package, self.package)
        self.assertEqual(entry.status, 'In Transit')
        self.assertEqual(entry.location, 'Birmingham Hub')

    def test_str_representation(self):
        entry = TrackingHistory.objects.create(
            package=self.package,
            status='Out for Delivery',
            location='Manchester',
        )
        result = str(entry)
        self.assertIn(self.package.tracking_number, result)
        self.assertIn('Out for Delivery', result)
        self.assertIn('Manchester', result)

    def test_ordering_latest_first(self):
        TrackingHistory.objects.create(package=self.package, status='Pending', location='Origin')
        TrackingHistory.objects.create(package=self.package, status='In Transit', location='Hub')
        entries = list(self.package.tracking_history.all())
        self.assertEqual(entries[0].status, 'In Transit')
        self.assertEqual(entries[1].status, 'Pending')

    def test_get_latest_location(self):
        entry1 = TrackingHistory.objects.create(package=self.package, status='Pending', location='Origin')
        entry2 = TrackingHistory.objects.create(package=self.package, status='In Transit', location='Hub')
        latest = self.package.get_latest_location()
        # get_latest_location returns the most recent entry regardless of coordinates
        self.assertIsNotNone(latest)
        self.assertEqual(latest.location, 'Hub')

    def test_get_latest_location_none_when_no_history(self):
        latest = self.package.get_latest_location()
        self.assertIsNone(latest)
