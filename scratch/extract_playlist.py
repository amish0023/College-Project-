import re
import urllib.request
import json

path = r'C:\Users\PC World\.gemini\antigravity\brain\e8886286-11b8-48c7-920b-4d9b0bda8f2f\.system_generated\steps\678\content.md'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

vids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', text)
unique_vids = []
seen = set()
for v in vids:
    if v not in seen:
        seen.add(v)
        unique_vids.append(v)

print(f"Found {len(unique_vids)} unique videos in playlist.")

# Verify each with oEmbed
verified = []
for v in unique_vids[:20]:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={v}&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode())
            print(f"VERIFIED: {v} -> {data.get('title')} ({data.get('author_name')})")
            verified.append({'id': v, 'title': data.get('title'), 'author': data.get('author_name')})
    except Exception as e:
        print(f"FAILED: {v} -> {e}")

print(f"\nTotal verified in batch: {len(verified)}")
