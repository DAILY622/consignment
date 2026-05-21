#!/usr/bin/env python3
"""
Update Package Location to Kandahar, Afghanistan
"""

import os
import sys
import psycopg2
from datetime import datetime

DATABASE_URL = "postgresql://neondb_owner:npg_Hm6oMiXSaTc1@ep-soft-queen-ap4bqkwz-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require"

def update_to_kandahar():
    print("=" * 70)
    print("UPDATE LOCATION: Zahedan → Kandahar")
    print("=" * 70)
    print()
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("✅ Connected to production database\n")
        
        tracking_number = 'DFX-2XWJFI8R'
        
        # Get package
        cursor.execute("""
            SELECT id, tracking_number, status 
            FROM packages_package 
            WHERE tracking_number = %s
        """, (tracking_number,))
        
        package = cursor.fetchone()
        if not package:
            print(f"❌ Package not found!")
            return
        
        package_id = package[0]
        print(f"📦 Package: {tracking_number}")
        print(f"   Status: {package[2]}\n")
        
        # Get current location
        cursor.execute("""
            SELECT location FROM tracking_trackinghistory
            WHERE package_id = %s
            ORDER BY timestamp DESC, id DESC LIMIT 1
        """, (package_id,))
        
        current = cursor.fetchone()
        print(f"📍 Current: {current[0] if current else 'Unknown'}")
        print(f"🚚 Updating to: Kandahar, Afghanistan\n")
        
        # Insert Kandahar location
        cursor.execute("""
            INSERT INTO tracking_trackinghistory 
            (package_id, status, location, latitude, longitude, notes, timestamp)
            VALUES (%s, 'In Transit', 'Kandahar, Afghanistan', 31.6089, 65.7372, 
                    'Package moving through Afghanistan', NOW())
        """, (package_id,))
        
        conn.commit()
        
        print("✅ Location updated successfully!\n")
        
        # Verify
        cursor.execute("""
            SELECT location, latitude, longitude, timestamp
            FROM tracking_trackinghistory
            WHERE package_id = %s
            ORDER BY timestamp DESC, id DESC LIMIT 1
        """, (package_id,))
        
        updated = cursor.fetchone()
        print("=" * 70)
        print("UPDATED LOCATION")
        print("=" * 70)
        print(f"📍 Location: {updated[0]}")
        print(f"📌 GPS: {updated[1]}, {updated[2]}")
        print(f"🕐 Time: {updated[3]}")
        print()
        print(f"🌐 View: https://dailyfx-delivery.onrender.com/track/?q={tracking_number}")
        print()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    update_to_kandahar()
