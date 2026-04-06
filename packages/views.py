from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count, Q, Case, When, IntegerField
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import re
from .models import Package, generate_tracking_number, GLOBAL_CITY_COORDS
from tracking.models import TrackingHistory

# Global postal code patterns by country (supports international shipping)
POSTAL_PATTERNS = {
    'United Kingdom': r'^[A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2}$',
    'Norway': r'^\d{4}$',
    'Pakistan': r'^\d{5}$',
    'United States': r'^\d{5}(-\d{4})?$',
    'Canada': r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$',
    'Germany': r'^\d{5}$',
    'France': r'^\d{5}$',
    'Australia': r'^\d{4}$',
    'India': r'^\d{6}$',
    'Japan': r'^\d{3}-?\d{4}$',
    'China': r'^\d{6}$',
    'Brazil': r'^\d{5}-?\d{3}$',
    'Netherlands': r'^\d{4}\s?[A-Z]{2}$',
    'Italy': r'^\d{5}$',
    'Spain': r'^\d{5}$',
    'UAE': r'^.*$',  # UAE doesn't have standard postal codes
    'Singapore': r'^\d{6}$',
}


def validate_postal_code(postcode, country):
    """Validate postal code based on country. Returns True if valid or country not in pattern list."""
    if not postcode:
        return False
    pattern = POSTAL_PATTERNS.get(country)
    if not pattern:
        # Accept any format for countries not in the list
        return len(postcode.strip()) >= 2
    return bool(re.match(pattern, postcode.strip().upper(), re.IGNORECASE))


def home(request):
    if request.method == 'POST':
        # Newsletter subscription
        newsletter_email = request.POST.get('newsletter_email', '').strip()
        if newsletter_email:
            messages.success(request, 'Thank you for subscribing to our newsletter!')
        return redirect('home')
    return render(request, 'home.html')


def track(request):
    """Public tracking view - shows status and location only (no PII)"""
    from consignment.models import SiteSettings
    
    query = request.GET.get('q', '').strip()
    package = None
    tracking_history = []
    latest_location = None
    route_waypoints = []
    
    if query:
        package = Package.objects.filter(tracking_number__iexact=query).first()
        if package:
            tracking_history = package.tracking_history.all()
            latest_location = tracking_history.filter(latitude__isnull=False).first()
            # Get admin-defined route waypoints for the map
            route_waypoints = list(package.route_waypoints.all().order_by('order').values(
                'city_name', 'latitude', 'longitude', 'is_passed', 'order'
            ))
    
    # Build safe package data (no PII exposed)
    safe_package = None
    if package:
        safe_package = {
            'tracking_number': package.tracking_number,
            'status': package.status,
            'status_display': package.get_status_display(),
            'sender_city': package.sender_city,
            'sender_country': package.sender_country,
            'receiver_city': package.receiver_city,
            'receiver_country': package.receiver_country,
            'estimated_delivery': package.estimated_delivery,
            'created_at': package.created_at,
        }
    
    # Get map settings from admin
    map_settings = SiteSettings.get_settings()
    
    return render(request, 'track.html', {
        'query': query,
        'package': package,
        'safe_package': safe_package,
        'tracking_history': tracking_history,
        'latest_location': latest_location,
        'city_coords': GLOBAL_CITY_COORDS,
        'route_waypoints': route_waypoints,
        'map_settings': map_settings,
    })


@login_required
def dashboard(request):
    packages = Package.objects.filter(sender=request.user)
    
    # Search and Filter
    search = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '')
    
    if search:
        packages = packages.filter(
            Q(tracking_number__icontains=search) |
            Q(receiver_name__icontains=search) |
            Q(receiver_city__icontains=search)
        )
    
    if status_filter:
        packages = packages.filter(status=status_filter)

    # Use a single annotated query instead of 4 separate COUNT queries (#8)
    stats_qs = Package.objects.filter(sender=request.user).aggregate(
        total=Count('id'),
        pending=Count(Case(When(status='pending', then=1), output_field=IntegerField())),
        in_transit=Count(Case(
            When(status__in=['processing', 'in_transit', 'out_for_delivery'], then=1),
            output_field=IntegerField()
        )),
        delivered=Count(Case(When(status='delivered', then=1), output_field=IntegerField())),
    )
    stats = stats_qs

    # Active packages for map (#7) - include pending so pins appear on map
    active_packages = Package.objects.filter(
        sender=request.user,
        status__in=['pending', 'processing', 'in_transit', 'out_for_delivery']
    ).values('tracking_number', 'status', 'receiver_name', 'receiver_city', 'receiver_postcode')
    
    # Pagination
    paginator = Paginator(packages, 10)
    page = request.GET.get('page', 1)
    packages_page = paginator.get_page(page)
    
    return render(request, 'dashboard.html', {
        'packages': packages_page,
        'stats': stats,
        'search': search,
        'status_filter': status_filter,
        'active_packages': active_packages,
    })


