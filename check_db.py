import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== CHECKING FOR DELIVERY PACKAGES ===\n")

# Check if packages table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='packages_package'")
if not cursor.fetchone():
    print("❌ No packages table found. Database may not be set up yet.")
else:
    # Query packages
    cursor.execute("""
        SELECT 
            tracking_number, 
            status, 
            sender_city || ', ' || sender_country as origin,
            receiver_city || ', ' || receiver_country as destination,
            created_at
        FROM packages_package
        ORDER BY created_at DESC
    """)
    
    packages = cursor.fetchall()
    
    if packages:
        print(f"✅ Found {len(packages)} package(s):\n")
        for pkg in packages:
            print(f"  📦 {pkg[0]}")
            print(f"     Status: {pkg[1]}")
            print(f"     Route: {pkg[2]} → {pkg[3]}")
            print(f"     Created: {pkg[4]}")
            print()
        
        # Check tracking history
        print("=== TRACKING LOCATIONS ===\n")
        for pkg in packages:
            cursor.execute("""
                SELECT location, timestamp, latitude, longitude
                FROM tracking_trackinghistory
                WHERE package_id = (SELECT id FROM packages_package WHERE tracking_number = ?)
                ORDER BY timestamp DESC
                LIMIT 1
            """, (pkg[0],))
            
            location = cursor.fetchone()
            if location:
                print(f"  📍 {pkg[0]}: {location[0]}")
                print(f"     Coordinates: ({location[2]}, {location[3]})")
                print(f"     Last update: {location[1]}")
            else:
                print(f"  📍 {pkg[0]}: No tracking data yet")
            print()
    else:
        print("📭 No packages found in the database.")
        print("\n💡 Tip: Run 'python manage.py seed_data' to create sample packages")

conn.close()
