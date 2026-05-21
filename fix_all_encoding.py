#!/usr/bin/env python3
"""
COMPREHENSIVE Template Encoding Fix - DailyFX Delivery
Fixes ALL encoding issues including currency symbols, checkmarks, and special characters
"""

import os
import re
import codecs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Comprehensive character map
CHAR_MAP = {
    # Emoji fixes
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
    '≡▒': '📱',
    '≡┐': '🌿',
    '≡₧': '📞',
    '≡░': '💰',
    
    # Checkmark fixes
    'Γ£ô': '✓',
    'Γ£à': '✓',
    '✓': '✓',  # Ensure proper checkmark
    
    # Currency and special symbols
    '£': '£',
    '©': '©',
    '┬': '£',  # Another pound variant
    '€': '€',
    
    # Other problematic characters
    '╝∩╕Å': '',
    '╝': '▼',
    'Γëê': '≈',
    'ΓÅ▒∩╕Å': '⏱️',
    'Γ¢╢': '▼',
    '≡ƒƒó': '🚚',
    '≡ƒÄ»': '📏',
}

def remove_bom(text):
    """Remove all BOM variants"""
    # Remove UTF-8 BOM
    if text.startswith('\ufeff'):
        text = text[1:]
    if text.startswith(codecs.BOM_UTF8.decode('utf-8')):
        text = text[len(codecs.BOM_UTF8.decode('utf-8')):]
    # Remove visible BOM artifacts
    text = text.replace('﻿', '')
    return text

def fix_characters(text):
    """Replace all broken characters"""
    for broken, correct in CHAR_MAP.items():
        text = text.replace(broken, correct)
    return text

def fix_template_file(filepath):
    """Fix a single template file"""
    filename = os.path.basename(filepath)
    print(f"Processing: {filename}")
    
    try:
        # Read with UTF-8 BOM handling
        with open(filepath, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
        
        original_len = len(content)
        
        # Apply all fixes
        content = remove_bom(content)
        content = fix_characters(content)
        
        # Write back as clean UTF-8
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        
        changes = original_len - len(content)
        if changes != 0:
            print(f"  ✅ Fixed - {changes} bytes changed")
        else:
            print(f"  ✓  No changes needed")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("=" * 70)
    print("COMPREHENSIVE TEMPLATE ENCODING FIX")
    print("=" * 70)
    print()
    
    fixed = 0
    errors = 0
    
    for root, dirs, files in os.walk(TEMPLATES_DIR):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if fix_template_file(filepath):
                    fixed += 1
                else:
                    errors += 1
    
    print()
    print("=" * 70)
    print(f"✅ Processed: {fixed} files")
    print(f"❌ Errors: {errors} files")
    print("=" * 70)
    print()
    print("✅ All encoding issues should now be fixed!")
    print("Next: Commit and push to trigger Render deployment")

if __name__ == '__main__':
    main()
