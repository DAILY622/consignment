# 🚀 Render Deployment Guide - DailyFX Delivery Logistics

Complete guide for deploying your Django consignment management system to Render.com

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Deployment Steps](#deployment-steps)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance & Updates](#maintenance--updates)

---

## Prerequisites

Before deploying to Render, ensure you have:

- ✅ A GitHub account with your project repository
- ✅ A Render account (sign up at https://render.com)
- ✅ Your project pushed to a GitHub repository (can be private)
- ✅ Git installed locally

## Initial Setup

### 1. Prepare Your Repository

Make sure all files are committed and pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Sign Up for Render

1. Go to https://render.com
2. Click "Get Started"
3. Sign up using your GitHub account
4. Authorize Render to access your repositories

---

## Deployment Steps

### Method 1: Using Blueprint (Recommended) 🎯

This method uses the `render.yaml` file for infrastructure-as-code deployment.

#### Step 1: Create New Blueprint

1. Log in to Render Dashboard
2. Click "New +" button → Select **"Blueprint"**
3. Connect your GitHub repository
4. Select the repository containing your Django project
5. Render will automatically detect the `render.yaml` file

#### Step 2: Configure Blueprint

1. **Service Name**: `dailyfx-delivery` (or customize)
2. **Branch**: `main` (or your default branch)
3. The blueprint will create:
   - PostgreSQL database: `consignment-db`
   - Web service: `dailyfx-delivery`

#### Step 3: Review & Deploy

1. Review the services that will be created
2. Click **"Apply"** to start deployment
3. Render will:
   - Provision a PostgreSQL database
   - Build your Django application
   - Run migrations
   - Collect static files
   - Start the Gunicorn server

#### Step 4: Monitor Build

- Watch the build logs in real-time
- Build typically takes 3-5 minutes
- Look for "Build successful" message

---

### Method 2: Manual Setup (Alternative)

If you prefer manual configuration:

#### Step 1: Create PostgreSQL Database

1. Dashboard → **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `consignment-db`
   - **Database**: `consignment`
   - **User**: `consignment`
   - **Region**: Same as web service (e.g., Oregon)
   - **Plan**: Starter (Free)
3. Click **"Create Database"**
4. Wait for provisioning (~2 minutes)
5. **Copy the Internal Database URL** (starts with `postgresql://`)

#### Step 2: Create Web Service

1. Dashboard → **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:

**Basic Settings:**
- **Name**: `dailyfx-delivery`
- **Region**: Oregon (or closest to your users)
- **Branch**: `main`
- **Root Directory**: Leave empty (root of repo)
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  chmod +x build.sh && ./build.sh
  ```
- **Start Command**:
  ```bash
  gunicorn consignment.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile -
  ```

#### Step 3: Configure Environment Variables

Add these in the **"Environment"** tab:

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | From PostgreSQL service | Paste Internal Database URL |
| `SECRET_KEY` | Generate new key | Use https://djecrety.ir/ |
| `DEBUG` | `False` | Never `True` in production |
| `PYTHON_VERSION` | `3.12.0` | Match your local version |
| `DJANGO_SETTINGS_MODULE` | `consignment.settings` | |
| `ALLOWED_HOSTS` | `.onrender.com` | Or your custom domain |
| `DJANGO_LOG_LEVEL` | `INFO` | For better logging |

**Optional Email Configuration:**
| Key | Value |
|-----|-------|
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `True` |
| `EMAIL_HOST_USER` | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Your app password |
| `DEFAULT_FROM_EMAIL` | `noreply@yoursite.com` |

#### Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will start building automatically
3. Monitor logs for any errors

---

## Post-Deployment Configuration

### 1. Create Superuser

Once deployment is complete, create an admin account:

1. Go to your service in Render Dashboard
2. Click **"Shell"** tab
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow prompts to create admin credentials

### 2. Access Your Application

- **Public URL**: `https://dailyfx-delivery.onrender.com`
- **Admin Panel**: `https://dailyfx-delivery.onrender.com/admin`

### 3. Verify Deployment

Check these URLs:
- ✅ Homepage loads correctly
- ✅ Admin panel accessible
- ✅ Static files (CSS/JS) loading
- ✅ Can log in to admin
- ✅ Database queries working

### 4. Set Up Custom Domain (Optional)

1. Go to service **"Settings"** → **"Custom Domain"**
2. Add your domain (e.g., `www.dailyfxdelivery.com`)
3. Update DNS records as instructed:
   - **CNAME**: Point to `dailyfx-delivery.onrender.com`
4. Update `ALLOWED_HOSTS` environment variable:
   ```
   .onrender.com,dailyfxdelivery.com,www.dailyfxdelivery.com
   ```
5. Update `CSRF_TRUSTED_ORIGINS` in settings.py if needed

---

## Environment Variables

### Required Variables

```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-super-secret-key-here
DEBUG=False
PYTHON_VERSION=3.12.0
```

### Optional Variables

```bash
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@dailyfxdelivery.com
CONTACT_EMAIL=support@dailyfxdelivery.com

# Custom Domain
ALLOWED_HOSTS=.onrender.com,yourdomain.com

# Logging
DJANGO_LOG_LEVEL=INFO

# Performance
WEB_CONCURRENCY=2  # Number of Gunicorn workers
```

### How to Add/Update Environment Variables

1. Go to your service in Render Dashboard
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Enter key and value
5. Click **"Save Changes"**
6. Service will automatically redeploy

---

## Troubleshooting

### Common Issues

#### ❌ Build Failed: `ModuleNotFoundError`

**Solution**: Check `requirements.txt` has all dependencies
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

#### ❌ Static Files Not Loading

**Solution**: Ensure WhiteNoise is configured in settings.py
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be after SecurityMiddleware
    ...
]
```

Run:
```bash
python manage.py collectstatic --noinput
```

#### ❌ Database Connection Error

**Solution**: 
1. Verify `DATABASE_URL` is set correctly
2. Check database is running (Render Dashboard → Database service)
3. Ensure `dj-database-url` and `psycopg2-binary` are in requirements.txt

#### ❌ 502 Bad Gateway

**Solution**:
1. Check build logs for errors
2. Verify start command is correct
3. Ensure Gunicorn is installed
4. Check if port binding is correct (`--bind 0.0.0.0:$PORT`)

#### ❌ CSRF Verification Failed

**Solution**: Add your domain to `CSRF_TRUSTED_ORIGINS` in settings.py
```python
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://yourdomain.com',
]
```

#### ❌ Admin CSS Not Loading

**Solution**: Run collectstatic and check STATIC settings:
```python
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Viewing Logs

