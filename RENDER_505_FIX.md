# 505 Error Fix for Render Deployment

## 🔴 Problem: 505 Error on https://dailyfx-delivery-8ej1.onrender.com

## 📋 What the Logs Show:
```
✅ Server is running (Gunicorn started successfully)
✅ Health checks return 200 OK
⚠️ 301 redirect happening (HTTP → HTTPS)
🔴 Real requests get 505 error
```

## 🐛 Root Cause:
Django wildcard CSRF_TRUSTED_ORIGINS doesn't work in some cases. Need exact URL.

## ✅ Quick Fix

### Option 1: Update CSRF_TRUSTED_ORIGINS in Render

**Go to Render Dashboard:**
1. Open your service: `dailyfx-delivery`
2. Click **Environment**
3. Add new environment variable:

```
CSRF_TRUSTED_ORIGINS_EXTRA=https://dailyfx-delivery-8ej1.onrender.com
```

4. Click **Save Changes**
5. Service will auto-redeploy

### Option 2: Update settings.py (Recommended)

The wildcard `https://*.onrender.com` might not be working. Let me fix this:

```python
# In settings.py, change CSRF_TRUSTED_ORIGINS to:
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://dailyfx-delivery-8ej1.onrender.com',  # Exact URL
]

# Add support for extra origins from env
_extra_origins = os.environ.get('CSRF_TRUSTED_ORIGINS_EXTRA', '')
if _extra_origins:
    CSRF_TRUSTED_ORIGINS.extend([o.strip() for o in _extra_origins.split(',') if o.strip()])
```

## 🔍 Other Potential Issues:

### 1. Database Connection
Check if DATABASE_URL is set correctly in Render:
- Should start with `postgresql://`
- Should have correct Neon credentials

### 2. Static Files
Run collectstatic in build:
```bash
python manage.py collectstatic --no-input
```

### 3. SECRET_KEY
Ensure SECRET_KEY is generated in Render (should be automatic).

## 🚀 Immediate Fix Steps:

### Step 1: Check Render Environment Variables
Go to Render Dashboard → Environment and verify:
- ✅ `SECRET_KEY` exists (auto-generated)
- ✅ `DATABASE_URL` is correct
- ✅ `DEBUG=False`
- ✅ `ALLOWED_HOSTS=.onrender.com`

### Step 2: Add Exact URL to CSRF_TRUSTED_ORIGINS
Add environment variable in Render:
```
CSRF_TRUSTED_ORIGINS_EXTRA=https://dailyfx-delivery-8ej1.onrender.com
```

### Step 3: Check Database
The DATABASE_URL in render.yaml has `******` prefix which might be the issue. 

Check if it should be `postgres://` or `postgresql://`

### Step 4: View Logs
In Render Dashboard, click **Logs** to see actual error messages.

## 🔧 Code Fix (I'll apply this now):

Let me update settings.py to handle CSRF origins better and add better error logging.
