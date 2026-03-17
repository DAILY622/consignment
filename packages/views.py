from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Package
from tracking.models import TrackingHistory


def home(request):
    return render(request, 'home.html')


def track(request):
    query = request.GET.get('q', '').strip()
    package = None
    tracking_history = []
    latest_location = None
    
    if query:
        package = Package.objects.filter(tracking_number__iexact=query).first()
        if package:
            tracking_history = package.tracking_history.all()
            latest_location = tracking_history.filter(latitude__isnull=False).first()
    
    return render(request, 'track.html', {
        'query': query,
        'package': package,
        'tracking_history': tracking_history,
        'latest_location': latest_location,
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
    
    stats = {
        'total': Package.objects.filter(sender=request.user).count(),
        'pending': Package.objects.filter(sender=request.user, status='pending').count(),
        'in_transit': Package.objects.filter(sender=request.user, status__in=['processing', 'in_transit', 'out_for_delivery']).count(),
        'delivered': Package.objects.filter(sender=request.user, status='delivered').count(),
    }
    
    # Pagination
    paginator = Paginator(packages, 10)
    page = request.GET.get('page', 1)
    packages_page = paginator.get_page(page)
    
    return render(request, 'dashboard.html', {
        'packages': packages_page,
        'stats': stats,
        'search': search,
        'status_filter': status_filter,
    })


@login_required
def create_package(request):
    if request.method == 'POST':
        # Validation
        required_fields = ['sender_name', 'sender_address', 'sender_phone', 'sender_city', 
                          'sender_postcode', 'receiver_name', 'receiver_address', 
                          'receiver_phone', 'receiver_city', 'receiver_postcode', 'weight']
        
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
        
        if errors:
            messages.error(request, ' | '.join(errors))
            return render(request, 'create_package.html')
        
        package = Package.objects.create(
            sender=request.user,
            sender_name=request.POST.get('sender_name').strip(),
            sender_address=request.POST.get('sender_address').strip(),
            sender_phone=request.POST.get('sender_phone').strip(),
            sender_city=request.POST.get('sender_city').strip(),
            sender_postcode=request.POST.get('sender_postcode').strip().upper(),
            receiver_name=request.POST.get('receiver_name').strip(),
            receiver_address=request.POST.get('receiver_address').strip(),
            receiver_phone=request.POST.get('receiver_phone').strip(),
            receiver_city=request.POST.get('receiver_city').strip(),
            receiver_postcode=request.POST.get('receiver_postcode').strip().upper(),
            weight=weight,
            length=request.POST.get('length') or None,
            width=request.POST.get('width') or None,
            height=request.POST.get('height') or None,
            description=request.POST.get('description', '').strip(),
        )
        
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
        package.receiver_name = request.POST.get('receiver_name', '').strip()
        package.receiver_phone = request.POST.get('receiver_phone', '').strip()
        package.receiver_address = request.POST.get('receiver_address', '').strip()
        package.receiver_city = request.POST.get('receiver_city', '').strip()
        package.receiver_postcode = request.POST.get('receiver_postcode', '').strip().upper()
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
