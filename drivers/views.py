from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from packages.models import Package
from tracking.models import TrackingHistory
from .models import ProofOfDelivery

# Allowed image formats verified by Pillow
ALLOWED_IMAGE_FORMATS = {'JPEG', 'PNG', 'GIF', 'WEBP'}


def _validate_upload(file_obj):
    """Return an error string if the uploaded file is not an allowed image, or None if valid.
    Uses Pillow to inspect actual file content rather than trusting the client Content-Type."""
    if file_obj is None:
        return None
    try:
        from PIL import Image
        img = Image.open(file_obj)
        img.verify()
        file_obj.seek(0)
        if img.format not in ALLOWED_IMAGE_FORMATS:
            return f'Invalid image format "{img.format}". Only JPEG, PNG, GIF and WebP images are accepted.'
    except Exception:
        return 'Uploaded file is not a valid image. Only JPEG, PNG, GIF and WebP images are accepted.'
    return None


@login_required
def driver_portal(request):
    if request.user.role != 'driver' and not request.user.is_superuser:
        messages.error(request, 'Access denied. Driver account required.')
        return redirect('dashboard')
    
    assigned_packages = Package.objects.filter(
        assigned_driver=request.user
    ).exclude(status='delivered').exclude(status='cancelled').order_by('-created_at')
    
    # Stats for driver
    today = timezone.now().date()
    stats = {
        'assigned': assigned_packages.count(),
        'delivered_today': Package.objects.filter(
            assigned_driver=request.user, 
            status='delivered',
            updated_at__date=today
        ).count(),
        'delivered_total': Package.objects.filter(
            assigned_driver=request.user, 
            status='delivered'
        ).count(),
        'out_for_delivery': assigned_packages.filter(status='out_for_delivery').count(),
    }
    
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        status = request.POST.get('status')
        location = request.POST.get('location', '').strip()
        
        try:
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
                recipient_name = request.POST.get(f'recipient_name_{package_id}', '').strip()
                photo = request.FILES.get(f'photo_{package_id}')
                signature = request.FILES.get(f'signature_{package_id}')

                # Validate uploaded file types (#4)
                photo_err = _validate_upload(photo)
                sig_err = _validate_upload(signature)
                if photo_err or sig_err:
                    messages.error(request, photo_err or sig_err)
                    return redirect('driver_portal')

                # Use get_or_create to prevent duplicate POD race condition (#9)
                ProofOfDelivery.objects.get_or_create(
                    package=package,
                    defaults=dict(
                        driver=request.user,
                        recipient_name=recipient_name or package.receiver_name,
                        photo=photo,
                        signature=signature,
                        notes=request.POST.get(f'notes_{package_id}', '').strip(),
                        latitude=request.POST.get(f'latitude_{package_id}') or None,
                        longitude=request.POST.get(f'longitude_{package_id}') or None,
                    )
                )
            
            messages.success(request, f'Package {package.tracking_number} updated to {package.get_status_display()}')
        except Package.DoesNotExist:
            messages.error(request, 'Package not found or not assigned to you.')
        
        return redirect('driver_portal')
    
    return render(request, 'driver_portal.html', {
        'assigned_packages': assigned_packages,
        'stats': stats,
    })


@login_required
def driver_history(request):
    if request.user.role != 'driver' and not request.user.is_superuser:
        messages.error(request, 'Access denied. Driver account required.')
        return redirect('dashboard')
    
    # Get all delivered packages by this driver
    delivered_packages = Package.objects.filter(
        assigned_driver=request.user,
        status='delivered'
    ).select_related('proof_of_delivery').order_by('-updated_at')
    
    # Search functionality
    search = request.GET.get('search', '').strip()
    if search:
        delivered_packages = delivered_packages.filter(
            Q(tracking_number__icontains=search) |
            Q(receiver_name__icontains=search) |
            Q(receiver_city__icontains=search)
        )
    
    # Date filter
    date_filter = request.GET.get('date', '')
    if date_filter:
        delivered_packages = delivered_packages.filter(updated_at__date=date_filter)
    
    # Stats
    today = timezone.now().date()
    this_week = today - timedelta(days=7)
    this_month = today - timedelta(days=30)
    
    stats = {
        'today': Package.objects.filter(assigned_driver=request.user, status='delivered', updated_at__date=today).count(),
        'this_week': Package.objects.filter(assigned_driver=request.user, status='delivered', updated_at__date__gte=this_week).count(),
        'this_month': Package.objects.filter(assigned_driver=request.user, status='delivered', updated_at__date__gte=this_month).count(),
        'all_time': Package.objects.filter(assigned_driver=request.user, status='delivered').count(),
    }
    
    # Pagination
    paginator = Paginator(delivered_packages, 15)
    page = request.GET.get('page', 1)
    packages_page = paginator.get_page(page)
    
    return render(request, 'driver_history.html', {
        'packages': packages_page,
        'stats': stats,
        'search': search,
        'date_filter': date_filter,
    })
