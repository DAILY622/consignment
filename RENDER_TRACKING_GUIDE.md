# 🚀 Render Production Tracking Guide

## How to Check Active Tracking on Render

### Option 1: Python Script (Check Production Database)

Run this command to check your live Render production database:

```bash
python check_render_production.py
```

This script will:
- ✅ Connect to your Neon PostgreSQL database (Render production)
- ✅ Show all active packages with current locations
- ✅ Display tracking history and coordinates
- ✅ Show database statistics

---

### Option 2: Web Browser (User-Friendly)

Access your live Render deployment:

**Main Website:**
```
https://dailyfx-delivery.onrender.com
```

**Admin Panel:**
```
https://dailyfx-delivery.onrender.com/admin
```
- View/manage all packages
- See tracking history
- Update locations
- Monitor deliveries

**Track Specific Package:**
```
https://dailyfx-delivery.onrender.com/track/<TRACKING-NUMBER>
```
Example: `https://dailyfx-delivery.onrender.com/track/DFX-2XWJFI8R`

---

### Option 3: Render Shell (Direct Access)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Open your `dailyfx-delivery` service
3. Click **Shell** tab
4. Run:

```bash
# Check packages
python manage.py shell -c "from packages.models import Package; packages = Package.objects.all(); print(f'Total packages: {packages.count()}'); [print(f'{p.tracking_number}: {p.status} - {p.receiver_city}') for p in packages]"

# Check tracking
python manage.py shell -c "from tracking.models import TrackingHistory; history = TrackingHistory.objects.select_related('package').order_by('-timestamp')[:10]; [print(f'{h.package.tracking_number} @ {h.location} - {h.timestamp}') for h in history]"
```

---

### Option 4: API Endpoint (if you have one)

If you've created an API endpoint:

```bash
curl https://dailyfx-delivery.onrender.com/api/packages/
```

---

## 🗄️ Your Production Database

**Database Provider:** Neon PostgreSQL (Serverless)  
**Connection:** Configured in `render.yaml`

**Benefits:**
- ✅ Auto-scaling
- ✅ Built-in connection pooling
- ✅ No 90-day expiration
- ✅ Database branching support

---

## 📝 Current Configuration

From `render.yaml`:

```yaml
DATABASE_URL: postgresql://neondb_owner:npg_Hm6oMiXSaTc1@ep-soft-queen-ap4bqkwz-pooler.c-7.us-east-1.aws.neon.tech/neondb
Service Name: dailyfx-delivery
Region: oregon
Auto-deploy: true (on git push)
```

---

## 🔍 Quick Checks

### Is my app deployed?
Visit: `https://dailyfx-delivery.onrender.com`

### Check deployment logs:
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click your `dailyfx-delivery` service
3. View **Logs** tab

### Check database:
```bash
python check_render_production.py
```

---

## 🚨 Troubleshooting

### App not deployed yet?

1. **Push to GitHub** (already done ✅)
2. **Connect to Render:**
   - Go to https://dashboard.render.com
   - Click **New** → **Blueprint**
   - Select your repository: `KINGSACCOUNT1/consignment-site`
   - Render will auto-detect `render.yaml`
   - Click **Apply**

### Database empty?

If production database is empty, you need to:

1. **Run migrations** (Render should do this automatically via `build.sh`)
2. **Create admin user:**
   ```bash
   # In Render Shell
   python manage.py createsuperuser
   ```
3. **Add packages via admin panel**

### First request slow?

Free tier apps spin down after 15 minutes of inactivity.  
First request after spin-down takes ~30 seconds to wake up.

---

## 🎯 Quick Start Commands

**Local database (development):**
```bash
python check_db.py
```

**Production database (Render):**
```bash
python check_render_production.py
```

**Run migrations on Render:**
```bash
# In Render Shell
python manage.py migrate
```

**Create superuser on Render:**
```bash
# In Render Shell
python manage.py createsuperuser
```

---

## 📊 What You Should See

When you run `python check_render_production.py`:

```
======================================================================
🚀 RENDER PRODUCTION - ACTIVE PACKAGE TRACKING
======================================================================

📡 Connecting to Neon PostgreSQL (Render Production)...
✅ Connected successfully!

📦 ACTIVE PACKAGES: 2

======================================================================
📦 DFX-2XWJFI8R
   Status: IN_TRANSIT
   Route: Oslo, Norway → Lahore, Pakistan
   Created: 2026-04-06 22:18:45
   📍 Current Location: Quetta, Pakistan
   📌 Coordinates: (30.1798, 66.975)
   🕐 Last Update: 2026-05-18 10:20:21

======================================================================
📊 DATABASE STATISTICS
======================================================================
👥 Users: 2
📦 Packages: 2
🗺️  Route Waypoints: 7
```

---

## ✅ Next Steps

1. Run `python check_render_production.py` to verify production data
2. Visit your live site: `https://dailyfx-delivery.onrender.com`
3. Access admin: `https://dailyfx-delivery.onrender.com/admin`
4. Track packages via tracking numbers

**Note:** If the database is empty, the local data hasn't been migrated to production yet. You'll need to either:
- Import data to production
- Create new packages via the admin panel
- Use Django fixtures to load data
