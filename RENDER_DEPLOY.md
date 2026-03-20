# Deploying to Render

## Quick Deploy (Blueprint)

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click **New** → **Blueprint**
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml` and configure:
   - PostgreSQL database (free tier)
   - Web service with auto-deploy

## Manual Deploy

### Step 1: Create PostgreSQL Database

1. In Render Dashboard, click **New** → **PostgreSQL**
2. Name: `consignment-db`
3. Plan: Free
4. Click **Create Database**
5. Copy the **Internal Database URL**

### Step 2: Create Web Service

1. Click **New** → **Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `consignment-website`
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn consignment.wsgi:application`

4. Add Environment Variables:
   - `DATABASE_URL` = (paste Internal Database URL)
   - `SECRET_KEY` = (generate a secure key)
   - `DEBUG` = `False`

5. Click **Create Web Service**

## Post-Deploy

### Create Superuser

1. Go to your web service in Render
2. Click **Shell** tab
3. Run:
   ```bash
   python manage.py createsuperuser
   ```

### Access Admin

Visit: `https://your-app.onrender.com/admin/`

The admin panel now uses the Jazzmin theme for a modern look!

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (auto-set with Blueprint) |
| `SECRET_KEY` | Django secret key (auto-generated with Blueprint) |
| `DEBUG` | Set to `False` for production |

## Notes

- Free tier services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Free PostgreSQL database has 1GB storage limit
