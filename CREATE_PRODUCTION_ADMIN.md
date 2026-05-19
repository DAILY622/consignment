# 👤 Create Production Superuser on Heroku

## Using Heroku CLI

### Option 1: Interactive Mode (Recommended)
```bash
heroku run python manage.py createsuperuser --app consignment-site-2ac0cae70da0
```

**You'll be prompted for:**
- Username: (your choice, e.g., `admin`)
- Email: (your email)
- Password: (secure password)
- Password (again): (confirm password)

### Option 2: One-Line Command (Non-Interactive)
```bash
heroku run python manage.py createsuperuser --username admin --email admin@example.com --noinput --app consignment-site-2ac0cae70da0
```

Then set password:
```bash
heroku run python manage.py shell --app consignment-site-2ac0cae70da0
```

In the Python shell:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='admin')
user.set_password('YourSecurePassword123!')
user.save()
exit()
```

---

## Using Heroku Dashboard Console

1. Go to: https://dashboard.heroku.com/apps/consignment-site-2ac0cae70da0
2. Click **"More"** → **"Run console"**
3. Enter command: `python manage.py createsuperuser`
4. Click **"Run"**
5. Follow prompts to create admin user

---

## After Creating Admin

### Login to Production Admin Panel
Visit: https://consignment-site-2ac0cae70da0.herokuapp.com/admin/

Use credentials you just created:
- Username: (what you set)
- Password: (what you set)

### What You Can Do
- ✅ Create demo packages
- ✅ Update package locations
- ✅ Manage users (customers, drivers)
- ✅ View tracking history
- ✅ Update site settings
- ✅ Test all map features

---

## 🎯 Quick Admin Commands Reference

### Check if admin exists
```bash
heroku run python manage.py shell --app consignment-site-2ac0cae70da0
```
```python
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(is_superuser=True).values('username', 'email')
```

### Reset admin password
```bash
heroku run python manage.py changepassword admin --app consignment-site-2ac0cae70da0
```

### Create staff user (not superuser)
```bash
heroku run python manage.py shell --app consignment-site-2ac0cae70da0
```
```python
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.create_user('staff', 'staff@example.com', 'password')
user.is_staff = True
user.save()
```

---

## ⚠️ Important Notes

### Security Best Practices
1. **Strong Password**: Use at least 12 characters with numbers, symbols
2. **Unique Email**: Use your real email for password recovery
3. **Don't Share**: Keep admin credentials private
4. **Regular Updates**: Change password every 90 days

### Heroku CLI Installation
If you don't have Heroku CLI installed:
- Download: https://devcenter.heroku.com/articles/heroku-cli
- Or use PowerShell: `winget install Heroku.HerokuCLI`

### Login to Heroku CLI
```bash
heroku login
```
This opens browser for authentication.

---

**Status**: Ready to create admin once Heroku is reconnected!

**Next**: After admin creation, you can seed demo packages for testing.
