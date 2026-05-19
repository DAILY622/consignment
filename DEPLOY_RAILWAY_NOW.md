# 🚂 RAILWAY DEPLOYMENT - Quick Start Guide

## ✅ Your Platform: Railway + Neon Database

**Railway Dashboard**: https://railway.app/dashboard  
**Your Neon DB**: Already configured  
**Your GitHub**: KINGSACCOUNT1/consignment-site

---

## 🎯 Complete Deployment in 10 Minutes

### STEP 1: Login to Railway (2 minutes)

**Go to**: https://railway.app

1. [ ] Click **"Login"**
2. [ ] Select **"Login with GitHub"**
3. [ ] Authorize Railway to access GitHub
4. [ ] You'll be redirected to Railway Dashboard

---

### STEP 2: Create New Project (3 minutes)

1. [ ] Click **"New Project"** button
2. [ ] Select **"Deploy from GitHub repo"**
3. [ ] Choose repository: **KINGSACCOUNT1/consignment-site**
4. [ ] Click **"Deploy Now"**

Railway will automatically:
- ✅ Detect it's a Django project
- ✅ Use `nixpacks.toml` configuration
- ✅ Install dependencies from `requirements.txt`
- ✅ Start building your app

---

### STEP 3: Configure Environment Variables (3 minutes)

Click on your deployed project, then go to **"Variables"** tab.

Add these variables:

#### 1. DATABASE_URL (**CRITICAL**)
```
postgresql://neondb_owner:npg_Hm6oMiXSaTc1@ep-soft-queen-ap4bqkwz-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

#### 2. SECRET_KEY
```
django-insecure-x7k9m2p4q8r1s5t3u6v0w9y2z4a7b1c3d5e8f0g2h4j6
```
*(Or generate a new one)*

#### 3. DEBUG
```
False
```

#### 4. ALLOWED_HOSTS
```
*.railway.app
```

#### 5. PYTHONUNBUFFERED
```
1
```

**Click "Add" after each variable.**

Railway will automatically redeploy when you save variables.

---

### STEP 4: Wait for Build (2-3 minutes)

Watch the deployment logs:
- **Building**: Installing Python packages
- **Collecting static**: Gathering CSS/JS files
- **Migrating**: Creating database tables
- **Starting**: Launching with Gunicorn

**✅ When you see**: "Deployment successful" or "Live" status

---

### STEP 5: Get Your Live URL

1. [ ] Go to **"Settings"** tab
2. [ ] Find **"Domains"** section
3. [ ] Copy the Railway URL (e.g., `consignment-site-production.up.railway.app`)
4. [ ] Click on it to open your live site!

---

## 🎯 Post-Deployment Tasks

### Create Admin Account

**Option A: Railway Dashboard**
1. Go to your project
2. Click **"Deployments"** tab
3. Click latest deployment
4. Click **"View Logs"**
5. In the top-right, click **"..."** → **"Shell"**
6. Run: `python manage.py createsuperuser`
7. Follow prompts

**Option B: Railway CLI** (if you have it installed)
```bash
railway login
railway link
railway run python manage.py createsuperuser
```

### Seed Demo Data

**Via Shell:**
```bash
python manage.py seed_data
```

This creates 10 demo packages (ECG-DEMO0000 through ECG-DEMO0009).

---

## 📋 Your Live URLs

After deployment, you'll have:

| Page | URL |
|------|-----|
| **Homepage** | `https://your-app.railway.app/` |
| **Tracking** | `https://your-app.railway.app/track/` |
| **Admin** | `https://your-app.railway.app/admin/` |
| **API** | `https://your-app.railway.app/api/` |

*(Replace `your-app` with your actual Railway domain)*

---

## ✅ Verification Checklist

Test these after deployment:

### Basic Functionality:
- [ ] Site loads without errors
- [ ] Styling displays correctly (Tailwind CSS)
- [ ] Static files load (images, icons)
- [ ] Admin panel accessible
- [ ] Can login to admin

