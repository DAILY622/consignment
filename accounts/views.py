from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings

import re
from .models import User
from packages.models import Package

# Validation constants
UK_PHONE_RE = re.compile(r'^(\+44|0)[1-9]\d{8,10}$')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        errors = []
        
        if not username or not email or not password:
            errors.append('All required fields must be filled')
        
        if password != password2:
            errors.append('Passwords do not match')
        
        if len(password) < 8:
            errors.append('Password must be at least 8 characters')

        # Email format validation (#15)
        try:
            validate_email(email)
        except ValidationError:
            errors.append('Please enter a valid email address')

        # Phone format validation (#17)
        if phone and not UK_PHONE_RE.match(phone.replace(' ', '')):
            errors.append('Please enter a valid UK phone number (e.g. 07700900000 or +447700900000)')

        # Use a single generic message to prevent user enumeration (#5)
        if not errors:
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                errors.append('An account with that username or email already exists')
        
        if errors:
            return render(request, 'register.html', {'errors': errors})
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role='user'
        )
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('dashboard')
    
    return render(request, 'register.html')


@login_required
def profile(request):
    user = request.user
    
    # Get user stats
    packages = Package.objects.filter(sender=user)
    stats = {
        'total': packages.count(),
        'delivered': packages.filter(status='delivered').count(),
        'in_transit': packages.filter(status__in=['processing', 'in_transit', 'out_for_delivery']).count(),
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            new_email = request.POST.get('email', '').strip()
            new_phone = request.POST.get('phone', '').strip()

            # Validate email format
            try:
                validate_email(new_email)
            except ValidationError:
                messages.error(request, 'Please enter a valid email address')
                return redirect('profile')

            # Validate UK phone format if provided
            if new_phone and not UK_PHONE_RE.match(new_phone.replace(' ', '')):
                messages.error(request, 'Please enter a valid UK phone number (e.g. 07700900000 or +447700900000)')
                return redirect('profile')

            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name = request.POST.get('last_name', '').strip()
            user.email = new_email
            user.phone = new_phone
            user.address = request.POST.get('address', '').strip()
            user.save()
            messages.success(request, 'Profile updated successfully!')
            
        elif action == 'change_password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully!')
                
        elif action == 'delete_account':
            confirm_password = request.POST.get('confirm_delete_password', '')
            if not confirm_password or not user.check_password(confirm_password):
                messages.error(request, 'Incorrect password. Account not deleted.')
                return redirect('profile')
            user.delete()
            messages.success(request, 'Your account has been deleted')
            return redirect('home')
        
        return redirect('profile')
    
    return render(request, 'profile.html', {'stats': stats})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        tracking_number = request.POST.get('tracking_number', '').strip()

        if not name or not email or not subject or not message:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'contact.html')

        full_subject = f'Contact Form: {subject}'
        full_message = (
            f'Name: {name}\n'
            f'Email: {email}\n'
            f'Tracking Number: {tracking_number or "N/A"}\n\n'
            f'Message:\n{message}'
        )
        recipient = getattr(settings, 'CONTACT_EMAIL', 'support@e-cognite.com')
        try:
            send_mail(
                full_subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient],
                fail_silently=False,
            )
            messages.success(request, 'Thank you for your message! We will get back to you within 24 hours.')
        except Exception:
            messages.error(request, 'There was a problem sending your message. Please try again later.')
        return redirect('contact')
    
    return render(request, 'contact.html')


def terms(request):
    return render(request, 'terms.html')


def privacy(request):
    return render(request, 'privacy.html')


def services(request):
    return render(request, 'services.html')


def fleet(request):
    return render(request, 'fleet.html')


def pricing(request):
    return render(request, 'pricing.html')


def faq(request):
    return render(request, 'faq.html')


def careers(request):
    return render(request, 'careers.html')
