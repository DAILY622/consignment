# 📦 Seed Production Data - Demo Packages

## Using Django Admin (Easiest - No CLI Needed!)

### Option 1: Via Admin Panel (Recommended) ✅

1. **Login to Admin Panel**
   - Visit: https://consignment-site-2ac0cae70da0.herokuapp.com/admin/
   - Login with your superuser credentials

2. **Create Demo Package**
   - Click **"Packages"**
   - Click **"Add Package"** button (top-right)
   - Fill in details:
     - **Tracking Number**: Auto-generated (DFX-XXXXXXXX)
     - **Sender**: John Doe, Oslo, Norway
     - **Recipient**: Jane Smith, Lahore, Pakistan
     - **Status**: In Transit
     - **Dimensions**: 30cm x 20cm x 15cm, 2.5kg
     - **Current Location**: Add coordinates (29.4963, 60.8629)
   - Click **"Save"**

3. **Add Tracking History**
   - In the same package form, scroll to **"Tracking History"**
   - Click **"Add Another Tracking History"**
   - Add waypoints:
     - Oslo, Norway (59.9139, 10.7522)
     - Stockholm, Sweden (59.3293, 18.0686)
     - Warsaw, Poland (52.2297, 21.0122)
     - Kyiv, Ukraine (50.4501, 30.5234)
     - Bucharest, Romania (44.4268, 26.1025)
     - Istanbul, Turkey (41.0082, 28.9784)
     - Tehran, Iran (35.6892, 51.3890)
     - Zahedan, Iran (29.4963, 60.8629) ← Current
     - Quetta, Pakistan (30.1798, 66.9750)
     - Lahore, Pakistan (31.5497, 74.3436) ← Destination

4. **Test Tracking**
   - Copy the tracking number
   - Visit: https://consignment-site-2ac0cae70da0.herokuapp.com/track/
   - Paste tracking number
   - View enhanced map with all waypoints!

---

## Using Management Commands (CLI Method)

### Option 2: Run Seed Command via Heroku

```bash
heroku run python manage.py seed_data --app consignment-site-2ac0cae70da0
```

This creates:
- ✅ 10 demo packages (ECG-DEMO0000 through ECG-DEMO0009)
- ✅ Sample users (admin, customer, driver)
- ✅ Tracking history for each package
- ✅ Various statuses (pending, in transit, delivered)

### Option 3: Create Custom Demo Package

```bash
heroku run python manage.py create_demo_package --app consignment-site-2ac0cae70da0
```

Creates the Norway → Pakistan demo package with full route.

---

## Quick Test Packages

After seeding, try these tracking numbers:

| Tracking Number | Route | Status |
|----------------|-------|--------|
| **ECG-DEMO0000** | London → Manchester | Delivered |
| **ECG-DEMO0001** | Edinburgh → Glasgow | In Transit |
| **ECG-DEMO0002** | Cardiff → Bristol | Pending |
| **ECG-DEMO0003** | Belfast → Dublin | In Transit |
| **ECG-DEMO0004** | London → Paris | In Transit |
| **DFX-XXXXXXXX** | Custom package | (Your creation) |

---

## Manual Package Creation via Shell

### Open Heroku Shell
```bash
heroku run python manage.py shell --app consignment-site-2ac0cae70da0
```

### Create Package
```python
from packages.models import Package
from tracking.models import TrackingHistory
from django.contrib.auth import get_user_model

User = get_user_model()
admin = User.objects.filter(is_superuser=True).first()

# Create package
package = Package.objects.create(
    sender_name="John Doe",
    sender_address="Oslo Central Station",
    sender_city="Oslo",
    sender_country="Norway",
    recipient_name="Jane Smith",
    recipient_address="Mall Road",
    recipient_city="Lahore",
    recipient_country="Pakistan",
    weight=2.5,
    length=30,
    width=20,
    height=15,
    status="in_transit",
    current_location="Zahedan, Iran",
    current_latitude=29.4963,
    current_longitude=60.8629
)

# Add tracking history
TrackingHistory.objects.create(
    package=package,
    status="picked_up",
    location="Oslo, Norway",
    latitude=59.9139,
    longitude=10.7522,
    notes="Package picked up from sender"
)

TrackingHistory.objects.create(
    package=package,
    status="in_transit",
    location="Zahedan, Iran",
    latitude=29.4963,
    longitude=60.8629,
    notes="Package in transit through Iran"
)

print(f"✅ Package created: {package.tracking_number}")
print(f"🔗 Track at: https://consignment-site-2ac0cae70da0.herokuapp.com/track/?q={package.tracking_number}")
exit()
```

---

## Sample Coordinates for Testing

### European Cities
```
London, UK: (51.5074, -0.1278)
Paris, France: (48.8566, 2.3522)
Berlin, Germany: (52.5200, 13.4050)
Rome, Italy: (41.9028, 12.4964)
Madrid, Spain: (40.4168, -3.7038)
```

### Middle East
```
Istanbul, Turkey: (41.0082, 28.9784)
Dubai, UAE: (25.2048, 55.2708)
Tehran, Iran: (35.6892, 51.3890)
Baghdad, Iraq: (33.3152, 44.3661)
```

### South Asia
```
Lahore, Pakistan: (31.5497, 74.3436)
Islamabad, Pakistan: (33.6844, 73.0479)
Karachi, Pakistan: (24.8607, 67.0011)
Mumbai, India: (19.0760, 72.8777)
Delhi, India: (28.7041, 77.1025)
```

---

## 🎯 Testing Checklist

After seeding data, test these features:

### Homepage
- [ ] Search for tracking number
- [ ] View statistics (if displayed)

### Tracking Page
- [ ] Enter tracking number
- [ ] View package details
- [ ] See map with route
- [ ] Switch map layers (Clean, Satellite, Dark)
- [ ] Click truck marker for details
- [ ] Toggle access roads (📍 button)
- [ ] Check route details panel
- [ ] Verify ETA calculation

### Admin Panel
- [ ] Login successfully
- [ ] View all packages
- [ ] Edit package location
- [ ] Add tracking history
- [ ] Create new package
- [ ] Assign to driver

---

## ⚠️ Important Notes

### Database Persistence
- Heroku free tier may reset database periodically
- For permanent data, consider upgrading to paid PostgreSQL plan
- Or re-seed after each reset

### Performance
- First load may be slow (Heroku cold start)
- Subsequent requests are fast
- Consider upgrading dyno for always-on

---

**Status**: Ready to seed once admin is created!

**Recommended Order**:
1. Create admin account
2. Seed data via admin panel (easiest)
3. Test tracking features
4. Share with stakeholders

**Live Site**: https://consignment-site-2ac0cae70da0.herokuapp.com/
