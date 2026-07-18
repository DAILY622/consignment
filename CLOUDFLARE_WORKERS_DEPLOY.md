# Cloudflare Workers + D1 + R2 - Complete Setup Guide

## 🌐 All-in-One Cloudflare Deployment

Deploy your entire Django consignment app to Cloudflare with D1 database and R2 storage!

---

## ✅ **Prerequisites**

- Cloudflare account (free)
- Node.js installed (for Wrangler CLI)
- Git installed

---

## 🚀 **Quick Setup (5 Minutes)**

### **Step 1: Install Wrangler**

```bash
npm install
# or globally
npm install -g wrangler
```

### **Step 2: Login to Cloudflare**

```bash
wrangler login
```

This opens your browser to authenticate with Cloudflare.

### **Step 3: Create D1 Database**

```bash
npm run d1:create
# or
wrangler d1 create consignment-delivery-db
```

**Output:**
```
✅ Successfully created DB 'consignment-delivery-db'

[[d1_databases]]
binding = "DB"
database_name = "consignment-delivery-db"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

**IMPORTANT:** Copy the `database_id` and paste it into `wrangler.toml`:

```toml
[[d1_databases]]
binding = "DB"
database_name = "consignment-delivery-db"
database_id = "PASTE_YOUR_DATABASE_ID_HERE"  # ← Update this!
```

### **Step 4: Create R2 Bucket**

```bash
wrangler r2 bucket create consignment-media
```

**Or use existing bucket:**
Update `wrangler.toml`:
```toml
[[r2_buckets]]
binding = "MEDIA_BUCKET"
bucket_name = "your-existing-bucket-name"  # ← Update if reusing
```

### **Step 5: Set Secrets**

```bash
# Django SECRET_KEY
wrangler secret put SECRET_KEY
# When prompted, paste a secure random key

# R2 credentials (if not using binding)
wrangler secret put R2_ACCESS_KEY_ID
wrangler secret put R2_SECRET_ACCESS_KEY

# Database URL (for compatibility)
wrangler secret put DATABASE_URL
# Value: sqlite:///db.sqlite3
```

### **Step 6: Run Database Migrations**

```bash
# Export Django schema to SQL
python manage.py migrate --run-syncdb

# Create SQL dump
python manage.py sqlmigrate accounts 0001 > migrations/0001_initial.sql
python manage.py sqlmigrate packages 0001 >> migrations/0001_initial.sql
python manage.py sqlmigrate tracking 0001 >> migrations/0001_initial.sql
python manage.py sqlmigrate drivers 0001 >> migrations/0001_initial.sql
python manage.py sqlmigrate consignment 0001 >> migrations/0001_initial.sql

# Apply to D1
wrangler d1 execute consignment-delivery-db --file=migrations/0001_initial.sql
```

### **Step 7: Seed Demo Data**

```bash
# Create seed script
python manage.py dumpdata accounts packages tracking --indent 2 > seed_data.json

# Convert to SQL (you may need a script or do manually)
# For now, we can seed after deployment via Django admin
```

### **Step 8: Deploy!**

```bash
npm run deploy
# or
wrangler deploy
```

**Output:**
```
✨ Built successfully
🌍 Uploading...
✨ Uploaded successfully
🌏 Deploying...
✨ Deployed successfully

