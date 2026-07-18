# Using Existing R2 Credentials from Another Website

## ✅ YES - You Can Reuse R2 Credentials!

Cloudflare R2 allows you to use the same account and credentials across multiple websites/projects.

---

## 🎯 Three Options for Sharing R2

### **Option 1: Same Bucket (Simplest)** ✅

Use your existing R2 bucket without any changes. Files will be automatically organized by the Django app.

**Configuration (.env):**
```env
USE_R2=True
R2_ACCESS_KEY_ID=your_existing_access_key_from_other_site
R2_SECRET_ACCESS_KEY=your_existing_secret_key_from_other_site
R2_BUCKET_NAME=your_existing_bucket_name
R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
```

**Bucket Structure:**
```
your-existing-bucket/
├── delivery_photos/        ← Consignment site photos
│   ├── photo_abc123.jpg
│   └── photo_def456.jpg
├── signatures/             ← Consignment site signatures
│   ├── sig_xyz789.png
│   └── sig_uvw012.png
└── [other-site-files]/     ← Your other website's files
```

**Pros:**
- ✅ No setup needed - just copy credentials
- ✅ One bucket to manage
- ✅ Stays within 10GB free tier easily

**Cons:**
- ⚠️ All files in one bucket (but organized by folders)

---

### **Option 2: Separate Bucket (Recommended)** ⭐

Create a new bucket for this consignment site but use the same API credentials.

**Step 1: Create New Bucket**
1. Go to Cloudflare Dashboard → R2
2. Click **"Create bucket"**
3. Name: `consignment-delivery-media` (or any name you prefer)
4. Region: Automatic
5. Click **"Create bucket"**

**Step 2: Use Existing API Tokens**
```env
USE_R2=True
R2_ACCESS_KEY_ID=your_existing_access_key_from_other_site  # SAME
R2_SECRET_ACCESS_KEY=your_existing_secret_key_from_other_site  # SAME
R2_BUCKET_NAME=consignment-delivery-media  # NEW BUCKET NAME
R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com  # SAME
```

**Pros:**
- ✅ Clean separation between projects
- ✅ Same credentials work for all buckets
- ✅ Better organization

**Cons:**
- ⚠️ Need to create one more bucket (5 minutes)

---

### **Option 3: Same Bucket with Prefix** 🎯

Use the same bucket but add a prefix like `consignment/` to all files.

**Step 1: Add prefix support to settings**

I can add this to your `settings.py`:

```python
# In the R2 configuration section:
AWS_LOCATION = os.environ.get('R2_PREFIX', 'consignment')  # Prefix for this site
```

**Step 2: Configuration (.env):**
```env
USE_R2=True
R2_ACCESS_KEY_ID=your_existing_access_key
R2_SECRET_ACCESS_KEY=your_existing_secret_key
R2_BUCKET_NAME=your_existing_bucket_name
R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
R2_PREFIX=consignment  # NEW: Prefix for this site
```

**Bucket Structure:**
```
your-existing-bucket/
├── consignment/                    ← All consignment site files here
│   ├── delivery_photos/
│   │   ├── photo_abc123.jpg
│   │   └── photo_def456.jpg
│   └── signatures/
│       ├── sig_xyz789.png
│       └── sig_uvw012.png
└── [other-site-files-at-root]/    ← Your other site's files
```

**Would you like me to add prefix support to the code?**

---

## 💡 My Recommendation

**For you:** Use **Option 1 (Same Bucket)** - Simplest!

**Why?**
- ✅ No extra setup - just copy your existing R2 credentials
- ✅ Files are already organized by Django folders (`delivery_photos/`, `signatures/`)
- ✅ Works immediately with zero configuration changes
- ✅ If your other site uses different folder names, they won't conflict

**Your existing R2 setup from other site will work perfectly!**

---

## 🚀 Quick Setup (Option 1)

**1. Find your existing R2 credentials:**
   - Go to your other website's `.env` or settings
   - Copy: Access Key ID, Secret Key, Bucket Name, Endpoint URL

**2. Add to this project's `.env`:**
```env
USE_R2=True
R2_ACCESS_KEY_ID=<paste from other site>
R2_SECRET_ACCESS_KEY=<paste from other site>
R2_BUCKET_NAME=<paste from other site>
R2_ENDPOINT_URL=<paste from other site>
```

**3. Test locally:**
```bash
python manage.py runserver
# Upload a test delivery photo via admin
# Check your R2 bucket - file should appear!
```

**4. Deploy to Render:**
Add the same environment variables in Render Dashboard.

---

## 📊 Storage Impact

**Example scenario:**
- Your other site: 2GB of files
- This consignment site: ~500MB (1000 deliveries × 500KB photos)
- **Total: 2.5GB** - Still well within 10GB free tier! ✅

**File organization is automatic:**
- Other site: Uses its own folders
- Consignment site: Uses `delivery_photos/` and `signatures/`
- No conflicts!

---

## ⚠️ Important Notes

1. **Same API Credentials Work Across Buckets**
   - One set of R2 API tokens can access ALL buckets in your account
   - No need to create new tokens for each project

2. **Bucket Names Must Be Unique**
   - If creating a new bucket (Option 2), choose a unique name
   - Example: `consignment-delivery-media`

3. **Folder Names Don't Conflict**
   - Django automatically creates `delivery_photos/` and `signatures/`
   - Your other site likely uses different folder names
   - They can coexist in the same bucket

4. **Billing**
   - All buckets in same account share the 10GB free tier
   - Monitor total usage across all sites

---

## 🔍 How to Find Your Existing R2 Credentials

**From your other website:**

**If deployed on Render/Railway/Heroku:**
- Go to your app's environment variables
- Look for: `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`, `R2_ENDPOINT_URL`

**If you have the `.env` file:**
```env
# Look for these variables:
R2_ACCESS_KEY_ID=xxxxx
R2_SECRET_ACCESS_KEY=xxxxx
R2_BUCKET_NAME=xxxxx
R2_ENDPOINT_URL=https://xxxxx.r2.cloudflarestorage.com
```

**From Cloudflare Dashboard:**
1. Go to R2 → Overview
2. See your buckets listed
3. For API tokens: R2 → Manage R2 API Tokens

---

## ✅ Ready to Use!

**Just copy your existing R2 credentials to this project's `.env` file and you're done!**

No need to:
- ❌ Create new R2 account
- ❌ Create new API tokens
- ❌ Create new bucket (unless you want separate storage)

**Your existing R2 setup will work perfectly for this consignment site!** 🎉

---

**Need help?** Let me know which option you prefer and I can help configure it!
