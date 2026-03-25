from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from packages.models import Package
from tracking.models import TrackingHistory
from .models import ProofOfDelivery

User = get_user_model()


def _make_package(sender, assigned_driver=None, status='pending'):
    """Helper to create a minimal Package for testing."""
    return Package.objects.create(
        sender=sender,
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
        weight=2.0,
        status=status,
        assigned_driver=assigned_driver,
    )


class DriverPortalAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = User.objects.create_user(
            username='customer', email='cust@example.com', password='pass1234', role='user'
        )
        self.driver = User.objects.create_user(
            username='driver1', email='driver@example.com', password='pass1234', role='driver'
        )

    def test_portal_redirects_unauthenticated(self):
        response = self.client.get(reverse('driver_portal'))
        self.assertRedirects(
            response, '/login/?next=/driver/', fetch_redirect_response=False
        )

    def test_portal_denies_non_driver(self):
        self.client.login(username='customer', password='pass1234')
        response = self.client.get(reverse('driver_portal'))
        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)

    def test_portal_accessible_to_driver(self):
        self.client.login(username='driver1', password='pass1234')
        response = self.client.get(reverse('driver_portal'))
        self.assertEqual(response.status_code, 200)


class DriverPortalUpdateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.sender = User.objects.create_user(
            username='sender', email='sender@example.com', password='pass1234', role='user'
        )
        self.driver = User.objects.create_user(
            username='driver2', email='driver2@example.com', password='pass1234', role='driver'
        )
        self.package = _make_package(
            sender=self.sender, assigned_driver=self.driver, status='in_transit'
        )
        self.client.login(username='driver2', password='pass1234')

    def test_update_status_to_out_for_delivery(self):
        response = self.client.post(reverse('driver_portal'), {
            'package_id': self.package.id,
            'status': 'out_for_delivery',
            'location': 'Manchester South',
        })
        self.assertRedirects(response, reverse('driver_portal'), fetch_redirect_response=False)
        self.package.refresh_from_db()
        self.assertEqual(self.package.status, 'out_for_delivery')
        self.assertTrue(
            TrackingHistory.objects.filter(package=self.package, status='Out for Delivery').exists()
        )

    def test_update_unassigned_package_gives_error(self):
        other_driver = User.objects.create_user(
            username='driver3', email='d3@example.com', password='pass1234', role='driver'
        )
        other_package = _make_package(
            sender=self.sender, assigned_driver=other_driver, status='in_transit'
        )
        response = self.client.post(reverse('driver_portal'), {
            'package_id': other_package.id,
            'status': 'out_for_delivery',
            'location': 'Somewhere',
        })
        self.assertRedirects(response, reverse('driver_portal'), fetch_redirect_response=False)
        other_package.refresh_from_db()
        self.assertEqual(other_package.status, 'in_transit')


class DriverHistoryTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.sender = User.objects.create_user(
            username='sender2', email='s2@example.com', password='pass1234', role='user'
        )
        self.driver = User.objects.create_user(
            username='driver4', email='d4@example.com', password='pass1234', role='driver'
        )
        _make_package(sender=self.sender, assigned_driver=self.driver, status='delivered')
        self.client.login(username='driver4', password='pass1234')

    def test_history_page_loads(self):
        response = self.client.get(reverse('driver_history'))
        self.assertEqual(response.status_code, 200)

    def test_history_denies_non_driver(self):
        customer = User.objects.create_user(
            username='customer2', email='c2@example.com', password='pass1234', role='user'
        )
        self.client.login(username='customer2', password='pass1234')
        response = self.client.get(reverse('driver_history'))
        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)

    def test_history_search(self):
        response = self.client.get(reverse('driver_history') + '?search=NOTFOUND')
        self.assertEqual(response.status_code, 200)


class ProofOfDeliveryModelTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username='s3', email='s3@example.com', password='pass1234', role='user'
        )
        self.driver = User.objects.create_user(
            username='d5', email='d5@example.com', password='pass1234', role='driver'
        )
        self.package = _make_package(
            sender=self.sender, assigned_driver=self.driver, status='delivered'
        )

    def test_create_pod(self):
        pod = ProofOfDelivery.objects.create(
            package=self.package,
            driver=self.driver,
            recipient_name='Test Receiver',
            notes='Left at door',
        )
        self.assertEqual(pod.package, self.package)
        self.assertIn(self.package.tracking_number, str(pod))
