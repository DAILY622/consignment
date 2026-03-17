from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from packages.models import Package
from tracking.models import TrackingHistory
from .models import ProofOfDelivery


@login_required
def driver_portal(request):
    if request.user.role != 'driver' and not request.user.is_superuser:
        messages.error(request, 'Access denied. Driver account required.')
        return redirect('dashboard')
    
    assigned_packages = Package.objects.filter(
        assigned_driver=request.user
    ).exclude(status='delivered').exclude(status='cancelled')
    
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        status = request.POST.get('status')
        location = request.POST.get('location', '')
        
        package = Package.objects.get(id=package_id, assigned_driver=request.user)
        package.status = status
        package.save()
        
        # Create tracking entry
        TrackingHistory.objects.create(
            package=package,
            status=package.get_status_display(),
            location=location or package.receiver_city,
            latitude=request.POST.get(f'latitude_{package_id}') or None,
            longitude=request.POST.get(f'longitude_{package_id}') or None,
        )
        
        # If delivered, create proof of delivery
        if status == 'delivered':
            ProofOfDelivery.objects.create(
                package=package,
                driver=request.user,
                recipient_name=request.POST.get(f'recipient_name_{package_id}', package.receiver_name),
                photo=request.FILES.get(f'photo_{package_id}'),
                notes=request.POST.get(f'notes_{package_id}', ''),
                latitude=request.POST.get(f'latitude_{package_id}') or None,
                longitude=request.POST.get(f'longitude_{package_id}') or None,
            )
        
        messages.success(request, f'Package {package.tracking_number} updated to {package.get_status_display()}')
        return redirect('driver_portal')
    
    return render(request, 'driver_portal.html', {
        'assigned_packages': assigned_packages,
    })