@login_required
def create_package(request):
    if request.method == 'POST':
        # Validation
        required_fields = ['sender_name', 'sender_address', 'sender_phone', 'sender_city', 
                          'sender_country', 'sender_postcode', 'receiver_name', 'receiver_address', 
                          'receiver_phone', 'receiver_city', 'receiver_country', 'receiver_postcode', 'weight']
        
        errors = []
        for field in required_fields:
            if not request.POST.get(field, '').strip():
                errors.append(f'{field.replace("_", " ").title()} is required')
        
        try:
            weight = float(request.POST.get('weight', 0))
            if weight <= 0:
                errors.append('Weight must be greater than 0')
        except ValueError:
            errors.append('Invalid weight value')

        # Global postal code validation
        sender_country = request.POST.get('sender_country', '').strip()
        receiver_country = request.POST.get('receiver_country', '').strip()
        
        sender_postcode = request.POST.get('sender_postcode', '').strip().upper()
        if sender_postcode and not validate_postal_code(sender_postcode, sender_country):
            errors.append(f'Sender Postcode does not appear valid for {sender_country}')
        
        receiver_postcode = request.POST.get('receiver_postcode', '').strip().upper()
        if receiver_postcode and not validate_postal_code(receiver_postcode, receiver_country):
            errors.append(f'Receiver Postcode does not appear valid for {receiver_country}')
        
        if errors:
            messages.error(request, ' | '.join(errors))
            return render(request, 'create_package.html')
        
        # Calculate delivery estimate based on international/domestic
        is_international = sender_country != receiver_country
        delivery_days = 7 if is_international else 3  # 7 days international, 3 days domestic
        
        # Retry on tracking number collision (rare but possible with cryptographic generation)
        for _attempt in range(5):
            try:
                # Estimate delivery (skip weekends)
                estimated = timezone.now().date()
                working_days = 0
                while working_days < delivery_days:
                    estimated += timedelta(days=1)
                    if estimated.weekday() < 5:  # Mon-Fri
                        working_days += 1

                package = Package.objects.create(
                    sender=request.user,
                    tracking_number=generate_tracking_number(),
                    sender_name=request.POST.get('sender_name').strip(),
                    sender_address=request.POST.get('sender_address').strip(),
                    sender_phone=request.POST.get('sender_phone').strip(),
                    sender_city=request.POST.get('sender_city').strip(),
                    sender_country=sender_country,
                    sender_postcode=sender_postcode,
                    receiver_name=request.POST.get('receiver_name').strip(),
                    receiver_address=request.POST.get('receiver_address').strip(),
                    receiver_phone=request.POST.get('receiver_phone').strip(),
                    receiver_city=request.POST.get('receiver_city').strip(),
                    receiver_country=receiver_country,
                    receiver_postcode=receiver_postcode,
                    weight=weight,
                    length=request.POST.get('length') or None,
                    width=request.POST.get('width') or None,
                    height=request.POST.get('height') or None,
                    description=request.POST.get('description', '').strip(),
                    estimated_delivery=estimated,
                )
                break
            except IntegrityError:
                continue
        else:
            messages.error(request, 'Failed to generate a unique tracking number. Please try again.')
            return render(request, 'create_package.html')
        
        # Create initial tracking entry
        TrackingHistory.objects.create(
            package=package,
            status='Package Created',
            location=f"{package.sender_city}, {package.sender_postcode}",
            notes='Shipment registered in system'
        )
        
        messages.success(request, f'Package created! Tracking number: {package.tracking_number}')
        return redirect('package_detail', package_id=package.id)
    
    return render(request, 'create_package.html')


@login_required
def package_detail(request, package_id):
    package = get_object_or_404(Package, id=package_id, sender=request.user)
    tracking_history = package.tracking_history.all()
    
    return render(request, 'package_detail.html', {
        'package': package,
        'tracking_history': tracking_history,
    })


@login_required
def package_edit(request, package_id):
    package = get_object_or_404(Package, id=package_id, sender=request.user)
    
    # Only allow editing pending packages
    if package.status != 'pending':
        messages.error(request, 'You can only edit packages that are still pending.')
        return redirect('package_detail', package_id=package.id)
    
    if request.method == 'POST':
        receiver_postcode = request.POST.get('receiver_postcode', '').strip().upper()
        receiver_country = request.POST.get('receiver_country', package.receiver_country).strip()

        # International postcode validation (consistent with create_package)
        if receiver_postcode and not validate_postal_code(receiver_postcode, receiver_country):
            messages.error(request, f'Receiver Postcode does not appear valid for {receiver_country}')
            return render(request, 'package_edit.html', {'package': package})

        package.receiver_name = request.POST.get('receiver_name', '').strip()
        package.receiver_phone = request.POST.get('receiver_phone', '').strip()
        package.receiver_address = request.POST.get('receiver_address', '').strip()
        package.receiver_city = request.POST.get('receiver_city', '').strip()
        package.receiver_country = receiver_country
        package.receiver_postcode = receiver_postcode
        package.description = request.POST.get('description', '').strip()
        package.save()

        messages.success(request, 'Package details updated!')
        return redirect('package_detail', package_id=package.id)

    return render(request, 'package_edit.html', {'package': package})


@login_required
def package_cancel(request, package_id):
    package = get_object_or_404(Package, id=package_id, sender=request.user)
    
    if package.status != 'pending':
        messages.error(request, 'Only pending packages can be cancelled.')
        return redirect('package_detail', package_id=package.id)
    
    if request.method == 'POST':
        package.status = 'cancelled'
        package.save()
        
        TrackingHistory.objects.create(
            package=package,
            status='Cancelled',
            location='N/A',
            notes='Cancelled by customer'
        )
        
        messages.success(request, f'Package {package.tracking_number} has been cancelled.')
        return redirect('dashboard')
    
    return redirect('package_detail', package_id=package.id)
