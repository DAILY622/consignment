from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
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
    
    stats = {
        'total': packages.count(),
        'pending': packages.filter(status='pending').count(),
        'in_transit': packages.filter(status__in=['processing', 'in_transit', 'out_for_delivery']).count(),
        'delivered': packages.filter(status='delivered').count(),
    }
    
    return render(request, 'dashboard.html', {
        'packages': packages[:20],
        'stats': stats,
    })


@login_required
def create_package(request):
    if request.method == 'POST':
        package = Package.objects.create(
            sender=request.user,
            sender_name=request.POST.get('sender_name'),
            sender_address=request.POST.get('sender_address'),
            sender_phone=request.POST.get('sender_phone'),
            sender_city=request.POST.get('sender_city'),
            sender_postcode=request.POST.get('sender_postcode'),
            receiver_name=request.POST.get('receiver_name'),
            receiver_address=request.POST.get('receiver_address'),
            receiver_phone=request.POST.get('receiver_phone'),
            receiver_city=request.POST.get('receiver_city'),
            receiver_postcode=request.POST.get('receiver_postcode'),
            weight=request.POST.get('weight'),
            length=request.POST.get('length') or None,
            width=request.POST.get('width') or None,
            height=request.POST.get('height') or None,
            description=request.POST.get('description', ''),
        )
        
        # Create initial tracking entry
        TrackingHistory.objects.create(
            package=package,
            status='Package Created',
            location=f"{package.sender_city}, {package.sender_postcode}",
            notes='Shipment registered in system'
        )
        
        messages.success(request, f'Package created! Tracking number: {package.tracking_number}')
        return redirect('dashboard')
    
    return render(request, 'create_package.html')
