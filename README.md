# 🚚 E-Cognite - Consignment & Delivery Tracking System

A full-featured UK parcel delivery and tracking platform built with Django and its built-in admin panel.

## Features

- **📦 Package Management** - Create, track, and manage shipments
- **🗺️ Live GPS Tracking** - Real-time package location with interactive maps
- **👥 Multi-Role System** - Admin, Customer, and Driver accounts
- **📍 Route Visualization** - See package journey from origin to destination
- **📱 Driver Portal** - Mobile-friendly delivery updates with proof of delivery
- **🎛️ Admin Dashboard** - Custom admin with live map and quick actions

## Screenshots

### Tracking Page
- Visual progress bar showing delivery status
- Live map with truck position
- Detailed tracking timeline

### Admin Dashboard
- Package statistics
- Live map of all active deliveries
- Quick action buttons

## Tech Stack

- **Backend**: Django 6.0
- **Database**: SQLite (easily switchable to PostgreSQL)
- **Frontend**: Tailwind CSS (via CDN)
- **Maps**: Leaflet.js + OpenStreetMap
- **Auth**: Django built-in authentication

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/consign.git
cd consign

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install django pillow

# Run migrations
python manage.py migrate

# Seed sample data
python manage.py seed_data

# Run development server
python manage.py runserver
```

## Default Accounts

| Role | Username | Email | Password |
|------|----------|-------|----------|
| Admin | `admin` | `admin@example.com` | `admin123` |
| Customer | `user` | `user@example.com` | `password` |
| Driver | `driver` | `driver@example.com` | `driver123` |

## Sample Tracking Numbers

Try tracking: `ECG-DEMO0000` through `ECG-DEMO0009`

## URLs

| Page | URL |
|------|-----|
| Home | http://localhost:8000/ |
| Track Package | http://localhost:8000/track/ |
| User Dashboard | http://localhost:8000/dashboard/ |
| Admin Panel | http://localhost:8000/admin/ |
| Driver Portal | http://localhost:8000/driver/ |

## Project Structure

```
consign/
├── accounts/          # User management & authentication
├── packages/          # Package/shipment CRUD
├── tracking/          # GPS tracking history
├── drivers/           # Driver portal & proof of delivery
├── consignment/       # Django project settings
├── templates/         # HTML templates
├── static/            # CSS, JS, images
└── media/             # User uploads (photos, signatures)
```

## Admin Features

- **Custom Dashboard** with live statistics
- **Interactive Map** for updating package locations
- **Bulk Actions** (mark delivered, assign drivers)
- **Inline Tracking History** on package detail
- **Status Badges** with color coding

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first.
