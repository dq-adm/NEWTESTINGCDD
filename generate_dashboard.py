import os
import urllib.parse

# Configuration
ROOT_DIR = r"d:\Certified CyberDefender (CCD) Blue Team Training 2025"
INPUT_FILE = os.path.join(ROOT_DIR, "all_files.txt")
OUTPUT_FILE = os.path.join(ROOT_DIR, "main.html")

def generate_dashboard():
    files_by_module = {}
    
    try:
        with open(INPUT_FILE, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # sort lines to ensure order
    lines.sort()

    for line in lines:
        path = line.strip()
        if not path:
            continue
            
        # Get relative path from root
        try:
            rel_path = os.path.relpath(path, ROOT_DIR)
        except ValueError:
            continue # Should not happen if paths are correct

        # Extract module (first directory)
        parts = rel_path.split(os.sep)
        if len(parts) > 1:
            module = parts[0]
            # Skip if it's a file in root (unless we want to handle them, but structure suggests folders)
            if os.path.isfile(os.path.join(ROOT_DIR, module)):
                 module = "General"
        else:
            module = "General"

        if module not in files_by_module:
            files_by_module[module] = []
        
        files_by_module[module].append(rel_path)

    # Start HTML generation
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Dashboard - Certified CyberDefender</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --sidebar-bg: #1e293b;
            --text-color: #e2e8f0;
            --accent-color: #3b82f6;
            --hover-color: #334155;
            --card-bg: #1e293b;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            display: flex;
            min-height: 100vh;
        }
        .sidebar {
            width: 300px;
            background-color: var(--sidebar-bg);
            padding: 20px;
            overflow-y: auto;
            position: fixed;
            height: 100vh;
            border-right: 1px solid #334155;
        }
        .main-content {
            margin-left: 300px;
            padding: 40px;
            flex-grow: 1;
            max-width: 1200px;
        }
        h1, h2 {
            color: #fff;
        }
        .module-section {
            margin-bottom: 40px;
            background: var(--card-bg);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #334155;
        }
        .module-title {
            font-size: 1.5rem;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--accent-color);
            color: var(--accent-color);
        }
        .lecture-list {
            list-style: none;
            padding: 0;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 10px;
        }
        .lecture-item a {
            display: block;
            padding: 12px 15px;
            background-color: #2b384d;
            color: var(--text-color);
            text-decoration: none;
            border-radius: 6px;
            transition: all 0.2s;
            border: 1px solid transparent;
        }
        .lecture-item a:hover {
            background-color: var(--hover-color);
            border-color: var(--accent-color);
            transform: translateX(5px);
        }
        .sidebar-link {
            display: block;
            padding: 10px;
            color: #94a3b8;
            text-decoration: none;
            margin-bottom: 5px;
            border-radius: 6px;
        }
        .sidebar-link:hover {
            background-color: #334155;
            color: #fff;
        }
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-color);
        }
        ::-webkit-scrollbar-thumb {
            background: #475569;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <nav class="sidebar">
        <h2>Modules</h2>
"""
    # Sidebar links
    for module in sorted(files_by_module.keys()):
        safe_module_id = "".join(x for x in module if x.isalnum())
        html_content += f'<a href="#{safe_module_id}" class="sidebar-link">{module}</a>\n'

    html_content += """
    </nav>
    <div class="main-content">
        <h1>Course Dashboard</h1>
"""

    # Main content modules
    for module in sorted(files_by_module.keys()):
        safe_module_id = "".join(x for x in module if x.isalnum())
        html_content += f'<div id="{safe_module_id}" class="module-section">\n'
        html_content += f'<h2 class="module-title">{module}</h2>\n'
        html_content += '<ul class="lecture-list">\n'
        
        # Sort files naturally if possible, currently simple string sort
        # Ensure files are sorted
        files = sorted(files_by_module[module])
        
        for rel_path in files:
            filename = os.path.basename(rel_path)
            # Make path URL safe
            # On windows, separator is backslash, replace with slash for URL
            url_path = rel_path.replace(os.sep, '/')
            url_path = urllib.parse.quote(url_path)
            
            # Decent display name
            display_name = filename.replace(" hide01.ir.html", "").replace(".html", "")
            
            html_content += f'<li class="lecture-item"><a href="{url_path}" target="_blank">{display_name}</a></li>\n'
            
        html_content += '</ul>\n</div>\n'

    html_content += """
    </div>
</body>
</html>
"""

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Successfully generated {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error writing HTML: {e}")

if __name__ == "__main__":
    generate_dashboard()
