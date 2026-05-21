#!/usr/bin/env python
"""
Check Active Tracking on Render Production Database
Run this to see live packages on your deployed Render instance
"""

import os
import sys
import psycopg2
from datetime import datetime

# Render Production Database URL (from render.yaml)
DATABASE_URL = "postgresql://neondb_owner:npg_Hm6oMiXSaTc1@ep-soft-queen-ap4bqkwz-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require"

def check_production_tracking():
    """Check active packages in production database"""
    try:
        print("=" * 70)
        print("🚀 RENDER PRODUCTION - ACTIVE PACKAGE TRACKING")
        print("=" * 70)
        print()
        
        # Connect to production database
        print("📡 Connecting to Neon PostgreSQL (Render Production)...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("✅ Connected successfully!\n")
        
        # Check packages
        cursor.execute("""
            SELECT tracking_number, status, sender_city, sender_country, 
                   receiver_city, receiver_country, created_at
            FROM packages_package
            ORDER BY created_at DESC
        """)
        packages = cursor.fetchall()
        
        if not packages:
            print("⚠️  No packages found in production database")
            print("💡 You may need to create packages via the admin panel\n")
        else:
            print(f"📦 ACTIVE PACKAGES: {len(packages)}\n")
            for pkg in packages:
                tracking, status, s_city, s_country, r_city, r_country, created = pkg
                print(f"{'=' * 70}")
                print(f"📦 {tracking}")
                print(f"   Status: {status.upper()}")
                print(f"   Route: {s_city}, {s_country} → {r_city}, {r_country}")
                print(f"   Created: {created}")
                
                # Get latest tracking location
                cursor.execute("""
                    SELECT location, latitude, longitude, timestamp
                    FROM tracking_trackinghistory
                    WHERE package_id = (
                        SELECT id FROM packages_package 
                        WHERE tracking_number = %s
                    )
                    ORDER BY timestamp DESC, id DESC
                    LIMIT 1
                """, (tracking,))
                
                location = cursor.fetchone()
                if location:
                    loc, lat, lng, ts = location
                    print(f"   📍 Current Location: {loc}")
                    print(f"   📌 Coordinates: ({lat}, {lng})")
                    print(f"   🕐 Last Update: {ts}")
                else:
                    print(f"   📍 No tracking updates yet")
                print()
        
        # Check route waypoints
        cursor.execute("SELECT COUNT(*) FROM tracking_routewaypoint")
        waypoint_count = cursor.fetchone()[0]
        
        # Check users
        cursor.execute("SELECT COUNT(*) FROM accounts_user")
        user_count = cursor.fetchone()[0]
        
        print("=" * 70)
        print("📊 DATABASE STATISTICS")
        print("=" * 70)
        print(f"👥 Users: {user_count}")
        print(f"📦 Packages: {len(packages)}")
        print(f"🗺️  Route Waypoints: {waypoint_count}")
        print()
        
        cursor.close()
        conn.close()
        
        print("=" * 70)
        print("🌐 ACCESS YOUR RENDER DEPLOYMENT")
        print("=" * 70)
        print()
        print("Your Render app URL should be:")
        print("🔗 https://dailyfx-delivery.onrender.com")
        print()
        print("Admin Panel:")
        print("🔐 https://dailyfx-delivery.onrender.com/admin")
        print()
        print("Track Package:")
        print("📍 https://dailyfx-delivery.onrender.com/track/<tracking-number>")
        print()
        print("=" * 70)
        
    except psycopg2.Error as e:
        print(f"❌ Database Error: {e}")
        print()
        print("💡 Possible issues:")
        print("   1. Database not yet created on Render")
        print("   2. Migrations not run: python manage.py migrate")
        print("   3. Database connection string changed")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_production_tracking()
