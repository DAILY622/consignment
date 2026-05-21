#!/usr/bin/env python3
"""
Fix Template Encoding Issues - DailyFX Delivery
Fixes:
1. Remove BOM (Byte Order Mark) from templates
2. Replace broken emoji with proper HTML entities
3. Fix Tawk.to widget loading
"""

import os
import re

# Define base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Emoji replacements (broken → correct)
EMOJI_MAP = {
    '≡ñ': '📍',
    '≡Ü': '🚚',
    '≡Ñ': '🏁',
    '≡à': '📅',
    '≡ª': '📦',
    '≡ì': '📍',
    '≡ƒù║∩╕Å': '🗺️',
    '≡ƒ¢∩╕Å': '🛣️',
    '≡Å': '📏',
    '≡è': '📊',
    '≡ï': '📜',
    '≡¡': '📭',
    '≡╖': '📝',
    '≡╝': '💼',
    '≡¢': '✓',
    '≡▒': '📱',
    '≡┐': '🌿',
    '≡₧': '📞',
    '≡░': '💰',
}

def remove_bom(text):
    """Remove BOM from text"""
    if text.startswith('\ufeff'):
        text = text[1:]
    if text.startswith('﻿﻿'):
        text = text.replace('﻿﻿', '')
    if text.startswith('﻿'):
        text = text.replace('﻿', '')
    return text

def fix_emoji(text):
    """Replace broken emoji with correct ones"""
    for broken, correct in EMOJI_MAP.items():
        text = text.replace(broken, correct)
    return text

def fix_tawk_to(text):
    """Reduce Tawk.to loading delay"""
    # Find and replace the 2000ms delay with 500ms
    text = re.sub(
        r"}, 2000\); // Delay by 2 seconds after page load",
        "}, 500); // Delay by 0.5 seconds after page load",
        text
    )
    return text

def fix_template_file(filepath):
    """Fix a single template file"""
    print(f"Processing: {filepath}")
    
    try:
        # Read file with UTF-8 encoding
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        original_length = len(content)
        
        # Apply fixes
        content = remove_bom(content)
        content = fix_emoji(content)
        
        if 'base.html' in filepath:
            content = fix_tawk_to(content)
        
        # Write back without BOM
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        
        print(f"  ✅ Fixed ({original_length} → {len(content)} bytes)")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("=" * 70)
    print("TEMPLATE ENCODING FIX SCRIPT")
    print("=" * 70)
    print()
    
    fixed_count = 0
    error_count = 0
    
    # Process all HTML files in templates directory
    for root, dirs, files in os.walk(TEMPLATES_DIR):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if fix_template_file(filepath):
                    fixed_count += 1
                else:
                    error_count += 1
    
    print()
    print("=" * 70)
    print(f"✅ Fixed: {fixed_count} files")
    print(f"❌ Errors: {error_count} files")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Test locally: python manage.py runserver")
    print("2. Commit changes: git add templates/ && git commit -m 'Fix template encoding'")
    print("3. Push to GitHub: git push")
    print("4. Render will auto-deploy")

if __name__ == '__main__':
    main()