### Enhanced Map Features:
- [ ] Tracking page loads
- [ ] Map displays with package location
- [ ] Multiple layer options visible (top-right)
- [ ] Can switch between Clean, Satellite, Dark mode
- [ ] Truck marker shows on map
- [ ] Click truck marker → See enhanced popup
- [ ] Route details panel displays below map
- [ ] All 7 control buttons work

### Tawk.to Chat Widget:
- [ ] Chat bubble visible (bottom-right corner)
- [ ] Clicking opens chat window
- [ ] Can send test message
- [ ] Widget appears on all pages

---

## 🔧 Railway Configuration Files

Your project includes these Railway-specific files:

### 1. `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. `nixpacks.toml`
```toml
[phases.setup]
nixPkgs = ["python312", "postgresql"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = [
    "python manage.py collectstatic --noinput",
    "python manage.py migrate --noinput"
]

[start]
cmd = "gunicorn consignment.wsgi:application --bind 0.0.0.0:$PORT"
```

These tell Railway exactly how to build and run your Django app.

---

## 🚀 Continuous Deployment (Auto-Deploy)

**Railway auto-deploys when you push to GitHub!**

Every time you run:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Railway:
1. Detects the push (within 30 seconds)
2. Starts a new build
3. Runs tests (if configured)
4. Deploys automatically
5. Makes it live

**No manual deployment needed!** 🎉

---

## 💰 Railway Free Tier

### What You Get (FREE):
- ✅ $5 credit per month
- ✅ ~500 hours of compute time
- ✅ **No cold starts** (always running!)
- ✅ Auto SSL certificates (HTTPS)
- ✅ Custom domains
- ✅ Automatic backups
- ✅ GitHub integration

### How Long Does $5 Last?
- **Light traffic** (few visitors): Full month
- **Moderate traffic**: 3-4 weeks
- **Heavy traffic**: 2-3 weeks

**Way better than Heroku's free tier!**

---

## 📊 Monitoring & Logs

### View Logs:
1. Railway Dashboard → Your Project
2. Click **"Deployments"** tab
3. Click on latest deployment
4. Click **"View Logs"**

See real-time:
- Application logs
- Error messages
- Request logs
- Database queries

### Metrics:
1. Go to **"Metrics"** tab
2. View:
   - CPU usage
   - Memory usage
   - Network traffic
   - Response times

---

## 🆘 Troubleshooting

### Build Failed
**Check:**
- Requirements.txt includes all dependencies
- Python version in nixpacks.toml (3.12)
- Build logs for specific error

### Site Loads But No Styling
**Fix:**
```bash
railway run python manage.py collectstatic --noinput
```

### Database Connection Error
**Verify:**
- DATABASE_URL is set correctly
- No extra spaces in connection string
- Neon DB is active (check Neon dashboard)

### Map Not Showing
**Check:**
- Browser console for JavaScript errors
- Package has latitude/longitude values
- Leaflet.js files loaded

### Chat Widget Not Appearing
**Verify:**
- Tawk.to script in base.html (we added it!)
- No JavaScript errors blocking it
- Widget ID is correct

---

## 🔄 Update Deployment

### Change Environment Variables:
1. Railway Dashboard → Your Project
2. **Variables** tab
3. Edit or add variables
4. Click **"Save"**
5. Railway redeploys automatically

### Manual Redeploy:
1. Go to **"Deployments"** tab
2. Click **"..."** on latest deployment
3. Click **"Redeploy"**

### Rollback to Previous Version:
1. Go to **"Deployments"** tab
2. Find working deployment
3. Click **"..."** → **"Redeploy"**

---

## 🎯 Add Custom Domain (Optional)

### Using Your Own Domain:

