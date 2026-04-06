"""Context processors for consignment app."""
from .models import SiteSettings


def site_settings(request):
    """Make site settings available to all templates as 'site_settings'."""
    return {
        'site_settings': SiteSettings.get_settings()
    }
