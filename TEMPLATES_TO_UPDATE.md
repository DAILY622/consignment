# 🚨 TEMPLATES TO UPDATE AFTER DOWNLOADING IMAGES

**Status:** Placeholder images deleted, these templates have broken image references  
**Action Required:** Download real photos then update these files

---

## 📄 **FILES THAT REFERENCE DELETED PLACEHOLDERS**

### **1. services.html** (2 references)
**Location:** `templates/services.html`
**References:** Local placeholder images (photo-*.svg)
**Fix:** Replace with downloaded service images

### **2. careers.html** (4 references)
**Location:** `templates/careers.html`
**References:** Local placeholder images (photo-*.svg)  
**Fix:** Replace with career/team images

### **3. fleet.html** (8 references)
**Location:** `templates/fleet.html`
**References:** Local placeholder images (photo-*.svg)
**Fix:** Replace with fleet vehicle images

### **4. about.html** (3 references)
**Location:** `templates/about.html`
**References:** Local placeholder images (photo-*.svg)
**Fix:** Replace with team/company images

---

## ✅ **TEMPLATES THAT USE EXTERNAL IMAGES (ALREADY OK)**

### **1. home.html** (34 references)
**Status:** ✅ Using images.unsplash.com URLs
**Action:** None needed - already using real Unsplash photos
**Note:** Images load from external CDN (fast & reliable)

---

## 🔧 **TEMPLATE UPDATE PATTERNS**

### **Current (Broken):**
```html
<img src="{% static 'images/photo-1234567890-w600.svg' %}" alt="...">
```

### **After Downloading (Fixed):**
```html
<img src="{% static 'images/feature-tracking.jpg' %}" alt="Real-time tracking">
```

---

## 📋 **UPDATE CHECKLIST**

After downloading real images to `static/images/`:

- [ ] Update `services.html` - Replace 2 image references
- [ ] Update `careers.html` - Replace 4 image references
- [ ] Update `fleet.html` - Replace 8 image references
- [ ] Update `about.html` - Replace 3 image references
- [ ] Test locally (python manage.py runserver)
- [ ] Verify all images load correctly
- [ ] Commit changes to Git
- [ ] Push to GitHub
- [ ] Deploy to Render

---

## 💡 **WHAT TO DO NOW**

**Option 1: Download images first (Recommended)**
1. Follow IMAGE_REPLACEMENT_GUIDE.md
2. Download all 21 images to `static/images/`
3. Notify me when ready
4. I'll update all 4 template files with correct image paths

**Option 2: Use external Unsplash URLs (Quick fix)**
1. I can update templates to use direct Unsplash URLs (like home.html)
2. No downloads needed
3. Images load from external CDN
4. Downside: Relies on external service

**Option 3: Use icon placeholders temporarily**
1. Replace images with simple icon-based placeholders
2. No broken images during development
3. Replace with real photos later

---

**Which option do you prefer?**
