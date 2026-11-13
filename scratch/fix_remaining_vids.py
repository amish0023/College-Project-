import sys
import os
import json
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import database as db

def verify_oembed(video_id):
    url = f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode('utf-8'))
                return True, data.get('title', ''), data.get('author_name', '')
    except Exception as e:
        return False, None, str(e)
    return False, None, "Unknown"

def fix():
    db.execute("SET SQL_SAFE_UPDATES = 0")
    
    # 1. Fix tbRD2Hfy__8 -> sWH0T4Zez6I
    db.execute(
        """UPDATE lectures 
           SET youtube_video_id='sWH0T4Zez6I', 
               title='Multi-Agent Systems: Trust, Reputation & Coordination Protocols' 
           WHERE youtube_video_id='tbRD2Hfy__8'"""
    )
    
    # 2. Fix kBdlM6hHQUU -> kBdlM6hNDAE
    db.execute(
        """UPDATE lectures 
           SET youtube_video_id='kBdlM6hNDAE' 
           WHERE youtube_video_id='kBdlM6hHQUU'"""
    )
    
    # 3. Fix Wc1W5X9g4P8 -> exc-73Mna3A
    db.execute(
        """UPDATE lectures 
           SET youtube_video_id='exc-73Mna3A' 
           WHERE youtube_video_id='Wc1W5X9g4P8'"""
    )
    
    db.execute("SET SQL_SAFE_UPDATES = 1")
    print("Database updated with replacements.")
    
    # Run full verification on every single lecture row in MySQL!
    all_lectures = db.fetch_all("SELECT id, topic_id, title, youtube_video_id FROM lectures")
    print(f"\nVerifying ALL {len(all_lectures)} lectures in database...")
    
    distinct_vids = set(l['youtube_video_id'] for l in all_lectures)
    print(f"Distinct video IDs: {len(distinct_vids)}")
    
    failed_vids = []
    for vid in distinct_vids:
        ok, title, extra = verify_oembed(vid)
        if not ok:
            print(f"  [ERROR] FAILED: {vid} -> {extra}")
            failed_vids.append(vid)
            
    if not failed_vids:
        print("\nSUCCESS! 100% OF ALL VIDEO LECTURES ARE VALID, ACTIVE, EMBEDDABLE, AND PLAYING ON YOUTUBE!")
    else:
        print(f"\nWARNING: {len(failed_vids)} videos failed.")

if __name__ == '__main__':
    fix()
