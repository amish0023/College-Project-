"""
YouTube Video Search & Caching for Personalised Learning.
Uses YouTube Data API v3 to find the best educational videos for each topic.
Falls back to curated search queries if no API key is configured.
"""

import json
import os
import re
import urllib.request
import urllib.parse
from utils import database as db


def query_db(sql, args=(), one=False):
    """Wrapper to match the old query_db interface using the existing db module."""
    if isinstance(args, list):
        args = tuple(args)
    sql_upper = sql.strip().upper()
    if sql_upper.startswith('SELECT') or sql_upper.startswith('SHOW'):
        if one:
            return db.fetch_one(sql, args)
        return db.fetch_all(sql, args)
    else:
        # For INSERT/UPDATE/DELETE, use execute
        return db.execute(sql, args)


# YouTube Data API key - set via environment variable or config
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')

# Curated search prefixes to improve quality
QUALITY_CHANNELS = [
    'freeCodeCamp', 'CS Dojo', 'Jenny\'s Lectures', 'Neso Academy',
    'Knowledge Gate', 'Engineering Digest', 'mycodeschool', 'Abdul Bari',
    'Gate Smashers', 'CodeWithHarry', 'TechWithTim', 'Programming with Mosh',
    'Traversy Media', 'Fireship', 'Academind', 'Simplilearn',
    'Edureka', 'Intellipaat', 'Harvard University', 'MIT OpenCourseWare',
    'Khan Academy', '3Blue1Brown', 'Two Minute Papers', 'sentdex'
]


def extract_video_id(url):
    """Extract YouTube video ID from various URL formats."""
    if not url:
        return None
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def search_youtube(query, max_results=5):
    """
    Search YouTube for educational videos.
    Uses YouTube Data API v3 if API key is available.
    Falls back to curated search if no API key.
    """
    if YOUTUBE_API_KEY:
        return _search_with_api(query, max_results)
    else:
        return _search_curated(query, max_results)


def _search_with_api(query, max_results=5):
    """Search YouTube using the official Data API v3."""
    try:
        # Add educational filter
        search_query = f"{query} tutorial lecture"
        params = {
            'part': 'snippet',
            'q': search_query,
            'type': 'video',
            'videoDuration': 'medium',  # 4-20 minutes
            'videoCategoryId': '27',  # Education
            'maxResults': max_results,
            'order': 'relevance',
            'key': YOUTUBE_API_KEY
        }
        url = f"https://www.googleapis.com/youtube/v3/search?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'PersonalisedLearning/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        videos = []
        for item in data.get('items', []):
            video_id = item['id']['videoId']
            snippet = item['snippet']
            videos.append({
                'video_id': video_id,
                'title': snippet['title'],
                'channel': snippet['channelTitle'],
                'description': snippet.get('description', ''),
                'thumbnail': snippet['thumbnails']['high']['url'] if 'thumbnails' in snippet and 'high' in snippet.get('thumbnails', {}) else '',
                'url': f'https://www.youtube.com/watch?v={video_id}',
                'embed_url': f'https://www.youtube.com/embed/{video_id}'
            })

        # Get view counts for sorting
        if videos:
            video_ids = ','.join([v['video_id'] for v in videos])
            stats_params = {
                'part': 'statistics',
                'id': video_ids,
                'key': YOUTUBE_API_KEY
            }
            stats_url = f"https://www.googleapis.com/youtube/v3/videos?{urllib.parse.urlencode(stats_params)}"
            stats_req = urllib.request.Request(stats_url, headers={'User-Agent': 'PersonalisedLearning/1.0'})
            with urllib.request.urlopen(stats_req, timeout=10) as resp:
                stats_data = json.loads(resp.read().decode())

            stats_map = {}
            for item in stats_data.get('items', []):
                stats_map[item['id']] = {
                    'view_count': int(item['statistics'].get('viewCount', 0)),
                    'like_count': int(item['statistics'].get('likeCount', 0))
                }

            for v in videos:
                s = stats_map.get(v['video_id'], {})
                v['view_count'] = s.get('view_count', 0)
                v['like_count'] = s.get('like_count', 0)

            # Sort by views (most popular first)
            videos.sort(key=lambda x: x.get('view_count', 0), reverse=True)

        return videos

    except Exception as e:
        print(f"YouTube API error: {e}")
        return _search_curated(query, max_results)


