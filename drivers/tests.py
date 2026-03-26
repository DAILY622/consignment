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


class DeliveryWithSignatureTests(TestCase):
    """Tests for the signature base64 fix: canvas data submitted in POST, not FILES."""

    def setUp(self):
        self.client = Client()
        self.sender = User.objects.create_user(
            username='sndr_sig', email='sndr@example.com', password='pass1234', role='user'
        )
        self.driver = User.objects.create_user(
            username='drvr_sig', email='drvr@example.com', password='pass1234', role='driver'
        )
        self.package = _make_package(
            sender=self.sender, assigned_driver=self.driver, status='out_for_delivery'
        )
        self.client.login(username='drvr_sig', password='pass1234')

    def _minimal_png_b64(self):
        """Return a valid 1×1 white PNG as a base64 data URL (generated via struct/zlib)."""
        import struct, zlib, base64

        def u32(n):
            return struct.pack('>I', n)

        def chunk(name, data):
            c = name + data
            return u32(len(data)) + c + u32(zlib.crc32(c) & 0xFFFFFFFF)

        sig = b'\x89PNG\r\n\x1a\n'
        ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
        idat = chunk(b'IDAT', zlib.compress(b'\x00\xff\xff\xff'))
        iend = chunk(b'IEND', b'')
        png = sig + ihdr + idat + iend
        return 'data:image/png;base64,' + base64.b64encode(png).decode()

    def test_deliver_with_base64_signature_creates_pod(self):
        """Delivering a package with a base64 canvas signature saves the POD."""
        pkg_id = self.package.id
        response = self.client.post(
            reverse('driver_portal'),
            {
                'package_id': pkg_id,
                'status': 'delivered',
                'location': 'Manchester City Centre',
                f'recipient_name_{pkg_id}': 'Jane Doe',
                f'signature_{pkg_id}': self._minimal_png_b64(),
                f'notes_{pkg_id}': 'Delivered to front door',
            },
        )
        self.assertRedirects(response, reverse('driver_portal'), fetch_redirect_response=False)
        self.package.refresh_from_db()
        self.assertEqual(self.package.status, 'delivered')
        pod = ProofOfDelivery.objects.filter(package=self.package).first()
        self.assertIsNotNone(pod, 'ProofOfDelivery should be created on delivery')
        self.assertEqual(pod.recipient_name, 'Jane Doe')
        self.assertTrue(bool(pod.signature), 'Signature file should be saved')

    def test_deliver_without_signature_still_creates_pod(self):
        """Delivering without a signature (empty canvas data) should still create POD."""
        pkg_id = self.package.id
        response = self.client.post(
            reverse('driver_portal'),
            {
                'package_id': pkg_id,
                'status': 'delivered',
                'location': 'Manchester',
                f'recipient_name_{pkg_id}': 'Bob Smith',
                f'signature_{pkg_id}': '',  # No signature drawn
            },
        )
        self.assertRedirects(response, reverse('driver_portal'), fetch_redirect_response=False)
        self.package.refresh_from_db()
        self.assertEqual(self.package.status, 'delivered')
        pod = ProofOfDelivery.objects.filter(package=self.package).first()
        self.assertIsNotNone(pod, 'ProofOfDelivery should be created even without signature')
        self.assertFalse(bool(pod.signature), 'Signature should be empty/None when not provided')
