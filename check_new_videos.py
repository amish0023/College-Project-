"""Verify candidate YouTube video IDs for availability."""
import urllib.request
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

# All candidate video IDs from web search results
candidates = {
    # DBMS
    'c5HAwKX-suM': 'Learn DBMS from Scratch',
    '6Iu45VZGQDk': 'Intro to DBMS',
    'scxc0FXp2rg': 'Complete DBMS one shot',
    'YRnjGeQbsHQ': 'Complete DBMS KnowledgeGate',
    'NdeeSEknp58': 'Relational DBMS Course',
    'E--yzX05_k8': 'Gate Smashers Indexing DBMS',
    'bFypv6cQTj0': 'DBMS Indexing Hashing',
    'GFQaEYEc8_8': 'DBMS Normalization 1NF-5NF',
    'IBEuwmYsMKI': 'Normalization normal forms examples',
    'Fb9jZsCETVA': 'Normalization SQL Edureka',
    'uUNJKhT5tmU': 'Normalization in DBMS Explained',
    'Vg5Gvl3Gd1c': 'Deadlocks in DBMS',
    'dD16tN1sGDc': 'Learn Deadlock in DBMS',
    'CbG8WHmAv1M': 'Transactions Concurrency Control',
    'sqSwZKkcURo': 'Views Stored Procedures Triggers',
    'ISb3RGKLOGU': 'Master SQL Stored Procedures Triggers',
    'M-55BmjOuXY': 'Advanced SQL Tutorial',
    'QMUZ5HfWMRc': 'Triggers Events MySQL',
    '7vnxpcqmqNQ': 'Stored Procedures MySQL',
    'uQ5wHypsTDs': 'DBMS Normal Forms SQL',
    'va-QO-dhilI': 'Normalization DBMS Simplified',
    # Compiler Design
    '5ZmFlxrNaN8': 'Intro to Compiler Design Neso',
    'TApMNhQPaCM': 'Different Phases of Compiler Neso',
    '4nx8LEGy9kI': 'Lexical Analyzer Neso',
    'izGDMglQzgY': 'Lexical Analyzer Solved Problems',
    'kRGhDdybd-Y': 'Lexical Analysis Parsing Automata',
    'sigUuLtK058': 'Lexical Analysis Compiler Ch2',
    'fmd-tDDPonY': 'Bottom Up Parser Shift Reduce',
    '1HcZGBLBtcs': 'Shift Reduce Parser Neso',
    '4HbQZ-E7f6g': 'Bottom Up Parser Huddar',
    '0i8q9Gubu6Q': 'Semantic Analysis Neso',
    'SaKfQX_tQrs': 'Runtime Environment Code Optimization Neso',
    'SiYxGP0O68s': 'Intermediate Code Generation Neso',
    'OIKL6wFjFOo': 'Intro to Parsers Neso',
    # AI
    'T0r3hhFaA1k': 'All in One AI Full Course 2024',
    'MqffbpjhriQ': 'AI Full Course Beginners',
    'THtGV_9lc68': 'AI Tutorial 10 Hours Edureka',
    'zkubwWb3m4Q': 'AI Full Course Simplilearn',
    'l-hh51ncgDI': 'Minimax Alpha Beta Pruning Sebastian',
    'ec5mluJnWM0': 'Alpha Beta Pruning Easy Examples',
    '9D1hVGumxCo': 'Alpha Beta Pruning Example Huddar',
    'zp3VMe0Jpf8': 'Minimax Alpha Beta Pruning',
    '0GPrVTqTX5Q': 'Adversarial Search Alpha Beta',
    # Big Data
    '9QxZhapbo0o': 'Big Data Hadoop Full Course 12hrs Edureka',
    'rTe5fWz_fFk': 'Hadoop MapReduce Tutorial',
    'WRr8lK7JFFI': 'MapReduce Tutorial Edureka',
    'myTA04dRe1k': 'Hadoop 2.0 Architecture YARN',
    'YirUQhskJ3o': 'Hadoop Tutorial Beginners Edureka',
    'nnnloKX5r84': 'Big Data Hadoop Intro',
    'zQrB45UZsvQ': 'Hadoop Ecosystem Hive Pig Sqoop',
    'ZCWiZNBV6-U': 'Apache HBase Tutorial Edureka',
    'tKNGB5IZPFE': 'Hive Tutorial Beginners Edureka',
    'XfXWF2cvLi0': 'What is Apache HBase Edureka',
    'AnGCeuIvO-k': 'Learn Every Core Big Data Tool',
    'prEa4erc6fM': 'Pig Architecture Big Data',
    'k7JMGk3rRDE': 'Linear Regression Analytics',
    # NLP Healthcare
    'oyhpIWa9w1Y': 'Medical NLP Google Cloud',
    'q_Ff3J0-i0c': 'NLP for Healthcare Medical Affairs',
    'OEgyLwjecgU': 'NLP in Healthcare Chun Xiao',
    '4xdg0y8QDGc': 'NLP Intro',
    'B3xB9gaBosw': 'Text Classification NER Spark NLP',
    'hZnnSzOkdgY': 'Text Classification NER Python',
    'bb_0TfZTnjs': 'Common NLP Tasks Transformers',
    'aijeWvQv6lE': 'NLP Python Crash Course',
    'cd51nXNpiiU': 'Sentiment Classification SpaCy',
    'H-gE1zLWjQ8': 'NLP Text Classification Python',
    'MmgjhvOSd-E': 'Named Entity Extraction NLP',
    # VR
    'EVIDMRayeT0': 'Complete Beginner Guide VR/AR',
    '99ZPRFNWIFY': 'VR Headsets How Its Made',
    'B7LwauHpGjE': 'Immersive VR Explained',
    'HBNH8tzsfVM': 'What is VR Mashable',
    'YBQ_ps6e71k': 'Learn VR Development Unity 3hrs',
    'H8dWVlZKQu4': 'Make VR Game 2 Hours',
    'ZbUVzy1DJr4': 'Set Up VR Unreal Engine 5',
    'i3xNb5R_xos': 'First VR Project Unreal Engine 5',
    'oRnvRJqgaGQ': 'Make VR Games Unity Beginner',
    # Already working (keep these)
    'HXV3zeQKqGY': 'SQL Tutorial Full Course freeCodeCamp',
    '8HyCNIVRbSU': 'LSTM GRU Guide',
    'ad79nYk2keg': 'What is AI Simplilearn',
    'aircAruvnKk': 'Neural Network 3Blue1Brown',
    'kCc8FmEb1nY': 'Build GPT Andrej Karpathy',
}

