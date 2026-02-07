import os
import re

ROOT_DIR = r"d:\Certified CyberDefender (CCD) Blue Team Training 2025"
INPUT_FILE = os.path.join(ROOT_DIR, "all_files.txt")

# Navigation bar template
NAV_BAR_TEMPLATE = """
<!-- Navigation Bar Injected -->
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; gap: 10px; font-family: Segoe UI, sans-serif; font-weight: bold;">
    {prev_btn}
    <a href="{dash_link}" style="background-color: #3b82f6; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border: 2px solid #1e293b; display: flex; align-items: center;">
        Dashboard
    </a>
    {next_btn}
</div>
"""

BTN_TEMPLATE = """
    <a href="{link}" style="background-color: #3b82f6; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border: 2px solid #1e293b; display: flex; align-items: center;">
        {label}
    </a>
"""

DISABLED_BTN_TEMPLATE = """
    <span style="background-color: #64748b; color: #cbd5e1; padding: 10px 20px; border-radius: 5px; cursor: not-allowed; box-shadow: none; border: 2px solid #475569; display: flex; align-items: center;">
        {label}
    </span>
"""

def natural_sort_key(s):
    # Splits string into a list of integers and other text
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def inject_links():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8-sig") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print(f"Error reading list: {e}")
        return

    # Sort files naturally
    lines.sort(key=natural_sort_key)
    
    total_files = len(lines)
    count = 0
    
    for i, file_path in enumerate(lines):
        try:
            # Calculate relative path to main.html
            try:
                rel_from_root = os.path.relpath(file_path, ROOT_DIR)
            except ValueError:
                continue

            depth = len(rel_from_root.split(os.sep)) - 1
            if depth < 0: depth = 0
            
            # Paths construction
            dash_path = "../" * depth + "main.html"
            
            # Prev Link
            if i > 0:
                prev_file = lines[i-1]
                try:
                    rel_prev = os.path.relpath(prev_file, os.path.dirname(file_path))
                    # Replace backslash with smile slash for web url
                    rel_prev = rel_prev.replace(os.sep, "/")
                    prev_btn = BTN_TEMPLATE.format(link=rel_prev, label="&larr; Prev")
                except ValueError:
                    prev_btn = DISABLED_BTN_TEMPLATE.format(label="&larr; Prev")
            else:
                prev_btn = DISABLED_BTN_TEMPLATE.format(label="&larr; Prev")
                
            # Next Link
            if i < total_files - 1:
                next_file = lines[i+1]
                try:
                    rel_next = os.path.relpath(next_file, os.path.dirname(file_path))
                    rel_next = rel_next.replace(os.sep, "/")
                    next_btn = BTN_TEMPLATE.format(link=rel_next, label="Next &rarr;")
                except ValueError:
                    next_btn = DISABLED_BTN_TEMPLATE.format(label="Next &rarr;")
            else:
                next_btn = DISABLED_BTN_TEMPLATE.format(label="Next &rarr;")

            # Read file
            content = None
            encoding_used = "utf-8"
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                encoding_used = "latin-1"
                with open(file_path, "r", encoding="latin-1") as f:
                    content = f.read()
            
            # Remove old injection if exists
            # We look for "<!-- Dashboard Link Injected -->" and the following <a> tag
            # Or "<!-- Navigation Bar Injected -->"
            
            # Simple regex to remove old dashboard link
            content = re.sub(r'<!-- Dashboard Link Injected -->\s*<a[^>]+>.*?</a>', '', content, flags=re.DOTALL)
            
            # Simple regex to remove old nav bar if we run this script multiple times
            content = re.sub(r'<!-- Navigation Bar Injected -->\s*<div[^>]+>.*?</div>', '', content, flags=re.DOTALL)

            # Construct new injection
            nav_bar = NAV_BAR_TEMPLATE.format(prev_btn=prev_btn, dash_link=dash_path, next_btn=next_btn)
            
            if "</body>" in content:
                new_content = content.replace("</body>", nav_bar + "\n</body>")
            else:
                new_content = content + nav_bar
                
            with open(file_path, "w", encoding=encoding_used) as f:
                f.write(new_content)
                
            count += 1
            if count % 50 == 0:
                print(f"Processed {count}/{total_files} files...")
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"Finished. Updated {count} files.")

if __name__ == "__main__":
    inject_links()
