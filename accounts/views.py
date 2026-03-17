from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import User
from packages.models import Package


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
        
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists')
        
        if User.objects.filter(email=email).exists():
            errors.append('Email already registered')
        
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
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name = request.POST.get('last_name', '').strip()
            user.email = request.POST.get('email', '').strip()
            user.phone = request.POST.get('phone', '').strip()
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
            user.delete()
            messages.success(request, 'Your account has been deleted')
            return redirect('home')
        
        return redirect('profile')
    
    return render(request, 'profile.html', {'stats': stats})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        # In production, you would send an email here
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        tracking_number = request.POST.get('tracking_number', '')
        
        # For now, just show success message
        messages.success(request, 'Thank you for your message! We will get back to you within 24 hours.')
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


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if User.objects.filter(email=email).exists():
            # In production, send actual email with reset link
            messages.success(request, 'If an account exists with this email, you will receive a reset link.')
        else:
            messages.success(request, 'If an account exists with this email, you will receive a reset link.')
        return redirect('password_reset_done')
    return render(request, 'registration/password_reset.html')