1. Railway Dashboard → Your Project
2. **Settings** tab → **Domains** section
3. Click **"Custom Domain"**
4. Enter your domain (e.g., `track.dailyfxdelivery.com`)
5. Add DNS records (Railway provides them):
   - Type: CNAME
   - Name: track
   - Value: your-app.railway.app

**Railway automatically provisions SSL certificate!**

---

## 📱 Railway CLI (Optional)

### Install:
```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex

# Or via npm
npm install -g @railway/cli
```

### Login:
```bash
railway login
```

### Link to Project:
```bash
cd "C:\Users\Wisdom Godswill\Desktop\consign"
railway link
```

### Useful Commands:
```bash
# Deploy
railway up

# View logs
railway logs

# Open in browser
railway open

# Run Django commands
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py shell

# Check status
railway status

# View variables
railway variables
```

---

## ✅ Deployment Status

| Task | Status |
|------|--------|
| **Code in GitHub** | ✅ Committed (latest: c179ae5) |
| **Railway config** | ✅ railway.json & nixpacks.toml |
| **Neon database** | ✅ Connection string ready |
| **Environment vars** | ⏳ Need to set in Railway |
| **Project created** | ⏳ Need to create on Railway |
| **Live deployment** | ⏳ Waiting for Steps 1-4 |

---

## 🎉 What's Included in Your Deployment

### Core Features:
- ✅ Django 6.0 application
- ✅ Package tracking system
- ✅ User authentication
- ✅ Driver portal
- ✅ Admin panel (Django Admin)

### Enhanced Features (NEW!):
- ✅ **6 Map Upgrades**: Multiple layers, enhanced markers, route details
- ✅ **Tawk.to Chat**: Live customer support
- ✅ **Neon Database**: Serverless PostgreSQL
- ✅ **Auto-deploy**: Push to Git = Auto deploy
- ✅ **SSL/HTTPS**: Automatic secure connection

### Documentation:
- ✅ Complete deployment guides
- ✅ Map upgrade documentation
- ✅ Database setup instructions
- ✅ Chat widget integration guide

---

## 🎯 Next Steps (IN ORDER)

1. **Login to Railway** → https://railway.app
2. **Create new project** from GitHub repo
3. **Add environment variables** (especially DATABASE_URL)
4. **Wait for build** to complete
5. **Get your live URL** from Settings → Domains
6. **Create admin account** via Railway shell
7. **Seed demo data** for testing
8. **Test all features** (map, tracking, chat)
9. **Share URL** with stakeholders
10. **Celebrate!** 🎉

---

## 📞 Support & Resources

### Railway:
- **Dashboard**: https://railway.app/dashboard
- **Docs**: https://docs.railway.app
- **Discord**: https://discord.gg/railway
- **Status**: https://status.railway.app

### Neon:
- **Console**: https://console.neon.tech
- **Docs**: https://neon.tech/docs
- **Discord**: https://discord.gg/neon

### Your Repository:
- **GitHub**: https://github.com/KINGSACCOUNT1/consignment-site
- **Latest Commit**: c179ae5

---

## 🔐 Security Notes

### Environment Variables:
- ⚠️ **Never commit** DATABASE_URL or SECRET_KEY to Git
- ✅ Store only in Railway variables (encrypted)
- 🔒 Rotate secrets if accidentally exposed

### Production Settings:
- ✅ DEBUG=False (already set)
- ✅ SSL enforced (automatic on Railway)
- ✅ Database connection encrypted (Neon SSL)
- ✅ ALLOWED_HOSTS configured

---

**DEPLOYMENT TIME**: 10-15 minutes total  
**COST**: $0/month (free tiers)  
**READY**: YES! All code is committed and ready to deploy.

**👉 START HERE**: https://railway.app (Login with GitHub)

---

📅 **Created**: May 18, 2026  
🚂 **Platform**: Railway  
🗄️ **Database**: Neon PostgreSQL  
📦 **Repository**: KINGSACCOUNT1/consignment-site  
✅ **Status**: READY TO DEPLOY!
