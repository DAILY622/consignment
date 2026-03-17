"""
URL configuration for consignment project.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .admin import admin_site
from accounts.views import register
from packages.views import home, track, dashboard, create_package
from drivers.views import driver_portal

urlpatterns = [
    path('admin/', admin_site.urls),
    
    # Public pages
    path('', home, name='home'),
    path('track/', track, name='track'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    
    # User dashboard
    path('dashboard/', dashboard, name='dashboard'),
    path('packages/create/', create_package, name='create_package'),
    
    # Driver portal
    path('driver/', driver_portal, name='driver_portal'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else '')
