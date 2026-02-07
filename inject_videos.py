import os
import re
import urllib.parse

ROOT_DIR = r"d:\Certified CyberDefender (CCD) Blue Team Training 2025"

def inject_video_player():
    count = 0
    updated_files = []
    
    print(f"Scanning {ROOT_DIR} for missing video players...")
    
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.lower().endswith(".html") and not file.lower().endswith("main.html"):
                html_path = os.path.join(root, file)
                
                # Logic to find matching video
                # HTML: [Name].html
                # Video: @WickHelps_[Name].mp4
                
                stem = file[:-5] # remove .html suffix
                
                # List of potential video filenames to check
                potential_video_names = [
                    f"@WickHelps_{stem}.mp4",
                    f"@WickHelps_{stem} .mp4",
                    f"{stem}.mp4",
                    f"{stem} [Video].mp4",
                    f"@WickHelps_{stem} [Video].mp4"
                ]
                
                video_file = None
                for v_name in potential_video_names:
                    if v_name in files:
                        video_file = v_name
                        break
                
                # Special fuzzy check case if exact match fails
                # Sometimes filenames differ slightly (e.g. extra spaces)
                if not video_file:
                    # simplistic fuzzy: check if stem is in video filename and it starts with @WickHelps
                    for f in files:
                        if f.endswith(".mp4") and stem in f and "@WickHelps" in f:
                            # Be careful not to match partial stems of other files
                            # e.g. "Topic 1" matching "Topic 10"
                            # This is risky, so maybe stick to strict checking first
                            pass

                if video_file:
                    if inject_into_file(html_path, video_file):
                        count += 1
                        updated_files.append(file)
                        print(f"[UPDATED] {file} -> Linked to {video_file}")
                    else:
                        # print(f"[SKIPPED] {file} (Already has video or read error)")
                        pass
                else:
                    # print(f"[NO VIDEO] {file}")
                    pass
                    
    print(f"\nTotal files updated: {count}")
    return updated_files

def inject_into_file(html_path, video_filename):
    content = None
    encoding = 'utf-8'
    
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            encoding = 'utf-8-sig'
            with open(html_path, "r", encoding="utf-8-sig") as f:
                content = f.read()
        except:
            print(f"ERROR: Could not read {html_path}")
            return False

    if "<video" in content:
        return False

    # Encode video filename for URL
    video_src_encoded = urllib.parse.quote(video_filename)

    player_html = f"""
                                    <!-- Injected Video Player -->
                                    <div class="video-container" style="text-align: center; margin: 0 auto 30px auto;">
                                        <video controls style="width: 100%; max-width: 900px; border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.5); outline: none;">
                                            <source src="{video_src_encoded}" type="video/mp4">
                                            Your browser does not support the video tag.
                                        </video>
                                    </div>
    """
    
    # Injection Logic
    # We look for <div class="fr-view"> which wraps the text content
    target_marker = '<div class="fr-view">'
    
    if target_marker in content:
        # Inject BEFORE the text content starts inside fr-view
        new_content = content.replace(target_marker, target_marker + "\n" + player_html, 1)
    else:
        # Fallback 1: id="content-inner"
        if 'id="content-inner"' in content:
             # Find the closing angle bracket of the section/div tag
             idx = content.find('id="content-inner"')
             end_tag_idx = content.find('>', idx)
             if end_tag_idx != -1:
                 pre = content[:end_tag_idx+1]
                 post = content[end_tag_idx+1:]
                 new_content = pre + "\n" + player_html + post
             else:
                 return False
        # Fallback 2: Top of body
        elif '<body' in content:
             new_content = re.sub(r'(<body[^>]*>)', r'\1' + "\n" + player_html, content, 1)
        else:
            return False

    try:
        with open(html_path, "w", encoding=encoding) as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"ERROR writing to {html_path}: {e}")
        return False

if __name__ == "__main__":
    inject_video_player()