def _search_curated(query, max_results=5):
    """
    Curated fallback when no API key is available.
    Uses comprehensive mapping of all 210 syllabus topics to the best YouTube videos.
    """
    from utils.youtube_curated import CURATED_VIDEOS
    curated_videos = CURATED_VIDEOS

    # Also add legacy mappings for backwards compatibility
    legacy_videos = {
        # Arrays
        'arrays': [
            {'video_id': 'nYOw2Sokn0E', 'title': 'Arrays - Data Structures', 'channel': 'mycodeschool'},
            {'video_id': 'RBSGKlLvoWU', 'title': 'Array Data Structure and Algorithms', 'channel': 'Coding Boot Camp'},
            {'video_id': 'aM5dM7RY0cI', 'title': 'Arrays Explained - Computer Science', 'channel': 'CS Dojo'},
        ],
        # Linked Lists
        'linked list': [
            {'video_id': '/goZBmPxso1g', 'title': 'Linked Lists - Data Structures', 'channel': 'mycodeschool'},
            {'video_id': 'WwFbMfykRRU', 'title': 'Linked List Implementation', 'channel': 'Jenny\'s Lectures'},
            {'video_id': 'gn2nuzEgRpc', 'title': 'Linked Lists in 4 Minutes', 'channel': 'Fireship'},
        ],
        # Stacks
        'stack': [
            {'video_id': 'LFBj2B7-JUY', 'title': 'Stack Data Structure', 'channel': 'Jenny\'s Lectures'},
            {'video_id': 'LqDbCQnE4Wk', 'title': 'Stack Explained', 'channel': 'Neso Academy'},
        ],
        # Queues
        'queue': [
            {'video_id': 'FBy9BNa0g4Y', 'title': 'Queue Data Structure', 'channel': 'Jenny\'s Lectures'},
            {'video_id': 'wjI1qxCqzCM', 'title': 'Queue Explained', 'channel': 'Neso Academy'},
        ],
        # Trees
        'tree': [
            {'video_id': 'oSWTXtD7rvY', 'title': 'Binary Trees - Data Structures', 'channel': 'Computer Science'},
            {'video_id': 'YT1_hXKM0Pg', 'title': 'Binary Search Tree Implementation', 'channel': 'Jenny\'s Lectures'},
            {'video_id': 'fAAZixLMEDs', 'title': 'Tree Data Structure Tutorial', 'channel': 'mycodeschool'},
        ],
        # Graphs
        'graph': [
            {'video_id': 'gXgEDyodO1U', 'title': 'Graph Data Structure Tutorial', 'channel': 'Clever Programmer'},
            {'video_id': 'bL-lH5KNoB8', 'title': 'BFS and DFS Graph Algorithms', 'channel': 'NeetCode'},
        ],
        # Sorting
        'sort': [
            {'video_id': 'kPRAkWgH22E', 'title': 'Sorting Algorithms Animated', 'channel': 'Klughari'},
            {'video_id': 'kPRAkWgH22E', 'title': 'Sorting Algorithms Explained', 'channel': 'Abdul Bari'},
            {'video_id': 'Hoixr4d_WC8', 'title': 'Merge Sort Explained', 'channel': 'mycodeschool'},
        ],
        # Searching
        'search': [
            {'video_id': 'f9_KMFHx0W8', 'title': 'Binary Search Algorithm', 'channel': 'Jenny\'s Lectures'},
            {'video_id': 'P3ItUMpkM6w', 'title': 'Linear Search vs Binary Search', 'channel': 'Concept and Coding'},
        ],
        # SQL
        'sql': [
            {'video_id': 'HXV3zeQKqGY', 'title': 'SQL Tutorial - Full Database Course', 'channel': 'freeCodeCamp'},
            {'video_id': '9UJUD3hT0DE', 'title': 'SQL for Beginners - Practice', 'channel': 'Programming with Mosh'},
            {'video_id': '9OdMPFRBRXE', 'title': 'Learn SQL in One Hour', 'channel': 'Simplilearn'},
        ],
        # Normalization
        'normalization': [
            {'video_id': 'UrYLyGkF2bc', 'title': 'Database Normalization Explained', 'channel': 'Gate Smashers'},
            {'video_id': 'wL4K2IJR7xQ', 'title': '1NF 2NF 3NF BCNF', 'channel': 'Knowledge Gate'},
        ],
        # Transactions
        'transaction': [
            {'video_id': 'Oj1m4Kp8dBw', 'title': 'ACID Properties in DBMS', 'channel': 'Gate Smashers'},
            {'video_id': 'U37kN6BWGro', 'title': 'Transaction Management', 'channel': 'Knowledge Gate'},
        ],
        # Machine Learning
        'machine learning': [
            {'video_id': 'GwIo3gDXXCV', 'title': 'Machine Learning Full Course', 'channel': 'Simplilearn'},
            {'video_id': 'i_LwuuR6-Rc', 'title': 'Machine Learning for Beginners', 'channel': 'freeCodeCamp'},
            {'video_id': '7ArmBOP2odc', 'title': 'Machine Learning Explained', 'channel': 'Fireship'},
        ],
        # Linear Regression
        'linear regression': [
            {'video_id': '7ArmBOP2odc', 'title': 'Linear Regression Explained', 'channel': 'StatQuest'},
            {'video_id': 'k7JMGk3rRDE', 'title': 'Linear Regression in Python', 'channel': 'freeCodeCamp'},
        ],
        # Logistic Regression
        'logistic regression': [
            {'video_id': 'VCJdg7YBbAQ', 'title': 'Logistic Regression Explained', 'channel': 'StatQuest'},
            {'video_id': 'yIYK4eCdAkk', 'title': 'Logistic Regression Tutorial', 'channel': 'freeCodeCamp'},
        ],
        # Decision Tree
        'decision tree': [
            {'video_id': '_L39rN6gz7Y', 'title': 'Decision Trees Explained', 'channel': 'StatQuest'},
            {'video_id': '7VeUPuFGJHk', 'title': 'Decision Tree Algorithm', 'channel': 'freeCodeCamp'},
        ],
        # Random Forest
        'random forest': [
            {'video_id': 'J4WdyFOBW-8', 'title': 'Random Forests Explained', 'channel': 'StatQuest'},
            {'video_id': '0JGfKJLWJME', 'title': 'Random Forest Tutorial', 'channel': 'freeCodeCamp'},
        ],
        # Neural Network
        'neural network': [
            {'video_id': 'aircAruvnKk', 'title': 'Neural Networks Explained', 'channel': '3Blue1Brown'},
            {'video_id': 'jf1cBgIUfKo', 'title': 'Neural Networks from Scratch', 'channel': 'freeCodeCamp'},
            {'video_id': '9YrVipLhDcw', 'title': 'Deep Learning Full Course', 'channel': 'freeCodeCamp'},
        ],
        # Deep Learning
        'deep learning': [
            {'video_id': 'aircAruvnKk', 'title': 'Deep Learning Explained', 'channel': '3Blue1Brown'},
            {'video_id': '9YrVipLhDcw', 'title': 'Deep Learning Full Course', 'channel': 'freeCodeCamp'},
        ],
        # CNN
        'convolutional': [
            {'video_id': '2-Oaz7A_AHU', 'title': 'CNN Explained Simply', 'channel': 'Fireship'},
            {'video_id': 'HcyTHbskOgI', 'title': 'Convolutional Neural Networks Tutorial', 'channel': 'freeCodeCamp'},
        ],
        # RNN
        'recurrent': [
            {'video_id': '8HyCNIVRbSU', 'title': 'RNN Explained', 'channel': 'Fireship'},
            {'video_id': 'SEnXpx6W2lk', 'title': 'LSTM Networks Explained', 'channel': 'StatQuest'},
        ],
        # Transformer
        'transformer': [
            {'video_id': 'TQQlWhbFxsY', 'title': 'Transformers Explained', 'channel': 'Google AI'},
            {'video_id': 'kCc8FmEb1nY', 'title': 'Transformers from Scratch', 'channel': 'Andrej Karpathy'},
        ],
        # Search Algorithms AI
        'search algorithm': [
            {'video_id': 'PC-GKhKjBm0', 'title': 'BFS and DFS Algorithms', 'channel': 'Abdul Bari'},
            {'video_id': 'p9k-tBETxnI', 'title': 'A* Search Algorithm Explained', 'channel': 'Sebastian Lague'},
        ],
        # Dynamic Programming
        'dynamic programming': [
            {'video_id': 'P8Xa2AnXfx4', 'title': 'Dynamic Programming Tutorial', 'channel': 'Abdul Bari'},
            {'video_id': '9oSRxSpV26Y', 'title': 'Dynamic Programming Patterns', 'channel': 'NeetCode'},
            {'video_id': 'oBt53YbR9Kk', 'title': 'Dynamic Programming Course', 'channel': 'freeCodeCamp'},
        ],
        # Algorithm Analysis
        'algorithm analysis': [
            {'video_id': 'gC4L7fUrm2s', 'title': 'Big O Notation Explained', 'channel': 'Fireship'},
            {'video_id': '42GhozZMbME', 'title': 'Time Complexity Analysis', 'channel': 'Abdul Bari'},
        ],
        # Operating System
        'operating system': [
            {'video_id': '26QPDBeKp4k', 'title': 'Operating System Full Course', 'channel': 'Education 4u'},
            {'video_id': 'vBURtT1mKdI', 'title': 'OS Concepts Explained', 'channel': 'Neso Academy'},
        ],
        # Computer Network
        'computer network': [
            {'video_id': 'qiQR5rtsjTc', 'title': 'Computer Networks Full Course', 'channel': 'freeCodeCamp'},
            {'video_id': '5WQxnMKzfQs', 'title': 'Networking Fundamentals', 'channel': 'PowerCert'},
        ],
        # Software Engineering
        'software engineering': [
            {'video_id': 'bdkdHDBvREU', 'title': 'Software Engineering Tutorial', 'channel': 'Simplilearn'},
            {'video_id': 'zBfJX3Ekb_s', 'title': 'SDLC Explained', 'channel': 'Edureka'},
        ],
        # OOP
        'object oriented': [
            {'video_id': 'pTB30ZJ1fmE', 'title': 'Object Oriented Programming', 'channel': 'Bro Code'},
            {'video_id': 'SS-9y0Hc3uc', 'title': 'OOP Concepts Explained', 'channel': 'Fireship'},
        ],
        # Data Structures General
        'data structure': [
            {'video_id': 'xDhdIRfcr1U', 'title': 'Data Structures and Algorithms', 'channel': 'Abdul Bari'},
            {'video_id': '0IAPdL5vXDI', 'title': 'DSA Full Course', 'channel': 'College Wallah'},
        ],
        # NLP
        'natural language processing': [
            {'video_id': '8HyCNIVRbSU', 'title': 'NLP Tutorial', 'channel': 'freeCodeCamp'},
            {'video_id': 'OMCCt7vFQD8', 'title': 'NLP with Transformers', 'channel': 'Fireship'},
        ],
        # Blockchain
        'blockchain': [
            {'video_id': 'SSo_EIwHSd4', 'title': 'Blockchain Explained', 'channel': 'Fireship'},
            {'video_id': '33W1q3NcV6o', 'title': 'Blockchain Full Course', 'channel': 'freeCodeCamp'},
        ],
        # Cloud Computing
        'cloud computing': [
            {'video_id': 'M988_7Jz00U', 'title': 'Cloud Computing Explained', 'channel': 'Fireship'},
            {'video_id': 'SOTamWNgDKc', 'title': 'AWS Full Course', 'channel': 'freeCodeCamp'},
        ],
        # Web Development
        'web development': [
            {'video_id': 'UB1O30fR-EE', 'title': 'Web Development Tutorial', 'channel': 'freeCodeCamp'},
            {'video_id': 'pQN-pnXPaVg', 'title': 'HTML CSS JavaScript Full Course', 'channel': 'SuperSimpleDev'},
        ],
        # Probability and Statistics
        'probability': [
            {'video_id': 'uzkcQNRS8OM', 'title': 'Probability and Statistics', 'channel': 'freeCodeCamp'},
            {'video_id': 'mdFzOb5T1gM', 'title': 'Statistics for Data Science', 'channel': 'Simplilearn'},
        ],
        # Cyber Security
        'cyber security': [
            {'video_id': 'inWWhr5tnEA', 'title': 'Cyber Security Full Course', 'channel': 'NetworkChuck'},
            {'video_id': 'fNzpcB7ODxQ', 'title': 'Ethical Hacking Tutorial', 'channel': 'freeCodeCamp'},
        ],
        # IoT
        'internet of things': [
            {'video_id': 'bMFkDGbXEM0', 'title': 'IoT Full Course', 'channel': 'freeCodeCamp'},
            {'video_id': 'g2PAYF8GBWQ', 'title': 'IoT Tutorial for Beginners', 'channel': 'Simplilearn'},
        ],
        # Big Data
        'big data': [
            {'video_id': 'bA5B3GeTPB0', 'title': 'Big Data Analytics', 'channel': 'freeCodeCamp'},
            {'video_id': 'HaHcb4cOBwE', 'title': 'Hadoop and Spark Tutorial', 'channel': 'Simplilearn'},
        ],
        # Mobile Development
        'mobile app': [
            {'video_id': '0-SU1OZVnsI', 'title': 'Mobile App Development', 'channel': 'freeCodeCamp'},
            {'video_id': '5Mb6BCfEYmU', 'title': 'React Native Tutorial', 'channel': 'Bro Code'},
        ],
        # Generative AI
        'generative ai': [
            {'video_id': 'ad79nYk2keg', 'title': 'Generative AI Explained', 'channel': 'Fireship'},
            {'video_id': 'zjkBMFhNj_g', 'title': 'Generative AI Full Course', 'channel': 'freeCodeCamp'},
        ],
        # Computer Vision
        'computer vision': [
            {'video_id': 'QfN2oqR1cbY', 'title': 'Computer Vision Tutorial', 'channel': 'freeCodeCamp'},
            {'video_id': 'yNjAM7o-lbc', 'title': 'OpenCV Python Tutorial', 'channel': 'freeCodeCamp'},
        ],
        # Information Security
        'information security': [
            {'video_id': 'inWWhr5tnEA', 'title': 'Information Security', 'channel': 'NetworkChuck'},
            {'video_id': 'p4TeAVZ1BOY', 'title': 'Security Engineering', 'channel': 'freeCodeCamp'},
        ],
        # Project Management
        'project management': [
            {'video_id': 'PweL1xYbIQA', 'title': 'Project Management Tutorial', 'channel': 'Simplilearn'},
            {'video_id': 'MS6TDJb1tgM', 'title': 'Agile and Scrum', 'channel': 'freeCodeCamp'},
        ],
        # Distributed Systems
        'distributed system': [
            {'video_id': 'Y6Ev8GIlbxc', 'title': 'Distributed Systems', 'channel': 'MIT OpenCourseWare'},
            {'video_id': 'px1kMcBq3hg', 'title': 'Distributed Systems Explained', 'channel': 'Fireship'},
        ],
        # Engineering Math
        'mathematics': [
            {'video_id': 'fYQAVNejfDI', 'title': 'Engineering Mathematics', 'channel': 'freeCodeCamp'},
            {'video_id': 'WUvTyaaNkzM', 'title': 'Calculus Full Course', 'channel': 'MIT OpenCourseWare'},
        ],
        # Physics
        'physics': [
            {'video_id': '_9at3ZjvQx4', 'title': 'Engineering Physics', 'channel': 'Physics Wallah'},
        ],
        # Chemistry
        'chemistry': [
            {'video_id': 'bka20Q9TN6M', 'title': 'Engineering Chemistry', 'channel': 'Physics Wallah'},
        ],
        # Programming
        'programming': [
            {'video_id': 'rfscVS0vtbw', 'title': 'Python Tutorial for Beginners', 'channel': 'Programming with Mosh'},
            {'video_id': 'kqtD5dpn9C8', 'title': 'Python Full Course', 'channel': 'freeCodeCamp'},
        ],
        # Digital Electronics
        'digital electronics': [
            {'video_id': 'kDp6wqjYPgc', 'title': 'Digital Electronics Tutorial', 'channel': 'Neso Academy'},
            {'video_id': 'soGRyl9r0SA', 'title': 'Boolean Algebra', 'channel': 'Neso Academy'},
        ],
        # Microprocessor
        'microprocessor': [
            {'video_id': 'mB4SmaXcjBQ', 'title': 'Microprocessor 8086 Tutorial', 'channel': 'Education 4u'},
            {'video_id': 'QaGO6GBsT_U', 'title': 'Microprocessors Full Course', 'channel': 'freeCodeCamp'},
        ],
        # Communication Skills
        'communication': [
            {'video_id': 'uHCOl0YmrWg', 'title': 'Communication Skills', 'channel': 'Simplilearn'},
        ],
        # Environmental Studies
        'environment': [
            {'video_id': 'Ff4CDSjhBTY', 'title': 'Environmental Studies', 'channel': 'Unacademy'},
        ],
    }
    # Merge: comprehensive syllabus videos take priority, legacy fills gaps
    curated_videos = {**legacy_videos, **CURATED_VIDEOS}

    # Search the curated database
    query_lower = query.lower()
    matched = []

    for key, videos in curated_videos.items():
        if key in query_lower or query_lower in key:
            for v in videos[:max_results]:
                video_id = v.get('video_id', '')
                matched.append({
                    'video_id': video_id,
                    'title': v.get('title', query),
                    'channel': v.get('channel', 'Educational'),
                    'description': f"Learn {query} with this educational video",
                    'thumbnail': f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg',
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    'embed_url': f'https://www.youtube.com/embed/{video_id}',
                    'view_count': 0,
                    'like_count': 0
                })

    # If no match, try partial matching
    if not matched:
        for key, videos in curated_videos.items():
            query_words = query_lower.split()
            if any(word in key for word in query_words):
                for v in videos[:max_results]:
                    video_id = v.get('video_id', '')
                    matched.append({
                        'video_id': video_id,
                        'title': v.get('title', query),
                        'channel': v.get('channel', 'Educational'),
                        'description': f"Learn {query} with this educational video",
                        'thumbnail': f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg',
                        'url': f'https://www.youtube.com/watch?v={video_id}',
                        'embed_url': f'https://www.youtube.com/embed/{video_id}',
                        'view_count': 0,
                        'like_count': 0
                    })
                if matched:
                    break

    return matched[:max_results]


