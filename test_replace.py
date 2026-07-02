# -*- coding: utf-8 -*-
import os

def check_style_css():
    with open("d:/Kho tri thức/du-toan/style.css", "r", encoding="utf-8") as f:
        content = f.read()
    
    pattern1 = ".form-group input,\n.form-group select {"
    pattern2 = ".form-group input,\r\n.form-group select {"
    
    if pattern1 in content:
        print("style.css: Pattern 1 found (LF)")
    elif pattern2 in content:
        print("style.css: Pattern 2 found (CRLF)")
    else:
        print("style.css: Pattern NOT found")

def check_index_html():
    with open("d:/Kho tri thức/du-toan/index.html", "r", encoding="utf-8") as f:
        content = f.read()
        
    start_str = '⚡ Thiết Bị Điện (nhập số lượng — 0 = bỏ qua)'
    end_str = 'id="elec-note"'
    
    if start_str in content:
        print("index.html: Start string found")
        start_idx = content.find(start_str)
        # find the div before it
        sec_title_idx = content.rfind('<div class="section-title"', 0, start_idx)
        print(f"index.html: Section title starts at {sec_title_idx}")
    else:
        print("index.html: Start string NOT found")
        
    if end_str in content:
        print("index.html: End string found")
        end_idx = content.find(end_str)
        # find the next closing div
        close_div_idx = content.find('</div>', end_idx) + 6
        print(f"index.html: Replacement ends at {close_div_idx}")
    else:
        print("index.html: End string NOT found")

def check_app_js():
    with open("d:/Kho tri thức/du-toan/app.js", "r", encoding="utf-8") as f:
        content = f.read()
        
    targets = [
        "function parseNoteItems(room)",
        "elecLightDl:      parseInt(document.getElementById('elec-light-dl').value)",
        "document.getElementById('elec-light-dl').value           = room?.elecLightDl       ?? 0;",
        "const eLightDl       = +room.elecLightDl       || 0;"
    ]
    
    for t in targets:
        if t in content:
            print(f"app.js: '{t}' found")
        else:
            # Let's try with flexible spacing
            norm_t = " ".join(t.split())
            found = False
            for line in content.splitlines():
                if norm_t in " ".join(line.split()):
                    print(f"app.js: '{t}' found with spacing differences: '{line.strip()}'")
                    found = True
                    break
            if not found:
                print(f"app.js: '{t}' NOT found")

check_style_css()
check_index_html()
check_app_js()
