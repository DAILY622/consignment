from django.test import TestCase, Client
from django.urls import reverse
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def _make_package(user, **kwargs):
    """Helper to create a minimal Package for testing."""
    from packages.models import Package
    defaults = dict(
        sender=user,
        sender_name='Test Sender',
        sender_address='1 Test St',
        sender_phone='07700900000',
        sender_city='London',
        sender_postcode='SW1A 1AA',
        receiver_name='Test Receiver',
        receiver_address='2 Test Rd',
        receiver_phone='07700900001',
        receiver_city='Manchester',
        receiver_postcode='M1 1AE',
        weight=2.0,
    )
    defaults.update(kwargs)
    return Package.objects.create(**defaults)


class TemplateLoadTests(TestCase):
    """Verify every template can be loaded (no broken extends/load tags)."""

    TEMPLATES = [
        'home.html', 'track.html', 'about.html', 'contact.html',
        'terms.html', 'privacy.html', 'services.html', 'fleet.html',
        'pricing.html', 'faq.html', 'careers.html', 'dashboard.html',
        'package_detail.html', 'profile.html', 'register.html',
        '404.html', '500.html', 'driver_portal.html', 'driver_history.html',
        'create_package.html', 'package_edit.html',
        'registration/login.html', 'registration/password_reset.html',
        'admin/index.html', 'admin/packages/update_location.html',
    ]

    def test_all_templates_load(self):
        for tname in self.TEMPLATES:
            with self.subTest(template=tname):
                # Should not raise TemplateSyntaxError or any exception
                get_template(tname)


class PublicPageTests(TestCase):
    """Smoke-test every public URL returns HTTP 200."""

    def setUp(self):
        self.client = Client()

    def _get_200(self, url_name, **kwargs):
        url = reverse(url_name, **kwargs)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200,
            msg=f"Expected 200 for '{url_name}', got {response.status_code}",
        )
        return response

    def test_home(self):       self._get_200('home')
    def test_track(self):      self._get_200('track')
    def test_about(self):      self._get_200('about')
    def test_contact(self):    self._get_200('contact')
    def test_terms(self):      self._get_200('terms')
    def test_privacy(self):    self._get_200('privacy')
    def test_services(self):   self._get_200('services')
    def test_fleet(self):      self._get_200('fleet')
    def test_pricing(self):    self._get_200('pricing')
    def test_faq(self):        self._get_200('faq')
    def test_careers(self):    self._get_200('careers')
    def test_login_page(self): self._get_200('login')
    def test_register(self):   self._get_200('register')

    def test_track_with_query(self):
        url = reverse('track') + '?q=ECG-NOTFOUND'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_redirects_when_unauthenticated(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/', fetch_redirect_response=False)

    def test_create_package_redirects_when_unauthenticated(self):
        response = self.client.get(reverse('create_package'))
        self.assertRedirects(response, '/login/?next=/packages/create/', fetch_redirect_response=False)

    def test_driver_portal_redirects_when_unauthenticated(self):
        response = self.client.get(reverse('driver_portal'))
        self.assertRedirects(response, '/login/?next=/driver/', fetch_redirect_response=False)


class AuthenticatedPageTests(TestCase):
    """Pages that require login."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', email='t@test.com',
        )
        self.client.login(username='testuser', password='testpass123')

    def test_dashboard(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_create_package_get(self):
        response = self.client.get(reverse('create_package'))
        self.assertEqual(response.status_code, 200)


class CreatePackageTests(TestCase):
    """Tests for the create_package POST flow."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='creator', email='creator@test.com', password='testpass123',
        )
        self.client.login(username='creator', password='testpass123')
        self.url = reverse('create_package')
        self.valid_data = {
            'sender_name': 'John Sender',
            'sender_address': '1 Sender St',
            'sender_phone': '07700900000',
            'sender_city': 'London',
            'sender_postcode': 'SW1A 1AA',
            'receiver_name': 'Jane Receiver',
            'receiver_address': '2 Receiver Rd',
            'receiver_phone': '07700900001',
            'receiver_city': 'Manchester',
            'receiver_postcode': 'M1 1AE',
            'weight': '2.5',
        }

    def test_create_package_success(self):
        response = self.client.post(self.url, self.valid_data)
        from packages.models import Package
        pkg = Package.objects.filter(sender=self.user).first()
        self.assertIsNotNone(pkg)
        self.assertRedirects(
            response, reverse('package_detail', args=[pkg.id]),
            fetch_redirect_response=False,
        )

    def test_create_package_sets_tracking_number(self):
        self.client.post(self.url, self.valid_data)
        from packages.models import Package
        pkg = Package.objects.filter(sender=self.user).first()
        self.assertTrue(pkg.tracking_number.startswith('ECG-'))

    def test_create_package_sets_estimated_delivery(self):
        self.client.post(self.url, self.valid_data)
        from packages.models import Package
        pkg = Package.objects.filter(sender=self.user).first()
        self.assertIsNotNone(pkg.estimated_delivery)
        # Should be at least 1 day in the future
        self.assertGreater(pkg.estimated_delivery, timezone.now().date())

    def test_create_package_invalid_sender_postcode(self):
        data = dict(self.valid_data, sender_postcode='INVALID')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        from packages.models import Package
        self.assertEqual(Package.objects.filter(sender=self.user).count(), 0)

    def test_create_package_invalid_receiver_postcode(self):
        data = dict(self.valid_data, receiver_postcode='NOTAPOSTCODE')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        from packages.models import Package
        self.assertEqual(Package.objects.filter(sender=self.user).count(), 0)

    def test_create_package_zero_weight(self):
        data = dict(self.valid_data, weight='0')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        from packages.models import Package
        self.assertEqual(Package.objects.filter(sender=self.user).count(), 0)

    def test_create_package_creates_initial_tracking_history(self):
        self.client.post(self.url, self.valid_data)
        from packages.models import Package
        from tracking.models import TrackingHistory
        pkg = Package.objects.filter(sender=self.user).first()
        history = TrackingHistory.objects.filter(package=pkg)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().status, 'Package Created')


