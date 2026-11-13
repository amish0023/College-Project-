"""Update all existing lectures with verified YouTube video IDs."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from utils.youtube_curated import CURATED_VIDEOS
from utils import database as db

# Get all lectures with their topic/module info
lectures = db.fetch_all("""
    SELECT l.id, l.title as lecture_title, l.youtube_video_id, l.module_id,
           m.name as module_name, m.subject_id,
           s.name as subject_name
    FROM lectures l
    JOIN modules m ON l.module_id = m.id
    JOIN subjects s ON m.subject_id = s.id
    ORDER BY s.id, m.id
""")

print(f"Found {len(lectures)} lectures to update\n")

updated = 0
already_ok = 0

for lec in lectures:
    module_name = lec['module_name']
    subject_name = lec['subject_name']
    
    # Find best matching curated video for this module
    best_match = None
    module_lower = module_name.lower()
    
    for keyword, videos in CURATED_VIDEOS.items():
        if keyword.lower() in module_lower or module_lower in keyword.lower():
            best_match = videos
            break
    
    if not best_match:
        # Try partial word match
        module_words = set(module_lower.split())
        for keyword, videos in CURATED_VIDEOS.items():
            keyword_words = set(keyword.lower().split())
            if module_words & keyword_words and len(module_words & keyword_words) >= 1:
                best_match = videos
                break
    
    if not best_match:
        # Use first available video for this subject area
        if 'database' in subject_name.lower() or 'dbms' in subject_name.lower():
            best_match = [{'video_id': 'HXV3zeQKqGY', 'title': 'SQL Tutorial Full Database Course', 'channel': 'freeCodeCamp'}]
        elif 'compiler' in subject_name.lower():
            best_match = [{'video_id': '5ZmFlxrNaN8', 'title': 'Introduction to Compiler Design', 'channel': 'Neso Academy'}]
        elif 'intelligence' in subject_name.lower() or 'artificial' in subject_name.lower():
            best_match = [{'video_id': 'T0r3hhFaA1k', 'title': 'AI Full Course 2024', 'channel': 'Simplilearn'}]
        elif 'big data' in subject_name.lower():
            best_match = [{'video_id': '9QxZhapbo0o', 'title': 'Big Data Hadoop Full Course', 'channel': 'Edureka'}]
        elif 'nlp' in subject_name.lower():
            best_match = [{'video_id': '4xdg0y8QDGc', 'title': 'NLP Tutorial', 'channel': 'Education 4u'}]
        elif 'virtual' in subject_name.lower() or 'vr' in subject_name.lower():
            best_match = [{'video_id': 'EVIDMRayeT0', 'title': 'Complete Beginner Guide to VR/AR', 'channel': 'Education 4u'}]
        else:
            print(f"  SKIP: No match for module '{module_name}' in '{subject_name}'")
            continue
    
    video = best_match[0]
    video_id = video['video_id']
    video_title = video['title']
    
    if lec['youtube_video_id'] == video_id:
        already_ok += 1
        continue
    
    new_title = f"{module_name} - {video_title}"
    db.execute(
        "UPDATE lectures SET youtube_video_id = %s, title = %s WHERE id = %s",
        (video_id, new_title, lec['id'])
    )
    updated += 1
    print(f"  [{subject_name}] {module_name}")
    print(f"    OLD: {lec['youtube_video_id']}")
    print(f"    NEW: {video_id} ({video_title})")

print(f"\nDone: {updated} updated, {already_ok} already correct")