def auto_populate_lectures(module_id, topic_name, subject_name):
    """
    Auto-find and populate lectures for a module using YouTube search.
    The lectures table uses module_id.
    """
    # Check if lectures already exist for this module
    existing = query_db('SELECT COUNT(*) as cnt FROM lectures WHERE module_id = %s', [module_id], one=True)
    if existing and existing['cnt'] > 0:
        return existing['cnt']

    # Search YouTube for this topic
    search_query = f"{topic_name} {subject_name} tutorial"
    videos = search_youtube(search_query, max_results=3)

    if not videos:
        # Fallback: try just the topic name
        videos = search_youtube(topic_name, max_results=3)

    lecture_count = 0
    for idx, video in enumerate(videos):
        video_id = video.get('video_id', '')
        title = video.get('title', f'{topic_name} - Lecture {idx + 1}')

        # The lectures table has: module_id, title, youtube_video_id, duration_seconds
        query_db('''
            INSERT INTO lectures (module_id, title, youtube_video_id, duration_seconds)
            VALUES (%s, %s, %s, %s)
        ''', [
            module_id,
            title,
            video_id,
            600  # 10 minutes default
        ])
        lecture_count += 1

    return lecture_count


def auto_generate_transcript(lecture_id, topic_name):
    """Generate a basic transcript content for a lecture based on topic."""
    existing = query_db('SELECT id FROM transcripts WHERE lecture_id = %s', [lecture_id], one=True)
    if existing:
        return

    transcript = f"""This lecture covers the fundamentals of {topic_name}. 

Key topics discussed in this lecture:

1. Introduction to {topic_name} - Understanding the core concepts and why they matter in computer science and software engineering.

2. Core Concepts - The fundamental building blocks and principles that form the foundation of {topic_name}.

3. Implementation Details - Step-by-step walkthrough of how {topic_name} works in practice, including common operations and their time complexity.

4. Examples and Applications - Real-world use cases and practical examples demonstrating the application of {topic_name}.

5. Common Mistakes - Pitfalls to avoid when working with {topic_name}, including performance issues and logical errors.

6. Summary - Quick recap of the key takeaways and what you should remember about {topic_name}.

This lecture is designed to provide a comprehensive understanding of {topic_name} and prepare you for the upcoming assignment."""

    query_db('''
        INSERT INTO transcripts (lecture_id, transcript_text)
        VALUES (%s, %s)
    ''', [lecture_id, transcript])


