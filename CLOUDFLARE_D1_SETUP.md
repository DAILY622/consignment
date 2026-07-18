# Cloudflare D1 Database Setup Guide

## 🚀 Cloudflare D1 - Serverless SQLite Database

Cloudflare D1 is a serverless SQL database built on SQLite, perfect for our consignment tracking system!

---

## ✨ Why Cloudflare D1?

✅ **Free Tier:**
- 5 GB storage
- 5 million reads/day
- 100,000 writes/day
- Perfect for small-medium delivery businesses

✅ **Benefits:**
- Zero cold starts
- Global edge distribution
- Built-in replication
- Works with Workers (if deploying to Cloudflare)
- S3-compatible (pairs perfectly with R2!)

✅ **Cost:**
- **FREE** for most use cases
- Paid: $0.75/million reads, $4.50/million writes beyond free tier

---

## 📋 Setup Steps

### **Step 1: Install Wrangler CLI**

```bash
npm install -g wrangler
# or
npm install wrangler --save-dev
```

### **Step 2: Login to Cloudflare**

```bash
wrangler login
```

This opens browser for authentication.

### **Step 3: Create D1 Database**

```bash
# Create database
wrangler d1 create consignment-delivery-db

# Output will show:
# ✅ Successfully created DB 'consignment-delivery-db'
# 
# [[d1_databases]]
# binding = "DB"
# database_name = "consignment-delivery-db"
# database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

**IMPORTANT:** Copy the `database_id` - you'll need it!

### **Step 4: Get Database Connection Info**

```bash
wrangler d1 info consignment-delivery-db
```

This shows your database ID and connection details.

---

## 🔧 Django Configuration

### **Option 1: Using D1 HTTP API (Recommended for Render)**

Since D1 is designed for Cloudflare Workers, we'll use the HTTP API from Django.

**Install package:**
```bash
pip install httpx
```

**Update requirements.txt:**
```
django==6.0.5
pillow==12.2.0
gunicorn==26.0.0
whitenoise==6.12.0
dj-database-url==3.1.2
psycopg2-binary==2.9.12
django-jazzmin==3.0.4
python-dotenv==1.0.1
django-storages==1.14.4
boto3==1.35.93
httpx==0.27.2  # NEW - for D1 HTTP API
```

### **Option 2: Use SQLite Locally, D1 in Production**

For simplicity, use SQLite locally and Cloudflare D1 in production via Workers.

---

## 🌐 Deployment Options

### **Option A: Deploy to Cloudflare Workers (Recommended)**

Cloudflare Workers can run Python now! Deploy entire Django app to Workers.

**Create wrangler.toml:**
```toml
name = "consignment-delivery"
main = "src/index.py"
compatibility_date = "2026-07-18"

[vars]
DEBUG = "false"

[[d1_databases]]
binding = "DB"
database_name = "consignment-delivery-db"
database_id = "YOUR_DATABASE_ID_HERE"

[[r2_buckets]]
binding = "MEDIA"
bucket_name = "consignment-media"

[observability]
enabled = true
```

### **Option B: Keep Render + Use D1 via API**

Use D1 HTTP API to connect from Render deployment.

---

## 🔑 Environment Variables

### **For Cloudflare Workers:**
```bash
# Set secrets
wrangler secret put SECRET_KEY
wrangler secret put R2_ACCESS_KEY_ID
wrangler secret put R2_SECRET_ACCESS_KEY
```

### **For Render + D1 API:**
```env
USE_D1=True
D1_DATABASE_ID=your-database-id
D1_ACCOUNT_ID=your-cloudflare-account-id
D1_API_TOKEN=your-api-token
```

---

## 📊 D1 Database Schema Migration

### **Run Migrations:**

```bash
# Export Django schema to SQL
python manage.py sqlmigrate accounts 0001 > schema.sql
python manage.py sqlmigrate packages 0001 >> schema.sql
python manage.py sqlmigrate tracking 0001 >> schema.sql

# Execute on D1
wrangler d1 execute consignment-delivery-db --file=schema.sql
```

Or use Wrangler migrations:

```bash
# Initialize migrations
wrangler d1 migrations create consignment-delivery-db initial

# Edit migrations/0001_initial.sql with Django schema

# Apply migrations
wrangler d1 migrations apply consignment-delivery-db
```

---

## 🎯 Recommended Architecture

### **Best Setup for Your Use Case:**

```
┌─────────────────────────────────────────┐
│   Cloudflare Ecosystem (All-in-One)    │
├─────────────────────────────────────────┤
│                                         │
│  🌐 Cloudflare Workers                 │
│     ├── Django App (Python)            │
│     └── Edge Computing (Global)        │
│                                         │
│  🗄️  Cloudflare D1                     │
│     ├── SQLite (Serverless)            │
│     └── Auto-replicated                │
│                                         │
│  📦 Cloudflare R2                      │
│     ├── Delivery Photos                │
│     └── Signatures                     │
│                                         │
│  🚀 Benefits:                          │
│     ✅ All in one dashboard            │
│     ✅ Zero cold starts                │
│     ✅ Global CDN                      │
│     ✅ Free tier generous              │
│     ✅ Simpler billing                 │
└─────────────────────────────────────────┘
```

---

## 🆚 D1 vs PostgreSQL (Neon)

| Feature | Cloudflare D1 | Neon PostgreSQL |
|---------|---------------|-----------------|
| **Database** | SQLite | PostgreSQL |
| **Free Storage** | 5 GB | 512 MB |
| **Reads/Day** | 5 million | Unlimited |
| **Writes/Day** | 100,000 | Limited by compute |
| **Cold Starts** | None | ~100ms |
| **Global** | Yes (replicated) | Single region |
| **Django Compat** | Good (SQLite) | Excellent |
| **Cost** | Free tier huge | Free tier limited |

**For your delivery tracking:** D1 is perfect! ✅

---

## 🚀 Quick Start (Easiest Path)

### **Step 1: Create D1 Database**
```bash
npm install -g wrangler
wrangler login
wrangler d1 create consignment-delivery-db
```

### **Step 2: Note Database ID**
Copy the `database_id` from output.

### **Step 3: Choose Deployment:**

**Option A - Deploy to Cloudflare Workers:**
- I'll create the Workers configuration
- Deploy with `wrangler deploy`
- Everything in one Cloudflare dashboard

**Option B - Stay on Render + Use D1:**
- Use D1 HTTP API from Render
- Keep current Render setup
- Access D1 via Cloudflare API

---

## ⚡ Which Option Do You Prefer?

**I recommend Option A (Cloudflare Workers)** because:
1. ✅ Everything in Cloudflare (R2 + D1 + Workers)
2. ✅ Simpler management
3. ✅ Better performance (edge computing)
4. ✅ More generous free tier

**Or stay with Option B (Render)** if you prefer:
- Keep existing Render deployment
- Use D1 as database backend only

---

**Which would you like me to set up?**

1. **Full Cloudflare Workers deployment** (D1 + R2 + Workers)
2. **Render + D1 via API** (hybrid approach)
3. **Just create D1 database** and I'll configure it

Let me know and I'll configure it for you! 🚀