class PackageCancelTests(TestCase):
    """Tests for the package_cancel view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='canceller', email='cancel@test.com', password='testpass123',
        )
        self.client.login(username='canceller', password='testpass123')

    def test_cancel_pending_package(self):
        pkg = _make_package(self.user, status='pending')
        response = self.client.post(reverse('package_cancel', args=[pkg.id]))
        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)
        pkg.refresh_from_db()
        self.assertEqual(pkg.status, 'cancelled')

    def test_cannot_cancel_in_transit_package(self):
        pkg = _make_package(self.user, status='in_transit')
        response = self.client.post(reverse('package_cancel', args=[pkg.id]))
        self.assertRedirects(
            response, reverse('package_detail', args=[pkg.id]),
            fetch_redirect_response=False,
        )
        pkg.refresh_from_db()
        self.assertEqual(pkg.status, 'in_transit')

    def test_cancel_adds_tracking_history(self):
        from tracking.models import TrackingHistory
        pkg = _make_package(self.user, status='pending')
        self.client.post(reverse('package_cancel', args=[pkg.id]))
        self.assertTrue(
            TrackingHistory.objects.filter(package=pkg, status='Cancelled').exists()
        )


class PackageEditTests(TestCase):
    """Tests for the package_edit view (postcode validation added in previous session)."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='editor', email='edit@test.com', password='testpass123',
        )
        self.client.login(username='editor', password='testpass123')
        self.pkg = _make_package(self.user, status='pending')

    def test_edit_pending_package_success(self):
        response = self.client.post(
            reverse('package_edit', args=[self.pkg.id]),
            {
                'receiver_name': 'Updated Receiver',
                'receiver_phone': '07700900002',
                'receiver_address': '3 New St',
                'receiver_city': 'Leeds',
                'receiver_postcode': 'LS1 1UR',
                'description': 'Updated description',
            },
        )
        self.assertRedirects(
            response, reverse('package_detail', args=[self.pkg.id]),
            fetch_redirect_response=False,
        )
        self.pkg.refresh_from_db()
        self.assertEqual(self.pkg.receiver_name, 'Updated Receiver')
        self.assertEqual(self.pkg.receiver_postcode, 'LS1 1UR')

    def test_edit_invalid_postcode_rejected(self):
        response = self.client.post(
            reverse('package_edit', args=[self.pkg.id]),
            {
                'receiver_name': 'Bad Postcode',
                'receiver_phone': '07700900000',
                'receiver_address': '1 Test St',
                'receiver_city': 'London',
                'receiver_postcode': 'INVALID123',
                'description': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.pkg.refresh_from_db()
        self.assertEqual(self.pkg.receiver_postcode, 'M1 1AE')  # unchanged

    def test_cannot_edit_in_transit_package(self):
        self.pkg.status = 'in_transit'
        self.pkg.save()
        response = self.client.post(
            reverse('package_edit', args=[self.pkg.id]),
            {
                'receiver_name': 'New Receiver',
                'receiver_phone': '07700900000',
                'receiver_address': '1 Test St',
                'receiver_city': 'London',
                'receiver_postcode': 'SW1A 1AA',
            },
        )
        self.assertRedirects(
            response, reverse('package_detail', args=[self.pkg.id]),
            fetch_redirect_response=False,
        )
        self.pkg.refresh_from_db()
        self.assertEqual(self.pkg.receiver_name, 'Test Receiver')  # unchanged