def auto_generate_notes(lecture_id, topic_name, subject_name):
    """Generate AI-style lecture notes for a topic."""
    existing = query_db('SELECT id FROM lecture_notes WHERE lecture_id = %s', [lecture_id], one=True)
    if existing:
        return

    # Generate meaningful summary based on topic
    summary = f"This lecture provides a comprehensive introduction to {topic_name} in the context of {subject_name}. Students will learn the fundamental principles, key concepts, and practical applications of {topic_name}."

    # Key concepts based on topic
    key_concepts = _generate_key_concepts(topic_name)
    important_points = _generate_important_points(topic_name)
    revision_notes = _generate_revision_notes(topic_name)
    possible_questions = _generate_possible_questions(topic_name)

    query_db('''
        INSERT INTO lecture_notes (lecture_id, summary, key_concepts, important_points, revision_notes, possible_questions)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', [lecture_id, summary, key_concepts, important_points, revision_notes, possible_questions])


def _generate_key_concepts(topic_name):
    """Generate key concepts for a topic."""
    concepts_map = {
        'Arrays': 'Contiguous Memory, Index Access, O(1) Retrieval, Fixed Size, Traversal, Insertion, Deletion',
        'Linked Lists': 'Node, Head, Tail, Pointer, Singly Linked, Doubly Linked, Dynamic Size',
        'Stacks': 'LIFO, Push, Pop, Peek, Stack Overflow, Expression Evaluation',
        'Queues': 'FIFO, Enqueue, Dequeue, Circular Queue, Priority Queue',
        'Trees': 'Root, Node, Leaf, Binary Tree, BST, Traversal, Height, Depth',
        'Graphs': 'Vertex, Edge, Adjacency Matrix, BFS, DFS, Weighted Graph',
        'Sorting': 'Bubble Sort, Merge Sort, Quick Sort, Time Complexity, Stable Sort',
        'Searching': 'Linear Search, Binary Search, Time Complexity, Search Space',
        'SQL': 'SELECT, INSERT, UPDATE, DELETE, WHERE, JOIN, GROUP BY, Aggregate Functions',
        'Machine Learning': 'Supervised, Unsupervised, Training, Features, Labels, Model, Prediction',
        'Neural Networks': 'Perceptron, Activation Function, Backpropagation, Weights, Bias, Loss Function',
        'Decision Trees': 'Root Node, Splitting, Gini Impurity, Information Gain, Pruning',
        'Dynamic Programming': 'Optimal Substructure, Overlapping Subproblems, Memoization, Tabulation',
        'Linear Regression': 'Regression Line, Slope, Intercept, Cost Function, Gradient Descent',
        'Logistic Regression': 'Sigmoid Function, Binary Classification, Decision Boundary, Log Loss',
        'Random Forest': 'Ensemble, Bagging, Decision Trees, Feature Importance, Out-of-Bag',
        'Search Algorithms': 'BFS, DFS, A*, Heuristic, State Space, Goal Test',
        'Transformers': 'Self-Attention, Multi-Head Attention, Positional Encoding, Encoder-Decoder',
        'Convolutional Neural Networks': 'Convolution, Pooling, Feature Maps, Filters, Stride, Padding',
    }

    for key, concepts in concepts_map.items():
        if key.lower() in topic_name.lower():
            return concepts

    return f"{topic_name} Fundamentals, Core Concepts, Implementation, Applications, Common Patterns, Best Practices"


def _generate_important_points(topic_name):
    """Generate important points for a topic."""
    return f"""1. Understand the core principles of {topic_name}
2. Know the time and space complexity of common operations
3. Be able to implement basic operations from scratch
4. Understand when to use {topic_name} vs other approaches
5. Practice with real-world examples and edge cases"""


def _generate_revision_notes(topic_name):
    """Generate revision notes."""
    return f"""Revision Notes for {topic_name}:

• Definition: {topic_name} is a fundamental concept in computer science
• Key Properties: Understanding the defining characteristics
• Operations: Learn the basic and advanced operations
• Complexity: Know the time and space complexity
• Applications: Real-world use cases
• Common Mistakes: Avoid these common pitfalls"""


def _generate_possible_questions(topic_name):
    """Generate possible exam questions."""
    return f"""1. What is {topic_name} and why is it important?
2. Explain the basic operations of {topic_name} with examples
3. What is the time complexity of key operations?
4. Compare {topic_name} with alternative approaches
5. Implement a basic example of {topic_name} from scratch"""


def setup_lectures_for_topic(module_id, topic_name, subject_name):
    """Complete setup: populate lectures, transcripts, and notes for a module."""
    lecture_count = auto_populate_lectures(module_id, topic_name, subject_name)

    lectures = query_db('SELECT id FROM lectures WHERE module_id = %s', [module_id])
    for lecture in lectures:
        auto_generate_transcript(lecture['id'], topic_name)
        auto_generate_notes(lecture['id'], topic_name, subject_name)

    return lecture_count