1. Render Dashboard → Your service
2. Click **"Logs"** tab
3. View real-time logs
4. Filter by log level (INFO, WARNING, ERROR)

### Debugging in Production

**Enable debug mode temporarily** (NOT recommended for long periods):
1. Set `DEBUG=True` in environment variables
2. Set `DJANGO_LOG_LEVEL=DEBUG`
3. Check logs for detailed errors
4. **Remember to set back to `False`** after debugging

---

## Maintenance & Updates

### Deploying Updates

Render auto-deploys when you push to GitHub:

```bash
# Make your changes
git add .
git commit -m "Your update message"
git push origin main
```

Render will:
1. Detect the push
2. Start a new build
3. Run build.sh (migrations, collectstatic)
4. Deploy new version
5. No downtime with rolling deployments

### Manual Deploy

If auto-deploy is disabled:
1. Render Dashboard → Your service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Database Migrations

Migrations run automatically during build (in `build.sh`):
```bash
python manage.py migrate
```

To run migrations manually:
1. Go to service **"Shell"**
2. Run: `python manage.py migrate`

### Backing Up Database

#### Method 1: Render Dashboard
1. Go to Database service
2. Click **"Backups"** tab (available on paid plans)

#### Method 2: Manual Backup
1. Go to service **"Shell"**
2. Run:
```bash
pg_dump $DATABASE_URL > backup.sql
```

#### Method 3: Download Backup Locally
```bash
# Get database connection string from Render
pg_dump "postgresql://user:pass@host:5432/db" > local_backup.sql
```

### Monitoring Performance

1. **Dashboard Metrics**: CPU, Memory, Request count
2. **Logs**: Monitor for errors and warnings
3. **Health Checks**: Render pings your `/` endpoint
4. **Alerts**: Set up email notifications for downtime

### Scaling

**Vertical Scaling** (upgrade plan):
- Starter → Standard → Pro
- More CPU, RAM, and concurrent connections

**Horizontal Scaling**:
- Paid plans allow multiple instances
- Load balancing handled automatically

---

## Cost Optimization

### Free Tier Limits
- **Web Service**: Spins down after 15 minutes of inactivity
- **Database**: 90-day expiration, 1GB storage
- **First request** may be slow (cold start)

### Paid Plans
- **Starter**: $7/month - Always on, no cold starts
- **Standard**: $25/month - More resources
- **Database**: $7/month - Persistent, no expiration

### Tips
1. Use free tier for testing/development
2. Upgrade to paid for production
3. Monitor usage in Render Dashboard
4. Set up billing alerts

---

## Security Best Practices

1. ✅ **Never commit secrets** to Git
2. ✅ Keep `DEBUG=False` in production
3. ✅ Use strong `SECRET_KEY`
4. ✅ Enable HTTPS (automatic on Render)
5. ✅ Set proper `ALLOWED_HOSTS`
6. ✅ Configure `CSRF_TRUSTED_ORIGINS`
7. ✅ Use environment variables for credentials
8. ✅ Regularly update dependencies
9. ✅ Monitor logs for suspicious activity
10. ✅ Keep Django updated

---

## Support & Resources

- **Render Documentation**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Django Deployment**: https://docs.djangoproject.com/en/5.0/howto/deployment/
- **Render Status**: https://status.render.com

---

## Quick Reference

### Essential Commands

```bash
# Seed data
python manage.py seed_data

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Check deployment
python manage.py check --deploy

# Shell access
python manage.py shell
```

### Useful URLs

- Dashboard: https://dashboard.render.com
- Your App: https://dailyfx-delivery.onrender.com
- Admin: https://dailyfx-delivery.onrender.com/admin
- Database: (Internal URL in environment variables)

---

## Checklist Before Going Live

- [ ] All environment variables configured
- [ ] Database connected and migrated
- [ ] Superuser created
- [ ] Static files collecting properly
- [ ] Email configured (if needed)
- [ ] Custom domain set up (if applicable)
- [ ] HTTPS working
- [ ] Admin panel accessible
- [ ] Test all major features
- [ ] Backups configured
- [ ] Monitoring enabled
- [ ] Documentation updated

---

**🎉 Congratulations!** Your Django application is now live on Render!

For questions or issues, check the [troubleshooting section](#troubleshooting) or contact Render support.
