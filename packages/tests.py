from django.test import TestCase, Client
from django.urls import reverse
from django.template.loader import get_template
from django.contrib.auth import get_user_model

User = get_user_model()


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
