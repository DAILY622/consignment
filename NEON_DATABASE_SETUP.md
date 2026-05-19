# 🐘 Configure Neon Database for Heroku

## Your Neon Database Connection

**Database URL:**
```
postgresql://neondb_owner:npg_Hm6oMiXSaTc1@ep-soft-queen-ap4bqkwz-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

**Provider**: Neon (Serverless PostgreSQL)  
**Region**: US East 1 (AWS)  
**Features**: Connection pooler enabled, SSL required

---

## 🚀 Set Up Neon Database on Heroku

### Method 1: Via Heroku Dashboard (Easiest) ✅

1. **Go to Heroku App Settings**
   - Visit: https://dashboard.heroku.com/apps/consignment-site-2ac0cae70da0/settings

2. **Reveal Config Vars**
   - Click **"Reveal Config Vars"** button

3. **Add DATABASE_URL**
   - **Key**: `DATABASE_URL`
   - **Value**: 
     ```
     postgresql://neondb_owner:npg_Hm6oMiXSaTc1@ep-soft-queen-ap4bqkwz-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
     ```
   - Click **"Add"**

4. **Verify Other Required Config Vars**
   Make sure these exist (add if missing):
   
   - **SECRET_KEY**: (generate one if not set)
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(50))"
     ```
   
   - **DEBUG**: `False`
   
   - **ALLOWED_HOSTS**: `consignment-site-2ac0cae70da0.herokuapp.com`

5. **Restart Dynos**
   - Click **"More"** → **"Restart all dynos"**
   - Or it restarts automatically after config change

---

### Method 2: Via Heroku CLI

```bash
# Set DATABASE_URL
heroku config:set DATABASE_URL="postgresql://neondb_owner:npg_Hm6oMiXSaTc1@ep-soft-queen-ap4bqkwz-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" --app consignment-site-2ac0cae70da0

# Verify it's set
heroku config --app consignment-site-2ac0cae70da0

# Restart app
heroku restart --app consignment-site-2ac0cae70da0
```

---

## 📊 Run Database Migrations

After setting the database URL, run migrations to create tables:

### Option 1: Via Heroku CLI
```bash
heroku run python manage.py migrate --app consignment-site-2ac0cae70da0
```

### Option 2: Via Heroku Dashboard Console
1. Go to app dashboard
2. Click **"More"** → **"Run console"**
3. Enter: `python manage.py migrate`
4. Click **"Run"**

**Expected Output:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying accounts.0001_initial... OK
  Applying packages.0001_initial... OK
  Applying tracking.0001_initial... OK
  ...
```

---

## ✅ Verify Database Connection

### Test 1: Check if tables were created
```bash
heroku run python manage.py showmigrations --app consignment-site-2ac0cae70da0
```

Should show `[X]` for all applied migrations.

### Test 2: Access Django shell
```bash
heroku run python manage.py shell --app consignment-site-2ac0cae70da0
```

```python
# Test database connection
from django.db import connection
print("✅ Connected to:", connection.settings_dict['NAME'])

# Check if tables exist
from packages.models import Package
print("✅ Package model works!")

# Count packages
print(f"Packages in database: {Package.objects.count()}")

