-- D1 Database Schema for Consignment Delivery System
-- SQLite schema compatible with Cloudflare D1

-- Users table
CREATE TABLE IF NOT EXISTS accounts_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT NOT NULL,
    last_login TEXT,
    is_superuser INTEGER NOT NULL DEFAULT 0,
    username TEXT NOT NULL UNIQUE,
    first_name TEXT,
    last_name TEXT,
    email TEXT NOT NULL,
    is_staff INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    date_joined TEXT NOT NULL,
    user_type TEXT NOT NULL DEFAULT 'customer',
    phone_number TEXT,
    address TEXT,
    city TEXT,
    country TEXT,
    postal_code TEXT
);

-- Packages table
CREATE TABLE IF NOT EXISTS packages_package (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_number TEXT NOT NULL UNIQUE,
    sender_name TEXT NOT NULL,
    sender_email TEXT NOT NULL,
    sender_phone TEXT NOT NULL,
    sender_address TEXT NOT NULL,
    sender_city TEXT NOT NULL,
    sender_country TEXT NOT NULL,
    sender_postal_code TEXT NOT NULL,
    receiver_name TEXT NOT NULL,
    receiver_email TEXT NOT NULL,
    receiver_phone TEXT NOT NULL,
    receiver_address TEXT NOT NULL,
    receiver_city TEXT NOT NULL,
    receiver_country TEXT NOT NULL,
    receiver_postal_code TEXT NOT NULL,
    weight REAL NOT NULL,
    dimensions TEXT,
    description TEXT,
    declared_value REAL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    estimated_delivery TEXT,
    actual_delivery TEXT,
    customer_id INTEGER,
    driver_id INTEGER,
    current_location TEXT,
    photo_url TEXT,
    signature_url TEXT,
    special_instructions TEXT,
    FOREIGN KEY (customer_id) REFERENCES accounts_user(id),
    FOREIGN KEY (driver_id) REFERENCES accounts_user(id)
);

-- Tracking History table
CREATE TABLE IF NOT EXISTS tracking_trackinghistory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    location TEXT NOT NULL,
    description TEXT,
    latitude REAL,
    longitude REAL,
    timestamp TEXT NOT NULL,
    updated_by_id INTEGER,
    FOREIGN KEY (package_id) REFERENCES packages_package(id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by_id) REFERENCES accounts_user(id)
);

-- Route Waypoints table
CREATE TABLE IF NOT EXISTS tracking_routewaypoint (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    location TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    sequence_order INTEGER NOT NULL,
    estimated_arrival TEXT,
    actual_arrival TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    FOREIGN KEY (package_id) REFERENCES packages_package(id) ON DELETE CASCADE
);

-- Proof of Delivery table
CREATE TABLE IF NOT EXISTS drivers_proofofdelivery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL UNIQUE,
    delivered_at TEXT NOT NULL,
    recipient_name TEXT NOT NULL,
    recipient_signature TEXT,
    delivery_photo TEXT,
    notes TEXT,
    driver_id INTEGER,
    FOREIGN KEY (package_id) REFERENCES packages_package(id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES accounts_user(id)
);

-- Site Settings table
CREATE TABLE IF NOT EXISTS consignment_sitesettings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_name TEXT NOT NULL DEFAULT 'DailyFX Delivery',
    site_logo TEXT,
    contact_email TEXT NOT NULL DEFAULT 'support@dailyfx.com',
    contact_phone TEXT NOT NULL DEFAULT '+1234567890',
    address TEXT,
    map_provider TEXT NOT NULL DEFAULT 'openstreetmap',
    map_api_key TEXT,
    marker_opacity REAL NOT NULL DEFAULT 0.8,
    route_opacity REAL NOT NULL DEFAULT 0.6,
    route_line_color TEXT NOT NULL DEFAULT '#FF5722',
    default_zoom_level INTEGER NOT NULL DEFAULT 10
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_packages_tracking ON packages_package(tracking_number);
CREATE INDEX IF NOT EXISTS idx_packages_status ON packages_package(status);
CREATE INDEX IF NOT EXISTS idx_packages_customer ON packages_package(customer_id);
CREATE INDEX IF NOT EXISTS idx_packages_driver ON packages_package(driver_id);
CREATE INDEX IF NOT EXISTS idx_tracking_package ON tracking_trackinghistory(package_id);
CREATE INDEX IF NOT EXISTS idx_tracking_timestamp ON tracking_trackinghistory(timestamp);
CREATE INDEX IF NOT EXISTS idx_waypoints_package ON tracking_routewaypoint(package_id);
CREATE INDEX IF NOT EXISTS idx_waypoints_sequence ON tracking_routewaypoint(sequence_order);
