"""
URL configuration for consignment project.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .admin import admin_site
from accounts.views import register, profile, about, contact, terms, privacy
from packages.views import home, track, dashboard, create_package, package_detail, package_edit, package_cancel
from drivers.views import driver_portal

urlpatterns = [
    path('admin/', admin_site.urls),
    
    # Public pages
    path('', home, name='home'),
    path('track/', track, name='track'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('terms/', terms, name='terms'),
    path('privacy/', privacy, name='privacy'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    
    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # User profile & dashboard
    path('profile/', profile, name='profile'),
    path('dashboard/', dashboard, name='dashboard'),
    
    # Package management
    path('packages/create/', create_package, name='create_package'),
    path('packages/<int:package_id>/', package_detail, name='package_detail'),
    path('packages/<int:package_id>/edit/', package_edit, name='package_edit'),
    path('packages/<int:package_id>/cancel/', package_cancel, name='package_cancel'),
    
    # Driver portal
    path('driver/', driver_portal, name='driver_portal'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else '')