exit()
```

---

## 🆚 Neon vs Heroku PostgreSQL

### Why Neon?

| Feature | Neon | Heroku PostgreSQL |
|---------|------|-------------------|
| **Pricing** | Free tier generous | Free tier limited |
| **Serverless** | ✅ Auto-scales | ❌ Fixed size |
| **Connection Pooling** | ✅ Built-in | Extra add-on |
| **Branching** | ✅ Database branching | ❌ Not available |
| **Performance** | ⚡ Fast (AWS) | Standard |
| **Storage** | More on free tier | 1GB limit |

### Benefits:
- ✅ Better free tier limits
- ✅ Automatic connection pooling
- ✅ Serverless (no idle charges)
- ✅ Instant branching for testing
- ✅ AWS infrastructure

---

## 🔐 Security Best Practices

### Connection String Breakdown:
```
postgresql://[user]:[password]@[host]:[port]/[database]?[options]
```

Your connection:
- **User**: `neondb_owner`
- **Password**: `npg_Hm6oMiXSaTc1` ⚠️ Keep secret!
- **Host**: `ep-soft-queen-ap4bqkwz-pooler.c-7.us-east-1.aws.neon.tech`
- **Database**: `neondb`
- **Options**: SSL required, channel binding

### Security Notes:
1. ⚠️ **Never commit** this URL to Git
2. ✅ Store only in Heroku config vars
3. ✅ SSL is enforced (secure connection)
4. ✅ Connection pooler enabled (better performance)
5. 🔒 Rotate password if exposed

---

## 🎯 Deployment Checklist with Neon

- [ ] **Set DATABASE_URL** in Heroku config vars
- [ ] **Run migrations** to create tables
- [ ] **Verify connection** using Django shell
- [ ] **Create superuser** for admin access
- [ ] **Seed demo data** for testing
- [ ] **Test tracking** on production site
- [ ] **Check Neon dashboard** for usage stats

---

## 📱 Neon Database Dashboard

### Access Your Database:
1. **Neon Console**: https://console.neon.tech
2. Find your project: `ep-soft-queen-ap4bqkwz`
3. View:
   - Connection details
   - Query editor (SQL)
   - Metrics & usage
   - Backups & branches

### Useful Neon Features:
- **SQL Editor**: Run queries directly
- **Monitoring**: Track connections, queries
- **Branches**: Create dev/staging databases
- **Point-in-time Restore**: Rollback to any moment

---

## 🐛 Troubleshooting

### Error: "SSL connection required"
✅ Your URL already includes `sslmode=require` - should work fine

### Error: "Too many connections"
✅ You're using the pooler endpoint - handles this automatically

### Error: "Could not connect to server"
- Check Neon dashboard (server might be sleeping on free tier)
- First connection wakes it up (may take a few seconds)

### Error: "Authentication failed"
- Verify DATABASE_URL is correct
- Check for typos in password
- Ensure no extra spaces

### Database is empty after deployment
Run migrations:
```bash
heroku run python manage.py migrate --app consignment-site-2ac0cae70da0
```

---

## 🔄 Migration Commands Reference

### Create migrations (after model changes)
```bash
heroku run python manage.py makemigrations --app consignment-site-2ac0cae70da0
```

### Apply migrations
```bash
heroku run python manage.py migrate --app consignment-site-2ac0cae70da0
```

### Check migration status
```bash
heroku run python manage.py showmigrations --app consignment-site-2ac0cae70da0
```

### Rollback migrations (if needed)
```bash
heroku run python manage.py migrate packages 0001 --app consignment-site-2ac0cae70da0
```

---

## 📊 After Setup - Create Admin & Seed Data

### 1. Create Superuser
```bash
heroku run python manage.py createsuperuser --app consignment-site-2ac0cae70da0
```

### 2. Seed Demo Packages
```bash
heroku run python manage.py seed_data --app consignment-site-2ac0cae70da0
```

### 3. Access Admin Panel
Visit: https://consignment-site-2ac0cae70da0.herokuapp.com/admin/

---

## ✅ Complete Setup Flow

**Step-by-step with Neon:**

1. ✅ **Set DATABASE_URL** (via Heroku dashboard)
2. ✅ **Run migrations** (`heroku run python manage.py migrate`)
3. ✅ **Create superuser** (`heroku run python manage.py createsuperuser`)
4. ✅ **Seed data** (via admin panel or seed command)
5. ✅ **Test site** (visit tracking page)
6. ✅ **Verify map features** (layers, markers, etc.)

**Total Time**: 15-20 minutes

---

## 🎉 Benefits of Your Setup

**Heroku + Neon = Best of Both Worlds**

- ✅ **Heroku**: Easy deployment, auto-build, SSL
- ✅ **Neon**: Better database, serverless, free tier
- ✅ **GitHub**: Version control, auto-deploy
- ✅ **Result**: Professional production setup!

---

## 📞 Support

### Neon Support:
- Docs: https://neon.tech/docs
- Discord: https://discord.gg/neon
- Status: https://neonstatus.com

### Heroku Support:
- Docs: https://devcenter.heroku.com
- Help: https://help.heroku.com

---

**Status**: Ready to configure! Set DATABASE_URL in Heroku and run migrations.

**Next Steps**:
1. Add DATABASE_URL to Heroku config vars
2. Run migrations
3. Create admin account
4. Start using your enhanced tracking system!

---

📅 **Created**: May 18, 2026  
🗄️ **Database**: Neon PostgreSQL (Serverless)  
🚀 **Status**: Ready to deploy!
