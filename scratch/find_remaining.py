import urllib.request
import urllib.parse
import re
import json

def find_verified(query):
    encoded = urllib.parse.quote(query)
    url = f'https://www.youtube.com/results?search_query={encoded}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    vids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
    for v in vids:
        oembed_url = f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={v}&format=json'
        try:
            oreq = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(oreq, timeout=5) as oresp:
                if oresp.status == 200:
                    data = json.loads(oresp.read().decode('utf-8'))
                    return v, data.get('title', ''), data.get('author_name', '')
        except Exception:
            continue
    return None, None, None

v_agent, t_agent, a_agent = find_verified('multi agent systems artificial intelligence tutorial')
print(f"Agent Video: {v_agent} | {t_agent} ({a_agent})")

v_vr, t_vr, a_vr = find_verified('VR development tutorial unity beginner Valem')
print(f"VR Video: {v_vr} | {t_vr} ({a_vr})")

v_dbms, t_dbms, a_dbms = find_verified('Gate Smashers Database Management Systems')
print(f"DBMS Video: {v_dbms} | {t_dbms} ({a_dbms})")
