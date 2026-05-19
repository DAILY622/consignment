# Railway Deployment Guide for Consignment Site

## 🚂 Railway + Neon DB - 100% FREE Deployment

### Prerequisites
- GitHub account (KINGSACCOUNT1)
- Railway account (free)
- Neon DB account (free)

## Step 1: Create Neon Database

1. Go to https://neon.tech
2. Sign in with GitHub (KINGSACCOUNT1)
3. Create a new project: "consignment-db"
4. Copy the connection string (starts with `postgresql://`)
   - Format: `postgresql://user:password@host/database?sslmode=require`

## Step 2: Deploy to Railway

### Option A: Web Dashboard (Easiest)

1. Go to https://railway.app
2. Sign in with GitHub (KINGSACCOUNT1)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select: **KINGSACCOUNT1/consignment-site**
5. Railway will auto-detect Django and deploy

### Option B: CLI (Faster)

```bash
# Login to Railway
railway login

# Link to GitHub repo
railway init

# Add environment variables
railway variables set DATABASE_URL="your-neon-connection-string"
railway variables set SECRET_KEY="your-secret-key"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="*.railway.app"

# Deploy
railway up
```

## Step 3: Configure Environment Variables

Add these in Railway Dashboard → Variables:

```
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
SECRET_KEY=django-insecure-x7k9m2p4q8r1s5t3u6v0w9y2z4a7b1c3d5e8f0g2h4j6
DEBUG=False
ALLOWED_HOSTS=*.railway.app
DJANGO_SETTINGS_MODULE=consignment.settings
PYTHONUNBUFFERED=1
PORT=8000
```

## Step 4: Generate New SECRET_KEY (Recommended)

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and update SECRET_KEY in Railway.

## Step 5: Run Migrations

Railway will automatically run:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## Step 6: Create Superuser (Admin Access)

In Railway Dashboard → Project → Deployments → Click latest → "View Logs"

Or use Railway CLI:
```bash
railway run python manage.py createsuperuser
```

## Step 7: Test Your Deployment

Your site will be live at:
```
https://consignment-site-production.up.railway.app
```

Test URLs:
- Home: https://your-app.railway.app/
- Admin: https://your-app.railway.app/admin/
- Track: https://your-app.railway.app/track/DFX-2XWJFI8R/

## 🎯 Railway Free Tier Limits

- $5 credit per month (500 hours of compute)
- Enough for hobby projects with moderate traffic
- No cold starts (always running)
- Auto SSL certificates
- Custom domains available

## 🔧 Troubleshooting

### Static files not loading
```bash
railway run python manage.py collectstatic --noinput
```

### Database connection issues
- Check DATABASE_URL format includes `?sslmode=require`
- Verify Neon DB is active (doesn't auto-suspend)

### App won't start
- Check logs: Railway Dashboard → Deployments → View Logs
- Verify all environment variables are set
- Ensure requirements.txt includes gunicorn

## 📊 Monitoring

- Railway Dashboard shows:
  - CPU/Memory usage
  - Request logs
  - Deployment history
  - Environment variables

## 🚀 Continuous Deployment

Railway auto-deploys when you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

Railway detects the push and deploys automatically!

## 💰 Cost

- **Free Tier**: $5/month credit (FREE)
- **Neon DB**: FREE tier (3GB storage)
- **Total Cost**: $0/month for small projects

## 🔗 Useful Links

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app
- Neon Console: https://console.neon.tech
- GitHub Repo: https://github.com/KINGSACCOUNT1/consignment-site

## ✅ Deployment Checklist

- [ ] Neon DB created and connection string copied
- [ ] Railway project created from GitHub repo
- [ ] Environment variables configured
- [ ] SECRET_KEY generated and updated
- [ ] Database migrations ran successfully
- [ ] Static files collected
- [ ] Superuser created
- [ ] Site accessible at Railway URL
- [ ] Admin panel working
- [ ] Package tracking working
- [ ] Map features displaying correctly

---

**Deployed with ❤️ using Railway + Neon DB**
