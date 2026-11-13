"""Check all YouTube video IDs for availability."""
import urllib.request
import json
import time
import sys
from utils.youtube_curated import CURATED_VIDEOS

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Extract all unique video IDs
all_ids = set()
for keyword, videos in CURATED_VIDEOS.items():
    for v in videos:
        all_ids.add(v['video_id'])

print(f"Total unique video IDs to check: {len(all_ids)}")

working = []
broken = []

for i, vid in enumerate(sorted(all_ids)):
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        if resp.status == 200:
            data = json.loads(resp.read())
            title = data.get('title', 'Unknown')
            working.append((vid, title))
            print(f"[{i+1}/{len(all_ids)}] OK   {vid} - {title}")
        else:
            broken.append(vid)
            print(f"[{i+1}/{len(all_ids)}] FAIL {vid} - HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        if e.code in (401, 403, 404):
            broken.append(vid)
            print(f"[{i+1}/{len(all_ids)}] FAIL {vid} - NOT FOUND ({e.code})")
        else:
            broken.append(vid)
            print(f"[{i+1}/{len(all_ids)}] FAIL {vid} - HTTP Error {e.code}")
    except Exception as e:
        broken.append(vid)
        print(f"[{i+1}/{len(all_ids)}] FAIL {vid} - Error: {e}")
    time.sleep(0.3)

print(f"\n{'='*60}")
print(f"RESULTS: {len(working)} working, {len(broken)} broken out of {len(all_ids)} total")
print(f"{'='*60}")

if broken:
    print(f"\nBroken video IDs:")
    for vid in broken:
        print(f"  FAIL {vid}")

if working:
    print(f"\nWorking video IDs:")
    for vid, title in working:
        print(f"  OK   {vid} - {title}")

# Save results
with open('video_check_results.json', 'w', encoding='utf-8') as f:
    json.dump({'working': [{'id': v, 'title': t} for v, t in working], 'broken': broken}, f, indent=2)

print(f"\nResults saved to video_check_results.json")
