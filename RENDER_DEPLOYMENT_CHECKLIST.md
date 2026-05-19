# 🚀 Render Deployment Checklist

## Pre-Deployment Verification

### Local Environment
- [ ] All changes committed to Git
- [ ] No sensitive data in repository (.env files in .gitignore)
- [ ] Requirements.txt up to date: `pip freeze > requirements.txt`
- [ ] Database migrations created: `python manage.py makemigrations`
- [ ] Code pushed to GitHub: `git push origin main`

### Configuration Files
- [ ] ✅ `render.yaml` - Updated and ready
- [ ] ✅ `build.sh` - Executable and functional
- [ ] ✅ `requirements.txt` - All dependencies listed
- [ ] ✅ `runtime.txt` - Python version specified
- [ ] ✅ Settings configured for Render (.onrender.com in ALLOWED_HOSTS)

---

## Render Setup

### 1. Create Render Account
- [ ] Sign up at https://render.com
- [ ] Connect GitHub account
- [ ] Verify email address

### 2. Deploy Using Blueprint
- [ ] Navigate to Render Dashboard
- [ ] Click "New +" → "Blueprint"
- [ ] Select your GitHub repository
- [ ] Confirm `render.yaml` detected
- [ ] Click "Apply" to deploy

### 3. Monitor Build Process
- [ ] Watch build logs for errors
- [ ] Verify "Installing dependencies" completes
- [ ] Verify "Collecting static files" succeeds
- [ ] Verify "Running migrations" succeeds
- [ ] Verify "Build successful" message
- [ ] Wait for "Live" status (green indicator)

---

## Post-Deployment Configuration

### Database & Admin
- [ ] Verify database created: `consignment-db`
- [ ] Open web service Shell tab
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Note admin credentials securely

### Environment Variables
Verify these are set (Render Dashboard → Service → Environment):
- [ ] `DATABASE_URL` - Auto-set from database
- [ ] `SECRET_KEY` - Generate new secure key
- [ ] `DEBUG` - Set to `False`
- [ ] `PYTHON_VERSION` - Set to `3.12.0`
- [ ] `ALLOWED_HOSTS` - Set to `.onrender.com`

Optional (if using email):
- [ ] `EMAIL_HOST`
- [ ] `EMAIL_PORT`
- [ ] `EMAIL_USE_TLS`
- [ ] `EMAIL_HOST_USER`
- [ ] `EMAIL_HOST_PASSWORD`

---

## Testing & Verification

### Basic Functionality
- [ ] Homepage loads: `https://your-app.onrender.com`
- [ ] No 404 or 500 errors
- [ ] Static files loading (CSS/JS/images)
- [ ] Admin accessible: `https://your-app.onrender.com/admin`
- [ ] Can login with superuser credentials

### Database Operations
- [ ] Admin dashboard loads
- [ ] Can view existing records
- [ ] Can create new package/user
- [ ] Can edit existing records
- [ ] Can delete records
- [ ] Search functionality works

### User Features
- [ ] User registration works (if enabled)
- [ ] User login/logout works
- [ ] Package tracking works
- [ ] Forms submit correctly
- [ ] File uploads work (if applicable)

### Performance & Security
- [ ] HTTPS working (automatic on Render)
- [ ] No security warnings in browser
- [ ] Page load times acceptable
- [ ] No console errors in browser DevTools
- [ ] CSRF protection working

---

## Monitoring & Maintenance

### Set Up Monitoring
- [ ] Check Render Dashboard metrics (CPU, Memory, Requests)
- [ ] Review logs for errors
- [ ] Set up email notifications for downtime
- [ ] Bookmark service dashboard

### Documentation
- [ ] Update README with live URL
- [ ] Document any custom configuration
- [ ] Share admin credentials with team (securely)
- [ ] Update API endpoints (if applicable)

---

## Troubleshooting Common Issues

### If Build Fails
1. Check build logs for specific error
2. Verify all files committed to Git
3. Check requirements.txt has all dependencies
4. Ensure Python version matches locally
5. Try manual deploy: "Manual Deploy" → "Clear build cache & deploy"

### If Static Files Don't Load
1. Verify WhiteNoise in MIDDLEWARE
2. Check STATIC_ROOT and STATIC_URL in settings
3. Run: `python manage.py collectstatic --noinput`
4. Check build logs for collectstatic output

### If Database Connection Fails
1. Verify DATABASE_URL is set
2. Check database service is "Available" (green)
3. Ensure psycopg2-binary in requirements.txt
4. Check database credentials match

### If 502 Bad Gateway
1. Check service logs for Python errors
2. Verify Gunicorn start command correct
3. Ensure PORT environment variable used
4. Check for code syntax errors

---

## Going Live Checklist

### Before Production
- [ ] All features tested thoroughly
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Database backed up
- [ ] SSL/HTTPS verified
- [ ] Performance optimized

### Domain Setup (Optional)
- [ ] Custom domain purchased
- [ ] DNS records configured
- [ ] CNAME pointing to Render
- [ ] Update ALLOWED_HOSTS
- [ ] Update CSRF_TRUSTED_ORIGINS
- [ ] SSL certificate issued (automatic)

### Security Review
- [ ] DEBUG=False in production
- [ ] SECRET_KEY is secure and unique
- [ ] No secrets in Git history
- [ ] Admin URL secured (consider custom path)
- [ ] Rate limiting configured (if needed)
- [ ] User permissions reviewed

---

## Success Criteria

Your deployment is successful when:
- ✅ Website accessible via public URL
- ✅ Admin panel working
- ✅ Database operations functional
- ✅ Static files serving correctly
- ✅ No errors in logs
- ✅ HTTPS working
- ✅ Performance acceptable
- ✅ Team can access and use the app

---

## Next Steps After Deployment

1. **Monitor First 24 Hours**
   - Watch for errors in logs
   - Monitor performance metrics
   - Check user feedback

2. **Optimize Performance**
   - Enable caching if needed
   - Optimize database queries
   - Consider CDN for static files

3. **Set Up Backups**
   - Enable automatic database backups (paid plan)
   - Document backup/restore process
   - Test restoration procedure

4. **Plan for Updates**
   - Set up staging environment
   - Document deployment process
   - Create rollback plan

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Django Deployment**: See RENDER_DEPLOYMENT_GUIDE.md
- **Community Support**: https://community.render.com
- **Status Page**: https://status.render.com

---

## Quick Commands Reference

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Check deployment readiness
python manage.py check --deploy

# Seed sample data
python manage.py seed_data
```

---

**Status**: ⬜ Not Started | 🔄 In Progress | ✅ Complete | ❌ Issue

**Date Started**: _________________

**Date Completed**: _________________

**Deployed URL**: _________________

**Notes**: _________________