🌐 https://consignment-delivery.YOUR-SUBDOMAIN.workers.dev
```

### **Step 9: Test**

Visit your Workers URL:
```
https://consignment-delivery.YOUR-SUBDOMAIN.workers.dev
```

---

## 📊 **Cost Breakdown**

### **Cloudflare Free Tier (ALL Included):**

| Service | Free Tier | Cost Beyond Free |
|---------|-----------|------------------|
| **Workers** | 100,000 requests/day | $0.50/million |
| **D1 Database** | 5 GB storage, 5M reads/day | $0.75/M reads |
| **R2 Storage** | 10 GB storage | $0.015/GB/month |
| **Bandwidth** | UNLIMITED (zero egress) | $0 |

**Total for small business:** $0/month ✅

---

## 🔧 **Configuration Files**

### **wrangler.toml** (Created)
- Worker configuration
- D1 database binding
- R2 bucket binding
- Environment variables

### **package.json** (Created)
- NPM scripts for deployment
- Wrangler dev dependency

### **migrations/** (To create)
- SQL migration files
- Applied with `wrangler d1 execute`

---

## 🌍 **Custom Domain (Optional)**

### **Add Custom Domain:**

1. Go to Cloudflare Dashboard → Workers & Pages
2. Click your worker → Settings → Domains & Routes
3. Click "Add Custom Domain"
4. Enter: `delivery.yourdomain.com`
5. Cloudflare automatically sets up DNS

**Update wrangler.toml:**
```toml
[[routes]]
pattern = "delivery.yourdomain.com/*"
custom_domain = true
```

**Update Django settings:**
```env
ALLOWED_HOSTS=.workers.dev,.pages.dev,delivery.yourdomain.com
CSRF_TRUSTED_ORIGINS_EXTRA=https://delivery.yourdomain.com
```

---

## 🔄 **Development Workflow**

### **Local Development:**
```bash
# Run local dev server
npm run dev
# or
wrangler dev

# Visit: http://localhost:8787
```

### **Deploy Changes:**
```bash
# Make code changes
git add -A
git commit -m "Update feature"

# Deploy to Workers
npm run deploy

# Or auto-deploy via GitHub Actions (set up CI/CD)
```

### **View Logs:**
```bash
npm run tail
# or
wrangler tail
```

### **Database Commands:**
```bash
# Execute SQL
wrangler d1 execute consignment-delivery-db --command "SELECT * FROM packages_package LIMIT 10"

# Execute SQL file
wrangler d1 execute consignment-delivery-db --file=query.sql

# Backup database
wrangler d1 export consignment-delivery-db --output=backup.sql
```

---

## 📁 **Project Structure**

```
consignment/
├── wrangler.toml           # Cloudflare Workers config
├── package.json            # NPM scripts
├── worker.py               # Workers entry point (to create)
├── requirements.txt        # Python dependencies
├── migrations/             # D1 SQL migrations
│   └── 0001_initial.sql
├── consignment/            # Django project
├── packages/               # Django app
├── tracking/               # Django app
└── static/                 # Static files (auto-uploaded)
```

---

## ⚡ **Performance Benefits**

### **Cloudflare Workers vs Traditional Hosting:**

| Metric | Workers (Cloudflare) | Render/Heroku |
|--------|----------------------|---------------|
| **Cold Start** | 0ms ⚡ | 1-5 seconds |
| **Global CDN** | Built-in (300+ locations) | Extra cost |
| **Database** | D1 (edge-replicated) | Single region |
| **Bandwidth** | FREE unlimited | Charged/limited |
| **Scaling** | Automatic | Manual/costly |
| **Cost** | $0-5/month | $7-25/month |

---

## 🆘 **Troubleshooting**

### **"Database not found" error:**
```bash
# Check D1 databases
wrangler d1 list

# Verify database_id in wrangler.toml matches
```

### **"R2 bucket not found" error:**
```bash
# List buckets
wrangler r2 bucket list

# Create if missing
wrangler r2 bucket create consignment-media
```

### **"Cannot find module" error:**
Make sure requirements.txt is correct:
```bash
pip install -r requirements.txt
```

### **Migrations not applied:**
```bash
# Re-run migrations
wrangler d1 execute consignment-delivery-db --file=migrations/0001_initial.sql
```

---

## ✅ **Next Steps**

1. ✅ Create D1 database (`npm run d1:create`)
2. ✅ Update `database_id` in wrangler.toml
3. ✅ Create R2 bucket (or reuse existing)
4. ✅ Set secrets (`wrangler secret put SECRET_KEY`)
5. ✅ Run migrations
6. ✅ Deploy (`npm run deploy`)
7. ✅ Test your Workers URL
8. ✅ Add custom domain (optional)

---

**Ready to deploy?** Run:

```bash
npm install
npm run setup
npm run deploy
```

🚀 **Your app will be live on Cloudflare Workers!**
