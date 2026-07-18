# Using Cloudflare D1 with Render Deployment

## ✅ YES! You Can Use D1 with Render!

Cloudflare D1 has a REST API that can be accessed from Render (or any server).

---

## 🎯 **How It Works:**

```
┌──────────────────────────────────────┐
│         Render.com                   │
│  ┌────────────────────────────┐     │
│  │   Django App (Python)      │     │
│  │   ├── Views                │     │
│  │   ├── Models               │     │
│  │   └── D1 HTTP Client ───────────┼──┐
│  └────────────────────────────┘     │  │
└──────────────────────────────────────┘  │
                                          │
                                          │ HTTPS API Calls
                                          │
┌──────────────────────────────────────┐  │
│      Cloudflare D1 Database          │ ◄┘
│  ┌────────────────────────────┐     │
│  │  consignment-delivery-db   │     │
│  │  ID: f1f78eb9-...          │     │
│  │  Region: WEUR              │     │
│  └────────────────────────────┘     │
└──────────────────────────────────────┘
```

**Benefits:**
- ✅ Keep Render deployment (familiar, working)
- ✅ Use D1 database (5GB free, serverless)
- ✅ No PostgreSQL costs
- ✅ Faster than Neon in some cases

---

## 🔑 **Step 1: Get Cloudflare API Token**

### **Create API Token:**

1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Click **Create Token**
3. Use template: **Edit Cloudflare Workers**
4. Or create custom token with permissions:
   - **D1**: Edit
   - **Account**: Read
5. Click **Continue to summary**
6. Click **Create Token**
7. **COPY THE TOKEN** (you won't see it again!)

Example token:
```
v3KhB7X9mF2pQ8dL5nY4tR1wS6cE0oU3iA7jH9kM
```

### **Get Account ID:**

1. Go to: https://dash.cloudflare.com
2. Click **Workers & Pages** in sidebar
3. Your **Account ID** is shown on the right side

Example:
```
Account ID: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

## 📦 **Step 2: Install D1 HTTP Client**

Add to `requirements.txt`:

```txt
django==6.0.5
pillow==12.2.0
gunicorn==26.0.0
whitenoise==6.12.0
dj-database-url==3.1.2
psycopg2-binary==2.9.12
django-jazzmin==3.0.4
python-dotenv==1.0.1
django-storages==1.14.4
boto3==1.35.93
httpx==0.27.2  # ← Add this for D1 API calls
```

---

## 🔧 **Step 3: Create D1 Client**

Create file: `consignment/d1_client.py`

```python
import httpx
import os
from typing import List, Dict, Any

class D1Client:
    """Cloudflare D1 HTTP API Client for Django"""
    
    def __init__(self):
        self.account_id = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
        self.database_id = os.environ.get('D1_DATABASE_ID', 'f1f78eb9-e992-42cf-a30e-9b74970babe1')
        self.api_token = os.environ.get('CLOUDFLARE_API_TOKEN')
        self.base_url = f'https://api.cloudflare.com/client/v4/accounts/{self.account_id}/d1/database/{self.database_id}'
        
    def execute(self, sql: str, params: List = None) -> Dict[str, Any]:
        """Execute SQL query on D1"""
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'sql': sql,
            'params': params or []
        }
        
        with httpx.Client() as client:
            response = client.post(
                f'{self.base_url}/query',
                headers=headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    def query(self, sql: str, params: List = None) -> List[Dict]:
        """Execute SELECT query and return results"""
        result = self.execute(sql, params)
        if result.get('success'):
            return result.get('result', [{}])[0].get('results', [])
        return []

# Global instance
d1 = D1Client()
```

---

## ⚙️ **Step 4: Configure Environment Variables**

### **In Render Dashboard:**

Go to your service → **Environment** → Add these:

```env
# Cloudflare D1 Configuration
USE_D1=True
D1_DATABASE_ID=f1f78eb9-e992-42cf-a30e-9b74970babe1
CLOUDFLARE_ACCOUNT_ID=<your-account-id>
CLOUDFLARE_API_TOKEN=<your-api-token>

# Keep these for local dev (SQLite)
# DATABASE_URL will be ignored when USE_D1=True
```

---

## 🔄 **Step 5: Update Django Settings**

In `consignment/settings.py`:

```python
# Database Configuration
USE_D1 = os.environ.get('USE_D1', 'False').lower() == 'true'

if USE_D1:
    # Use Cloudflare D1 via HTTP API
    # Note: Django ORM doesn't work directly with D1 API
    # You'll need to use raw SQL or build a custom backend
    
    # For now, use SQLite locally, D1 for custom queries
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    # D1 client available via: from consignment.d1_client import d1
    D1_ENABLED = True
else:
    # Use PostgreSQL or SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        DATABASES['default'] = dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
```

---

## 📝 **Step 6: Using D1 in Your Code**

Example usage in views:

```python
from consignment.d1_client import d1

# Query packages
def get_package(tracking_number):
    sql = "SELECT * FROM packages_package WHERE tracking_number = ?"
    results = d1.query(sql, [tracking_number])
    return results[0] if results else None

# Insert package
def create_package(data):
    sql = """
    INSERT INTO packages_package (tracking_number, sender_name, status, created_at)
    VALUES (?, ?, ?, ?)
    """
    d1.execute(sql, [
        data['tracking_number'],
        data['sender_name'],
        data['status'],
        data['created_at']
    ])
```

---

## ⚠️ **Important Limitations:**

### **D1 API Limitations:**

1. **No Django ORM**: D1 HTTP API doesn't work with Django's ORM
   - You'll need to write raw SQL
   - Or use SQLite locally, D1 in production

2. **Latency**: HTTP API calls are slower than direct database connection
   - Each query = 1 HTTP request
   - Good for: occasional queries, async jobs
   - Not ideal for: high-frequency ORM operations

3. **Workaround**: Hybrid approach
   - Use SQLite on Render for ORM operations
   - Use D1 API for specific queries (analytics, reports)

---

## 🎯 **Better Alternative: Use SQLite on Render**

For Django with Render, I recommend:

### **Option A: SQLite + Persistent Disk (Simplest)**

```env
# In Render
# Just don't set DATABASE_URL
# Django will use SQLite automatically

# Add a persistent disk in Render:
# 1. Go to Render → Your service → Disks
# 2. Add disk: Mount path = /data
# 3. Update settings.py to use /data/db.sqlite3
```

### **Option B: Neon PostgreSQL (Best)**

```env
# Create free Neon database
# Add to Render:
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/db
```

### **Option C: Full Cloudflare Workers (Advanced)**

Deploy entire app to Cloudflare Workers with D1 native access.

---

## 💡 **My Recommendation:**

For **immediate 505 fix**:

1. **Use Neon PostgreSQL** (3 minutes setup)
   - Full Django ORM support
   - Free tier: 512MB
   - Just works!

2. **Keep D1 for later**
   - When you deploy to Cloudflare Workers
   - Or for API-based queries only

---

## 🚀 **Quick Fix RIGHT NOW:**

```bash
# 1. Go to https://neon.tech
# 2. Create free project
# 3. Copy connection string
# 4. In Render → Environment:
DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require

# 5. Manual Deploy
# 6. Site works! ✅
```

---

**Answer:** YES, you CAN use D1 with Render via API, but Neon PostgreSQL is easier and better for Django! 

Would you like me to:
1. **Set up D1 API client** (advanced, raw SQL)
2. **Use Neon instead** (recommended, 3 minutes)
3. **Deploy to Cloudflare Workers** (full D1 integration)

Let me know! 🚀
