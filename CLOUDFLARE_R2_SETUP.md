# Cloudflare R2 Setup Guide for DailyFX Delivery

This guide will help you set up Cloudflare R2 for persistent media file storage (delivery photos and signatures).

## ✅ What's Already Done

1. **Dependencies installed:**
   - `django-storages==1.14.4`
   - `boto3==1.35.93`

2. **Settings configured:**
   - `settings.py` updated with R2 integration
   - Environment variables added to `.env.example`
   - Toggle-based configuration (USE_R2=True/False)

3. **Media files that will be stored in R2:**
   - Delivery proof photos (`delivery_photos/`)
   - Customer signatures (`signatures/`)

---

## 🚀 Setup Steps

### Step 1: Create Cloudflare R2 Bucket

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to **R2 Object Storage**
3. Click **Create bucket**
4. Enter bucket name (e.g., `dailyfx-delivery-media`)
5. Choose your region
6. Click **Create bucket**

### Step 2: Generate R2 API Token

1. In R2 dashboard, click **Manage R2 API Tokens**
2. Click **Create API Token**
3. Give it a name (e.g., `dailyfx-delivery-app`)
4. Set permissions:
   - **Object Read & Write**
   - Optionally specify your bucket
5. Click **Create API Token**
6. **IMPORTANT:** Copy the credentials shown:
   - Access Key ID
   - Secret Access Key
   - Endpoint URL (format: `https://<account-id>.r2.cloudflarestorage.com`)

### Step 3: Configure Environment Variables

Add these to your `.env` file:

```env
# Enable R2 storage
USE_R2=True

# R2 Credentials (from Step 2)
R2_ACCESS_KEY_ID=your_access_key_id_here
R2_SECRET_ACCESS_KEY=your_secret_access_key_here
R2_BUCKET_NAME=dailyfx-delivery-media
R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com

# Optional: Custom domain for R2 (if you set one up)
# R2_CUSTOM_DOMAIN=media.yourdomain.com
```

### Step 4: (Optional) Set up Custom Domain

Instead of using the default R2 URL, you can use your own domain:

1. In R2 bucket settings, click **Settings** → **Public access**
2. Click **Add custom domain**
3. Enter your domain (e.g., `media.yourdomain.com`)
4. Add the CNAME record to your DNS:
   ```
   media.yourdomain.com  →  <your-bucket>.r2.cloudflarestorage.com
   ```
5. Wait for DNS propagation
6. Update your `.env`:
   ```env
   R2_CUSTOM_DOMAIN=media.yourdomain.com
   ```

### Step 5: Test the Setup

1. Restart your development server:
   ```bash
   python manage.py runserver
   ```

2. Create a test delivery with a photo:
   - Go to driver portal: http://localhost:8000/driver/
   - Upload a proof of delivery photo
   - Check your R2 bucket - the file should appear there!

---

## 🔄 Migration Guide: Moving Existing Files to R2

If you already have media files in the local `media/` folder:

```bash
# Install AWS CLI (or use S3cmd, rclone, etc.)
pip install awscli

# Configure AWS CLI for R2
aws configure --profile r2
# Enter your R2 Access Key ID
# Enter your R2 Secret Access Key
# Region: auto
# Output format: json

# Sync existing media files to R2
aws s3 sync media/ s3://dailyfx-delivery-media/ --endpoint-url=https://your-account-id.r2.cloudflarestorage.com --profile r2
```

---

## 🎯 Production Deployment

For Render/Railway/Heroku, add these environment variables in your platform's dashboard:

```
USE_R2=True
R2_ACCESS_KEY_ID=<your-access-key>
R2_SECRET_ACCESS_KEY=<your-secret-key>
R2_BUCKET_NAME=dailyfx-delivery-media
R2_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
```

**Important:** Never commit these credentials to Git!

---

## 💰 Pricing

Cloudflare R2 is very cost-effective:

- **Free Tier:** 10 GB storage per month
- **Storage:** $0.015/GB/month (beyond free tier)
- **Class A operations (upload):** $4.50 per million requests
- **Class B operations (download):** $0.36 per million requests
- **ZERO egress fees** (unlike AWS S3 which charges for downloads)

### Example costs for small delivery business:
- 1,000 deliveries/month with photos (avg 500KB each) = 500MB
- Storage: FREE (under 10GB limit)
- Uploads: ~$0.004/month
- **Total: ~$0/month** (well within free tier)

---

## 🔐 Security Best Practices

1. **Never commit credentials to Git**
   - Already in `.gitignore`: `.env`

2. **Use separate tokens for dev/production**
   - Create different API tokens for development and production

3. **Restrict token permissions**
   - Only grant "Object Read & Write" for specific buckets

4. **Enable bucket encryption** (optional)
   - Cloudflare R2 encrypts data at rest by default

5. **Set up bucket lifecycle policies** (optional)
   - Auto-delete old delivery photos after X days if needed

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'storages'"
**Solution:** Run `pip install -r requirements.txt`

### Issue: Files not appearing in R2
**Solution:** Check your environment variables:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(f'USE_R2: {os.getenv(\"USE_R2\")}')"
```

### Issue: "Access Denied" errors
**Solution:** Verify:
1. API token has correct permissions
2. Bucket name is correct
3. Endpoint URL matches your account

### Issue: Images not displaying on website
**Solution:** 
1. Check `MEDIA_URL` in settings
2. If using custom domain, ensure DNS is configured
3. Check browser console for CORS errors

---

## 📚 Additional Resources

- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/)
- [django-storages Documentation](https://django-storages.readthedocs.io/)
- [S3-Compatible API Reference](https://developers.cloudflare.com/r2/api/s3/)

---

## ✨ Benefits Summary

✅ **Persistent storage** - Files survive deployments  
✅ **Free tier** - 10GB storage included  
✅ **No egress fees** - Unlimited bandwidth  
✅ **Global CDN** - Fast delivery worldwide  
✅ **S3 compatible** - Easy migration path  
✅ **Automatic backups** - Cloudflare handles redundancy  

---

**Ready to enable R2?** Just set `USE_R2=True` in your `.env` file and add your credentials!