print(f"Checking {len(candidates)} video IDs...")

working = []
broken = []

for i, (vid, title) in enumerate(sorted(candidates.items())):
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        if resp.status == 200:
            data = json.loads(resp.read())
            real_title = data.get('title', title)
            working.append((vid, real_title))
            print(f"[{i+1}/{len(candidates)}] OK   {vid} - {real_title}")
        else:
            broken.append((vid, title))
            print(f"[{i+1}/{len(candidates)}] FAIL {vid} - HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        broken.append((vid, title))
        print(f"[{i+1}/{len(candidates)}] FAIL {vid} - {e.code}")
    except Exception as e:
        broken.append((vid, title))
        print(f"[{i+1}/{len(candidates)}] FAIL {vid} - {e}")
    time.sleep(0.25)

print(f"\n{'='*60}")
print(f"RESULTS: {len(working)} working, {len(broken)} broken")
print(f"{'='*60}")

if broken:
    print(f"\nBROKEN:")
    for vid, title in broken:
        print(f"  FAIL {vid} ({title})")

# Save
with open('new_video_results.json', 'w', encoding='utf-8') as f:
    json.dump({
        'working': [{'id': v, 'title': t} for v, t in working],
        'broken': [{'id': v, 'title': t} for v, t in broken]
    }, f, indent=2)

print(f"\nSaved to new_video_results.json")
