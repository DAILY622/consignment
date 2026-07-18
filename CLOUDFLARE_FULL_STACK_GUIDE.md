# ======================================
# CLOUDFLARE FULL STACK - SETUP GUIDE
# ======================================
# R2 + D1 + Queues + Durable Objects + KV + Analytics

## ✅ RESOURCES CREATED

**D1 Database:**
- Name: consignment-delivery-db
- ID: f1f78eb9-e992-42cf-a30e-9b74970babe1
- Region: Western Europe (WEUR)

**Queue:**
- Name: delivery-notifications
- ✅ Created

**KV Namespace:**
- Binding: CACHE
- ID: d4e27370e54a4fa9850c3a8bcf667b0a
- ✅ Created

**R2 Bucket:**
- Name: mysite (reused from existing)
- Binding: MEDIA

**Durable Objects:**
- PackageTracker: Real-time package updates
- DeliveryRoom: WebSocket broadcasting

**Analytics:**
- Binding: ANALYTICS
- Auto-enabled


## 📦 INSTALLATION

```powershell
# Install Node.js dependencies
npm install --save-dev @cloudflare/workers-types typescript esbuild wrangler

# Or if you prefer package-full.json
Move-Item package-full.json package.json
npm install
```


## 🗄️ DATABASE MIGRATION

Apply schema to D1 production database:

```powershell
# Apply each table individually (D1 doesn't support transactions)
wrangler d1 execute consignment-delivery-db --file=d1-schema.sql --config=wrangler-full.toml
```

Or manually via dashboard:
1. Visit https://dash.cloudflare.com
2. Navigate to Workers & Pages → D1
3. Click on `consignment-delivery-db`
4. Paste and execute `d1-schema.sql` contents


## 🚀 DEPLOYMENT

```powershell
# Deploy to Cloudflare Workers
wrangler deploy --config wrangler-full.toml
```

Your worker will be deployed to: `https://consignment-delivery.YOURACCOUNT.workers.dev`


## 🧪 TESTING

### Track a package:
```bash
curl https://consignment-delivery.YOURACCOUNT.workers.dev/api/track/DFX-2XWJFI8R
```

### Upload photo:
```bash
curl -X POST https://consignment-delivery.YOURACCOUNT.workers.dev/api/upload \
  -F "photo=@delivery.jpg" \
  -F "tracking_number=DFX-2XWJFI8R"
```

### WebSocket (real-time tracking):
```javascript
const ws = new WebSocket('wss://consignment-delivery.YOURACCOUNT.workers.dev/ws/track?tracking=DFX-2XWJFI8R');
ws.onmessage = (event) => console.log(event.data);
```


## 📊 MONITORING

```powershell
# View real-time logs
wrangler tail --config wrangler-full.toml

# View analytics
# Visit: https://dash.cloudflare.com → Workers & Pages → consignment-delivery → Analytics
```


## 🔑 ENVIRONMENT VARIABLES

Set secrets via CLI:

```powershell
# Django secret key (if needed)
wrangler secret put SECRET_KEY --config wrangler-full.toml

# R2 credentials (if accessing from Django)
wrangler secret put R2_ACCESS_KEY_ID --config wrangler-full.toml
wrangler secret put R2_SECRET_ACCESS_KEY --config wrangler-full.toml
```


## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                   CLOUDFLARE WORKERS                        │
│                 (TypeScript: src/index.ts)                  │
└─────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
   ┌────────┐          ┌─────────┐         ┌──────────┐
   │   D1   │          │    R2   │         │  Queues  │
   │Database│          │ Storage │         │ Messages │
   └────────┘          └─────────┘         └──────────┘
        │                    │                    │
        │              Photo Upload          Notifications
        │                    │                    │
        ▼                    ▼                    ▼
   Track Package      delivery_photos/     Email/SMS/Push
   Status Updates      signatures/         Background Jobs
                       
                                         
   ┌─────────────────────────────────────────────────────┐
   │              DURABLE OBJECTS                        │
   │  ┌─────────────────┐    ┌──────────────────┐       │
   │  │ PackageTracker  │    │  DeliveryRoom    │       │
   │  │  (Stateful)     │    │   (WebSocket)    │       │
   │  └─────────────────┘    └──────────────────┘       │
   └─────────────────────────────────────────────────────┘
           Real-time GPS            Live Tracking
           State Management         Broadcasting


   ┌──────────┐
   │    KV    │  → Fast cache for tracking lookups (5 min TTL)
   └──────────┘

   ┌────────────┐
   │ Analytics  │  → Track API usage and popular routes
   └────────────┘
```


## 🎯 FEATURES ENABLED

✅ **API Endpoints:**
- `GET /api/track/{tracking_number}` - Get package details + history
- `POST /api/upload` - Upload delivery photo to R2

✅ **Real-time:**
- `WS /ws/track?tracking=XXX` - Live package updates via WebSocket

✅ **Background Jobs:**
- Queue-based notifications
- Async email/SMS sending

✅ **Storage:**
- R2 for delivery photos and signatures
- D1 for package/tracking data
- KV for caching frequently accessed packages

✅ **Stateful:**
- Durable Objects for real-time GPS tracking
- Per-package state management


## 📱 FRONTEND INTEGRATION

Replace Django API calls with Cloudflare Workers:

**Before (Django):**
```javascript
fetch('/packages/track/DFX-2XWJFI8R/')
```

**After (Workers):**
```javascript
fetch('https://consignment-delivery.YOURACCOUNT.workers.dev/api/track/DFX-2XWJFI8R')
```

**WebSocket (NEW):**
```javascript
const ws = new WebSocket('wss://consignment-delivery.YOURACCOUNT.workers.dev/ws/track?tracking=DFX-2XWJFI8R');
ws.onmessage = (e) => {
  const update = JSON.parse(e.data);
  updateMap(update.lat, update.lon);
};
```


## 💰 PRICING

All within FREE tier for moderate traffic:

- **D1:** 5 GB storage, 5M reads/day, 100K writes/day
- **R2:** 10 GB storage, unlimited egress (FREE)
- **Queues:** 1M operations/month
- **Durable Objects:** 1M requests/month
- **KV:** 100K reads/day, 1K writes/day
- **Workers:** 100K requests/day


## 🔄 SYNCING WITH DJANGO

**Option 1: Workers-only API (Recommended)**
- Keep Django for admin panel only
- All public APIs via Cloudflare Workers
- Faster, globally distributed

**Option 2: Hybrid**
- Workers for real-time features (WebSocket, uploads)
- Django for complex business logic
- Sync data via Queue


## 📚 NEXT STEPS

1. ✅ Deploy worker: `wrangler deploy --config wrangler-full.toml`
2. ✅ Migrate D1 database (apply d1-schema.sql)
3. ✅ Test API endpoints
4. ✅ Seed demo package data to D1
5. Update frontend to use Workers API
6. Set up custom domain (optional)
7. Configure email/SMS providers for queue notifications


## 🐛 TROUBLESHOOTING

**Error: "Durable Object not found"**
→ First deploy creates bindings, redeploy to activate Durable Objects

**Error: "Queue not found"**
→ Check queue name matches wrangler-full.toml binding

**WebSocket not connecting:**
→ Use `wss://` protocol, not `ws://`

**R2 upload fails:**
→ Check R2 bucket name and permissions


## 📞 SUPPORT

- Cloudflare Dashboard: https://dash.cloudflare.com
- Workers Docs: https://developers.cloudflare.com/workers/
- D1 Docs: https://developers.cloudflare.com/d1/
- R2 Docs: https://developers.cloudflare.com/r2/
