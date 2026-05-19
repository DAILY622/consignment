# Microsoft Edge - Auto Allow All Permissions

## ⚠️ Security Warning
Allowing all permissions by default reduces security. Only do this on:
- Development/testing machines
- Trusted local environments
- Your personal devices for specific purposes

---

## 🔧 Manual Configuration Steps

### Method 1: Edge Settings UI (Recommended)

1. **Open Edge Settings**
   - Open Microsoft Edge
   - Click `⋯` (three dots) → Settings
   - Or press: `Alt + F` → `S`
   - Or type in address bar: `edge://settings/`

2. **Go to Site Permissions**
   - Navigate to: **Cookies and site permissions**
   - Or direct URL: `edge://settings/content`

3. **Configure Each Permission:**

---

### 📍 Location
- Go to: `edge://settings/content/location`
- Toggle: **Ask before accessing (recommended)** → OFF
- Or click "Add" under "Allow" section
- Add: `[*.]localhost:8000` or `[*.]consignment-site-2ac0cae70da0.herokuapp.com`

### 📷 Camera
- Go to: `edge://settings/content/camera`
- Toggle: **Ask before accessing (recommended)** → OFF
- Or add specific sites to "Allow" list

### 🎤 Microphone
- Go to: `edge://settings/content/microphone`
- Toggle: **Ask before accessing (recommended)** → OFF
- Or add specific sites to "Allow" list

### 🌐 Motion and Light Sensors
- Go to: `edge://settings/content/sensors`
- Toggle: **Ask before accessing (recommended)** → OFF

### 🔔 Notifications
- Go to: `edge://settings/content/notifications`
- Toggle: **Ask before sending (recommended)** → OFF
- Or add sites to "Allow" list

### ⚡ JavaScript
- Go to: `edge://settings/content/javascript`
- Ensure: **Allowed (recommended)** is ON
- (Usually enabled by default)

### 🖼️ Images
- Go to: `edge://settings/content/images`
- Ensure: **Show all (recommended)** is selected
- (Usually enabled by default)

### 🪟 Pop-ups and Redirects
- Go to: `edge://settings/content/popups`
- Toggle: **Blocked (recommended)** → OFF (Allow)
- Or add sites to "Allow" list

### 🛡️ Intrusive Ads
- Go to: `edge://settings/content/ads`
- Toggle: **Block ads on sites that show intrusive or misleading ads** → OFF

### 🔄 Background Sync
- Go to: `edge://settings/content/backgroundSync`
- Toggle: **Ask before sending (recommended)** → OFF

### 📥 Automatic Downloads
- Go to: `edge://settings/content/automaticDownloads`
- Toggle: **Ask when a site wants to download multiple files** → OFF

### 🎹 MIDI Device Control
- Go to: `edge://settings/content/midi`
- Toggle: **Ask before accessing (recommended)** → OFF

### 🔌 USB Devices
- Go to: `edge://settings/content/usb`
- Toggle: **Ask before accessing (recommended)** → OFF

---

## 🚀 Quick Access URLs

Copy and paste these into Edge address bar:

```
edge://settings/content/location          # Location
edge://settings/content/camera            # Camera
edge://settings/content/microphone        # Microphone
edge://settings/content/sensors           # Motion sensors
edge://settings/content/notifications     # Notifications
edge://settings/content/javascript        # JavaScript
edge://settings/content/images            # Images
edge://settings/content/popups            # Pop-ups
edge://settings/content/ads               # Ads
edge://settings/content/backgroundSync    # Background sync
edge://settings/content/automaticDownloads # Downloads
edge://settings/content/midi              # MIDI
edge://settings/content/usb               # USB
```

---

## 📋 Method 2: Site-Specific Permissions

For your development site specifically:

1. Visit: `http://localhost:8000`
2. Click the 🔒 lock icon (or ⓘ info icon) in address bar
3. Click: **Permissions for this site**
4. Set each permission to "Allow"

---

## 🎯 For Your Tracking Site Specifically

Add these to allow lists:

**Development**:
- `http://localhost:8000`
- `http://127.0.0.1:8000`

**Production**:
- `https://consignment-site-2ac0cae70da0.herokuapp.com`
- `https://*.onrender.com` (if deploying to Render)

---

## 🔐 Reset to Default (If Needed)

To restore security defaults:

1. Go to: `edge://settings/content`
2. Scroll to bottom
3. Click: **Reset permissions**
4. Or manually toggle each setting back to "Ask before accessing"

---

## ⚡ Developer Mode (Recommended for Dev)

For development work, also enable:

1. Go to: `edge://settings/system`
2. Enable: **Use hardware acceleration when available**

3. Go to: `edge://flags/`
4. Search and enable:
   - `#edge-automatic-https` → Disabled (for localhost)
   - `#block-insecure-private-network-requests` → Disabled (for local dev)

---

## 🛠️ PowerShell Script (Advanced)

**Note**: This modifies registry. Use with caution!

See: `edge_permissions.ps1` for automated configuration.

---

## ✅ Verification

After configuration, test by visiting:
- `http://localhost:8000/track/?q=DFX-2XWJFI8R`

Check that:
- ✓ Map loads without permission prompts
- ✓ Location services work (reverse geocoding)
- ✓ No popup blockers interfere
- ✓ All map features function normally

---

## 📝 Notes

- **Incognito Mode**: Settings don't apply in InPrivate windows
- **Profiles**: Configure for each Edge profile separately
- **Updates**: Settings persist across browser updates
- **Sync**: If Edge sync is on, settings sync across devices

---

## 🔍 Troubleshooting

**Permissions not working?**
1. Clear site data: `edge://settings/siteData`
2. Remove site from "Block" list
3. Restart browser
4. Try site-specific permissions

**Still prompted?**
- Check if site is in "Ask" list (move to "Allow")
- Verify no extensions are blocking
- Check enterprise policies: `edge://policy/`

---

**Status**: ✅ Follow these steps to configure all permissions in Edge!
