#!/usr/bin/env bash
# ============================================
# Render Deployment Build Script
# ============================================
# Exit on error
set -o errexit

echo "🚀 Starting Render deployment build..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files (for Django admin and static assets)
echo "📂 Collecting static files..."
python manage.py collectstatic --no-input --clear

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --no-input

# Create superuser if needed (optional, comment out if not needed)
echo "👤 Setting up admin user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@dailyfx.com', 'admin123')
    print('✅ Admin user created: admin/admin123')
else:
    print('✅ Admin user already exists')
" || echo "⚠️  Skipping superuser creation (might already exist)"

# Seed demo data (creates sample packages if needed)
echo "🌱 Seeding demo data..."
python manage.py seed_data || echo "⚠️  Demo data seeding skipped (command not found or already seeded)"

echo "✅ Build completed successfully!"
