import urllib.request
import urllib.parse
import re
import json

def find_youtube_video(query):
    encoded = urllib.parse.quote(query)
    url = f'https://www.youtube.com/results?search_query={encoded}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching YouTube search for {query}: {e}")
        return None, None
    
    # Extract video IDs
    vids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
    print(f"Found {len(vids)} candidate video IDs for query: '{query}'")
    
    # Test candidates with oEmbed to ensure they are real and embeddable!
    seen = set()
    for vid in vids:
        if vid in seen:
            continue
        seen.add(vid)
        oembed_url = f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json'
        try:
            oreq = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(oreq, timeout=5) as oresp:
                data = json.loads(oresp.read().decode('utf-8'))
                print(f"  [SUCCESS] {vid} -> '{data.get('title')}' by {data.get('author_name')}")
                return vid, data.get('title')
        except Exception:
            continue
    return None, None

if __name__ == '__main__':
    v1, t1 = find_youtube_video('Gate Smashers Definition and Future of Artificial Intelligence')
    v2, t2 = find_youtube_video('Gate Smashers Phases of a compiler')
    v3, t3 = find_youtube_video('Edureka HDFS architecture Hadoop')
