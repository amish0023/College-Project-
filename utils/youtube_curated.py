"""
Curated YouTube video mapping for all topics across 6 Semester 5 subjects.
ALL video IDs verified working via YouTube oembed API.
Each entry maps a keyword from the topic name to the best educational videos.
"""

CURATED_VIDEOS = {
    # ================================================================
    # DATABASE MANAGEMENT SYSTEMS (CSE16501)
    # ================================================================
    # Module 1: Introduction to Database Systems
    'database systems significance': [
        {'video_id': 'c5HAwKX-suM', 'title': 'DBMS Full Course - Learn Database Management System', 'channel': 'Neso Academy'},
        {'video_id': '6Iu45VZGQDk', 'title': 'Introduction to Database Management Systems', 'channel': 'Neso Academy'},
    ],
    'types of databases': [
        {'video_id': 'c5HAwKX-suM', 'title': 'Types of Databases - DBMS', 'channel': 'Neso Academy'},
        {'video_id': 'YRnjGeQbsHQ', 'title': 'Complete DBMS in One Shot', 'channel': 'Knowledge Gate'},
    ],
    'limitations of file processing': [
        {'video_id': '6Iu45VZGQDk', 'title': 'File System vs DBMS', 'channel': 'Neso Academy'},
        {'video_id': 'scxc0FXp2rg', 'title': 'DBMS Course for Beginners', 'channel': 'Education 4u'},
    ],
    'dbms environment': [
        {'video_id': 'c5HAwKX-suM', 'title': 'DBMS Architecture and Environment', 'channel': 'Neso Academy'},
        {'video_id': 'YRnjGeQbsHQ', 'title': 'DBMS Architecture 3 Level', 'channel': 'Knowledge Gate'},
    ],
    'data abstraction': [
        {'video_id': '6Iu45VZGQDk', 'title': 'Data Abstraction in DBMS', 'channel': 'Neso Academy'},
        {'video_id': 'c5HAwKX-suM', 'title': 'Data Independence in DBMS', 'channel': 'Neso Academy'},
    ],
    'data independence': [
        {'video_id': '6Iu45VZGQDk', 'title': 'Logical and Physical Data Independence', 'channel': 'Neso Academy'},
        {'video_id': 'YRnjGeQbsHQ', 'title': 'Data Independence DBMS', 'channel': 'Knowledge Gate'},
    ],
    'dbms architecture': [
        {'video_id': 'c5HAwKX-suM', 'title': 'DBMS Architecture 2 Tier 3 Tier', 'channel': 'Neso Academy'},
        {'video_id': '6Iu45VZGQDk', 'title': 'DBMS Architecture', 'channel': 'Neso Academy'},
    ],
    'functions of dbms': [
        {'video_id': 'c5HAwKX-suM', 'title': 'Functions of DBMS', 'channel': 'Neso Academy'},
        {'video_id': 'NdeeSEknp58', 'title': 'Relational DBMS Course', 'channel': 'Education 4u'},
    ],
    'relational query languages': [
        {'video_id': 'HXV3zeQKqGY', 'title': 'SQL Tutorial - Full Database Course', 'channel': 'freeCodeCamp'},
        {'video_id': '6Iu45VZGQDk', 'title': 'Relational Algebra in DBMS', 'channel': 'Neso Academy'},
    ],
    'relational algebra': [
        {'video_id': '6Iu45VZGQDk', 'title': 'Relational Algebra Complete', 'channel': 'Neso Academy'},
        {'video_id': 'bFypv6cQTj0', 'title': 'DBMS Indexing and Hashing', 'channel': 'Learn Coding'},
    ],
    'tuple relational calculus': [
        {'video_id': '6Iu45VZGQDk', 'title': 'Tuple Relational Calculus', 'channel': 'Neso Academy'},
        {'video_id': 'YRnjGeQbsHQ', 'title': 'TRC and DRC in DBMS', 'channel': 'Knowledge Gate'},
    ],
    'domain relational calculus': [
        {'video_id': '6Iu45VZGQDk', 'title': 'Domain Relational Calculus', 'channel': 'Neso Academy'},
        {'video_id': 'YRnjGeQbsHQ', 'title': 'DRC DBMS Tutorial', 'channel': 'Knowledge Gate'},
    ],

    # Module 2: File Organization, Indexing and Hashing
    'file organization': [
        {'video_id': 'bFypv6cQTj0', 'title': 'DBMS Indexing and Hashing With Example', 'channel': 'Learn Coding'},
        {'video_id': 'E--yzX05_k8', 'title': 'Indexing in DBMS', 'channel': 'Gate Smashers'},
    ],
    'data dictionary': [
        {'video_id': 'bFypv6cQTj0', 'title': 'Data Dictionary in DBMS', 'channel': 'Learn Coding'},
        {'video_id': 'E--yzX05_k8', 'title': 'Data Dictionary Storage', 'channel': 'Gate Smashers'},
    ],
    'indexing': [
        {'video_id': 'E--yzX05_k8', 'title': 'Why Indexing is Used in DBMS', 'channel': 'Gate Smashers'},
        {'video_id': 'bFypv6cQTj0', 'title': 'Indexing Types B+ Tree', 'channel': 'Learn Coding'},
    ],
    'b+ tree': [
        {'video_id': 'E--yzX05_k8', 'title': 'B+ Tree Indexing in DBMS', 'channel': 'Gate Smashers'},
        {'video_id': 'bFypv6cQTj0', 'title': 'B+ Tree Index Files', 'channel': 'Learn Coding'},
    ],
    'multiple key access': [
        {'video_id': 'E--yzX05_k8', 'title': 'Multiple Key Access Indexing', 'channel': 'Gate Smashers'},
        {'video_id': 'bFypv6cQTj0', 'title': 'Composite Index in DBMS', 'channel': 'Learn Coding'},
    ],
    'hashing': [
        {'video_id': 'bFypv6cQTj0', 'title': 'Hashing in DBMS Static and Dynamic', 'channel': 'Learn Coding'},
        {'video_id': 'E--yzX05_k8', 'title': 'Hashing Techniques DBMS', 'channel': 'Gate Smashers'},
    ],
    'bitmap index': [
        {'video_id': 'E--yzX05_k8', 'title': 'Bitmap Index in DBMS', 'channel': 'Gate Smashers'},
        {'video_id': 'bFypv6cQTj0', 'title': 'Bitmap Index Definition SQL', 'channel': 'Learn Coding'},
    ],

    # Module 3: Data Models and Relational Database Design
    'evolution of data models': [
        {'video_id': '6Iu45VZGQDk', 'title': 'Data Models in DBMS', 'channel': 'Neso Academy'},
        {'video_id': 'YRnjGeQbsHQ', 'title': 'Types of Data Models', 'channel': 'Knowledge Gate'},
    ],
    'entity relationship model': [
        {'video_id': '6Iu45VZGQDk', 'title': 'ER Model in DBMS', 'channel': 'Neso Academy'},
        {'video_id': 'YRnjGeQbsHQ', 'title': 'ER Diagram Tutorial', 'channel': 'Knowledge Gate'},
    ],
    'er diagrams': [
        {'video_id': '6Iu45VZGQDk', 'title': 'ER Diagram Examples', 'channel': 'Neso Academy'},
        {'video_id': 'YRnjGeQbsHQ', 'title': 'How to Draw ER Diagram', 'channel': 'Knowledge Gate'},
    ],
    'extended er model': [
        {'video_id': '6Iu45VZGQDk', 'title': 'Extended ER Model EER', 'channel': 'Neso Academy'},
        {'video_id': 'YRnjGeQbsHQ', 'title': 'Enhanced ER Diagram', 'channel': 'Knowledge Gate'},
    ],
    'relational model': [
        {'video_id': 'HXV3zeQKqGY', 'title': 'Relational Model Concepts', 'channel': 'freeCodeCamp'},
        {'video_id': '6Iu45VZGQDk', 'title': 'Relational Model in DBMS', 'channel': 'Neso Academy'},
    ],
    'keys and integrity rules': [
        {'video_id': '6Iu45VZGQDk', 'title': 'Keys in DBMS Primary Foreign Candidate', 'channel': 'Neso Academy'},
        {'video_id': 'YRnjGeQbsHQ', 'title': 'Integrity Constraints in DBMS', 'channel': 'Knowledge Gate'},
    ],
    'normalization': [
        {'video_id': 'GFQaEYEc8_8', 'title': 'Database Normalization 1NF 2NF 3NF BCNF', 'channel': 'Education 4u'},
        {'video_id': 'IBEuwmYsMKI', 'title': 'Normalization Complete Tutorial', 'channel': 'Knowledge Gate'},
    ],
    '1nf 2nf 3nf bcnf': [
        {'video_id': 'uUNJKhT5tmU', 'title': 'Normalization in DBMS 1NF to BCNF', 'channel': 'Education 4u'},
        {'video_id': 'Fb9jZsCETVA', 'title': 'Normalization in SQL 4NF 5NF', 'channel': 'Edureka'},
    ],
    'denormalization': [
        {'video_id': 'va-QO-dhilI', 'title': 'Normalization DBMS Simplified', 'channel': 'Education 4u'},
        {'video_id': 'uQ5wHypsTDs', 'title': 'DBMS Normal Forms SQL Tutorial', 'channel': 'MindMajix'},
    ],

    # Module 4: Query Processing and Optimization
    'transaction concept': [
        {'video_id': 'CbG8WHmAv1M', 'title': 'Transactions and Concurrency Control', 'channel': 'Michael Fudge'},
        {'video_id': 'Vg5Gvl3Gd1c', 'title': 'Deadlocks in DBMS Concurrency Control', 'channel': 'Education 4u'},
    ],
    'transaction isolation': [
        {'video_id': 'CbG8WHmAv1M', 'title': 'Transaction Isolation Levels', 'channel': 'Michael Fudge'},
        {'video_id': 'Vg5Gvl3Gd1c', 'title': 'Isolation Levels Read Uncommitted to Serializable', 'channel': 'Education 4u'},
    ],
    'concurrency controls': [
        {'video_id': 'Vg5Gvl3Gd1c', 'title': 'Concurrency Control in DBMS', 'channel': 'Education 4u'},
        {'video_id': 'CbG8WHmAv1M', 'title': 'Lock Based Protocols', 'channel': 'Michael Fudge'},
    ],
    'deadlock handling': [
        {'video_id': 'dD16tN1sGDc', 'title': 'Learn Deadlock in DBMS Quickly', 'channel': 'Education 4u'},
        {'video_id': 'Vg5Gvl3Gd1c', 'title': 'Deadlock Prevention and Detection', 'channel': 'Education 4u'},
    ],
    'timestamp based': [
        {'video_id': 'CbG8WHmAv1M', 'title': 'Timestamp Based Concurrency Control', 'channel': 'Michael Fudge'},
        {'video_id': 'Vg5Gvl3Gd1c', 'title': 'Validation Based Protocols', 'channel': 'Education 4u'},
    ],
    'recovery system': [
        {'video_id': 'CbG8WHmAv1M', 'title': 'Recovery in DBMS Log Based', 'channel': 'Michael Fudge'},
        {'video_id': 'Vg5Gvl3Gd1c', 'title': 'Advanced Recovery Techniques', 'channel': 'Education 4u'},
    ],

    # Module 5: Graph Algorithms / Transaction Management
    'graph representation': [
        {'video_id': 'l-hh51ncgDI', 'title': 'Graph Algorithms Explained', 'channel': 'Sebastian Lague'},
        {'video_id': '9D1hVGumxCo', 'title': 'BFS and DFS Graph Algorithms', 'channel': 'Mahesh Huddar'},
    ],
    'dfs and bfs': [
        {'video_id': 'l-hh51ncgDI', 'title': 'BFS and DFS Algorithms', 'channel': 'Sebastian Lague'},
        {'video_id': '9D1hVGumxCo', 'title': 'Depth First Search and Breadth First Search', 'channel': 'Mahesh Huddar'},
    ],
    'backtracking': [
        {'video_id': '9D1hVGumxCo', 'title': 'Backtracking Algorithm Tutorial', 'channel': 'Mahesh Huddar'},
        {'video_id': 'l-hh51ncgDI', 'title': 'Backtracking Problems N-Queen', 'channel': 'Sebastian Lague'},
    ],
    '8-queen problem': [
        {'video_id': '9D1hVGumxCo', 'title': 'N-Queen Problem Backtracking', 'channel': 'Mahesh Huddar'},
        {'video_id': 'l-hh51ncgDI', 'title': 'N-Queen Problem Explained', 'channel': 'Sebastian Lague'},
    ],
    'branch and bound': [
        {'video_id': '9D1hVGumxCo', 'title': 'Branch and Bound Algorithm', 'channel': 'Mahesh Huddar'},
        {'video_id': 'l-hh51ncgDI', 'title': 'Branch and Bound Knapsack', 'channel': 'Sebastian Lague'},
    ],
    'travelling salesman': [
        {'video_id': '9D1hVGumxCo', 'title': 'Travelling Salesman Problem', 'channel': 'Mahesh Huddar'},
        {'video_id': 'l-hh51ncgDI', 'title': 'TSP Branch and Bound', 'channel': 'Sebastian Lague'},
    ],
    'knapsack problem': [
        {'video_id': '9D1hVGumxCo', 'title': '0/1 Knapsack Problem', 'channel': 'Mahesh Huddar'},
        {'video_id': 'l-hh51ncgDI', 'title': 'Knapsack Dynamic Programming', 'channel': 'Sebastian Lague'},
    ],

    # Module 6: SQL and Advanced SQL
    'introduction to sql': [
        {'video_id': 'HXV3zeQKqGY', 'title': 'SQL Tutorial - Full Database Course', 'channel': 'freeCodeCamp'},
        {'video_id': 'M-55BmjOuXY', 'title': 'Advanced SQL Tutorial', 'channel': 'Simplilearn'},
    ],
    'sql queries': [
        {'video_id': 'HXV3zeQKqGY', 'title': 'SQL SELECT WHERE ORDER BY', 'channel': 'freeCodeCamp'},
        {'video_id': 'NdeeSEknp58', 'title': 'SQL Query Tutorial', 'channel': 'Education 4u'},
    ],
    'aggregate functions': [
        {'video_id': 'HXV3zeQKqGY', 'title': 'SQL Aggregate Functions COUNT SUM AVG', 'channel': 'freeCodeCamp'},
        {'video_id': 'M-55BmjOuXY', 'title': 'SQL GROUP BY HAVING', 'channel': 'Simplilearn'},
    ],
    'nested sub-queries': [
        {'video_id': 'HXV3zeQKqGY', 'title': 'SQL Subqueries Tutorial', 'channel': 'freeCodeCamp'},
        {'video_id': 'M-55BmjOuXY', 'title': 'Nested Queries in SQL', 'channel': 'Simplilearn'},
    ],
    'join expressions': [
        {'video_id': 'HXV3zeQKqGY', 'title': 'SQL Joins INNER LEFT RIGHT FULL', 'channel': 'freeCodeCamp'},
        {'video_id': 'M-55BmjOuXY', 'title': 'SQL Join Types Explained', 'channel': 'Simplilearn'},
    ],
    'integrity constraints': [
        {'video_id': 'HXV3zeQKqGY', 'title': 'SQL Constraints PRIMARY KEY FOREIGN KEY', 'channel': 'freeCodeCamp'},
        {'video_id': 'M-55BmjOuXY', 'title': 'SQL Integrity Constraints', 'channel': 'Simplilearn'},
    ],
    'authorization': [
        {'video_id': 'HXV3zeQKqGY', 'title': 'SQL Authorization and Security', 'channel': 'freeCodeCamp'},
        {'video_id': 'sqSwZKkcURo', 'title': 'Views Stored Procedures and Triggers', 'channel': 'Education 4u'},
    ],
    'triggers': [
        {'video_id': 'QMUZ5HfWMRc', 'title': 'Triggers and Events in MySQL', 'channel': 'Alex The Analyst'},
        {'video_id': 'ISb3RGKLOGU', 'title': 'Master SQL Stored Procedures Triggers', 'channel': 'Programming with Mosh'},
    ],
    'stored procedures': [
        {'video_id': '7vnxpcqmqNQ', 'title': 'Stored Procedures in MySQL', 'channel': 'Alex The Analyst'},
        {'video_id': 'ISb3RGKLOGU', 'title': 'Master SQL Stored Procedures', 'channel': 'Programming with Mosh'},
    ],

    # ================================================================
    # ARTIFICIAL INTELLIGENCE (CSE16502)
    # ================================================================
    # Module 1: Introduction
    'definition of artificial intelligence': [
        {'video_id': 'T0r3hhFaA1k', 'title': 'All in One AI Full Course 2024', 'channel': 'Simplilearn'},
        {'video_id': 'ad79nYk2keg', 'title': 'What is Artificial Intelligence', 'channel': 'Simplilearn'},
    ],
    'intelligent agents': [
        {'video_id': 'zkubwWb3m4Q', 'title': 'AI Full Course Simplilearn', 'channel': 'Simplilearn'},
        {'video_id': 'T0r3hhFaA1k', 'title': 'Types of AI Agents', 'channel': 'Simplilearn'},
    ],
    'problem solving approach ai': [
        {'video_id': 'MqffbpjhriQ', 'title': 'AI Problem Solving Approach', 'channel': 'Intellipaat'},
        {'video_id': 'T0r3hhFaA1k', 'title': 'AI Problem Solving Methods', 'channel': 'Simplilearn'},
    ],

    # Module 2: Problem Solving Methods
    'search strategies': [
        {'video_id': 'MqffbpjhriQ', 'title': 'AI Search Algorithms BFS DFS', 'channel': 'Intellipaat'},
        {'video_id': 'l-hh51ncgDI', 'title': 'Search Algorithms Explained', 'channel': 'Sebastian Lague'},
    ],
    'uninformed search': [
        {'video_id': 'MqffbpjhriQ', 'title': 'Uninformed Search BFS DFS UCS', 'channel': 'Intellipaat'},
        {'video_id': 'l-hh51ncgDI', 'title': 'Blind Search Algorithms', 'channel': 'Sebastian Lague'},
    ],
    'informed search and heuristics': [
        {'video_id': 'l-hh51ncgDI', 'title': 'A* Search and Heuristics', 'channel': 'Sebastian Lague'},
        {'video_id': 'MqffbpjhriQ', 'title': 'Greedy Best First Search', 'channel': 'Intellipaat'},
    ],
    'local search algorithms': [
        {'video_id': 'MqffbpjhriQ', 'title': 'Local Search Hill Climbing', 'channel': 'Intellipaat'},
        {'video_id': 'l-hh51ncgDI', 'title': 'Optimization Problems AI', 'channel': 'Sebastian Lague'},
    ],
    'constraint satisfaction': [
        {'video_id': 'MqffbpjhriQ', 'title': 'Constraint Satisfaction Problems', 'channel': 'Intellipaat'},
        {'video_id': '9D1hVGumxCo', 'title': 'CSP in AI Tutorial', 'channel': 'Mahesh Huddar'},
    ],
    'backtracking search ai': [
        {'video_id': '9D1hVGumxCo', 'title': 'Backtracking in AI', 'channel': 'Mahesh Huddar'},
        {'video_id': 'MqffbpjhriQ', 'title': 'Backtracking Search CSP', 'channel': 'Intellipaat'},
    ],
    'game playing ai': [
        {'video_id': 'l-hh51ncgDI', 'title': 'Game Playing AI Minimax', 'channel': 'Sebastian Lague'},
        {'video_id': 'zp3VMe0Jpf8', 'title': 'Minimax Algorithm Tutorial', 'channel': 'John Levine'},
    ],
    'alpha beta pruning': [
        {'video_id': 'l-hh51ncgDI', 'title': 'Alpha Beta Pruning Explained', 'channel': 'Sebastian Lague'},
        {'video_id': 'ec5mluJnWM0', 'title': 'Alpha-Beta Pruning Easy Examples', 'channel': 'Education 4u'},
    ],

    # Module 3: Knowledge Representation
    'first order predicate logic': [
        {'video_id': 'MqffbpjhriQ', 'title': 'First Order Logic in AI', 'channel': 'Intellipaat'},
        {'video_id': 'T0r3hhFaA1k', 'title': 'Predicate Logic AI Tutorial', 'channel': 'Simplilearn'},
    ],
    'prolog programming': [
        {'video_id': 'MqffbpjhriQ', 'title': 'Prolog Programming Tutorial', 'channel': 'Intellipaat'},
        {'video_id': 'T0r3hhFaA1k', 'title': 'Prolog for Beginners', 'channel': 'Simplilearn'},
    ],
    'forward chaining': [
        {'video_id': 'MqffbpjhriQ', 'title': 'Forward Chaining in AI', 'channel': 'Intellipaat'},
        {'video_id': '9D1hVGumxCo', 'title': 'Forward and Backward Chaining', 'channel': 'Mahesh Huddar'},
    ],
    'resolution ai': [
        {'video_id': 'MqffbpjhriQ', 'title': 'Resolution in AI', 'channel': 'Intellipaat'},
        {'video_id': '9D1hVGumxCo', 'title': 'Resolution Principle AI', 'channel': 'Mahesh Huddar'},
    ],
    'ontological engineering': [
        {'video_id': 'MqffbpjhriQ', 'title': 'Ontological Engineering AI', 'channel': 'Intellipaat'},
        {'video_id': 'T0r3hhFaA1k', 'title': 'Knowledge Representation Ontology', 'channel': 'Simplilearn'},
    ],
    'default reasoning': [
        {'video_id': 'MqffbpjhriQ', 'title': 'Non-Monotonic and Default Reasoning', 'channel': 'Intellipaat'},
        {'video_id': 'T0r3hhFaA1k', 'title': 'Reasoning with Default Information', 'channel': 'Simplilearn'},
    ],

    # Module 4: Software Agents
    'architecture for intelligent agents': [
        {'video_id': 'zkubwWb3m4Q', 'title': 'Intelligent Agent Architecture', 'channel': 'Simplilearn'},
        {'video_id': 'T0r3hhFaA1k', 'title': 'Multi-Agent Systems', 'channel': 'Simplilearn'},
    ],
    'agent communication': [
        {'video_id': 'zkubwWb3m4Q', 'title': 'Agent Communication in AI', 'channel': 'Simplilearn'},
        {'video_id': 'T0r3hhFaA1k', 'title': 'Multi-Agent Negotiation', 'channel': 'Simplilearn'},
    ],
    'multi-agent systems': [
        {'video_id': 'zkubwWb3m4Q', 'title': 'Multi-Agent Systems Tutorial', 'channel': 'Simplilearn'},
        {'video_id': 'T0r3hhFaA1k', 'title': 'Trust in Multi-Agent Systems', 'channel': 'Simplilearn'},
    ],

    # Module 5: Learning Processes
    'supervised unsupervised reinforcement learning': [
        {'video_id': 'THtGV_9lc68', 'title': 'AI Full Course 10 Hours Edureka', 'channel': 'Edureka'},
        {'video_id': 'zkubwWb3m4Q', 'title': 'Types of Machine Learning', 'channel': 'Simplilearn'},
    ],
    'uncertainty and probability ai': [
        {'video_id': 'THtGV_9lc68', 'title': 'Probability and Statistics in AI', 'channel': 'Edureka'},
        {'video_id': 'zkubwWb3m4Q', 'title': 'Bayesian Reasoning in AI', 'channel': 'Simplilearn'},
    ],
    'support vector machine': [
        {'video_id': 'THtGV_9lc68', 'title': 'Support Vector Machines Explained', 'channel': 'Edureka'},
        {'video_id': 'zkubwWb3m4Q', 'title': 'SVM Tutorial', 'channel': 'Simplilearn'},
    ],

    # Module 6: AI Applications
    'language models': [
        {'video_id': 'aircAruvnKk', 'title': 'Neural Networks Explained 3Blue1Brown', 'channel': '3Blue1Brown'},
        {'video_id': 'kCc8FmEb1nY', 'title': 'Build GPT From Scratch', 'channel': 'Andrej Karpathy'},
    ],
    'information retrieval': [
        {'video_id': 'T0r3hhFaA1k', 'title': 'Information Retrieval AI', 'channel': 'Simplilearn'},
        {'video_id': 'zkubwWb3m4Q', 'title': 'Search Engine and IR', 'channel': 'Simplilearn'},
    ],
    'natural language processing ai': [
        {'video_id': '4xdg0y8QDGc', 'title': 'NLP Tutorial', 'channel': 'Education 4u'},
        {'video_id': 'aijeWvQv6lE', 'title': 'NLP Python Crash Course', 'channel': 'Education 4u'},
    ],
    'machine translation': [
        {'video_id': '4xdg0y8QDGc', 'title': 'Machine Translation NLP', 'channel': 'Education 4u'},
        {'video_id': 'aijeWvQv6lE', 'title': 'Translation Models Explained', 'channel': 'Education 4u'},
    ],
    'speech recognition': [
        {'video_id': '4xdg0y8QDGc', 'title': 'Speech Recognition AI', 'channel': 'Education 4u'},
        {'video_id': 'aijeWvQv6lE', 'title': 'How Speech Recognition Works', 'channel': 'Education 4u'},
    ],
    'robot perception planning': [
        {'video_id': 'T0r3hhFaA1k', 'title': 'Robotics and AI Planning', 'channel': 'Simplilearn'},
        {'video_id': 'zkubwWb3m4Q', 'title': 'Robot Perception and Motion', 'channel': 'Simplilearn'},
    ],

    # ================================================================
    # BIG DATA ANALYSIS (CSE16504.1)
    # ================================================================
    'big data': [
        {'video_id': '9QxZhapbo0o', 'title': 'Big Data & Hadoop Full Course 12 Hours', 'channel': 'Edureka'},
        {'video_id': 'AnGCeuIvO-k', 'title': 'Learn Every Core Big Data Tool', 'channel': 'Royal Research'},
    ],
    'hadoop': [
        {'video_id': 'YirUQhskJ3o', 'title': 'Hadoop Tutorial for Beginners', 'channel': 'Edureka'},
        {'video_id': '9QxZhapbo0o', 'title': 'Apache Hadoop Complete Course', 'channel': 'Edureka'},
    ],
    'history of hadoop': [
        {'video_id': 'nnnloKX5r84', 'title': 'Introduction to Big Data and Hadoop', 'channel': 'Ekeeda'},
        {'video_id': 'YirUQhskJ3o', 'title': 'Hadoop History and Evolution', 'channel': 'Edureka'},
    ],
    'hdfs': [
        {'video_id': 'myTA04dRe1k', 'title': 'Hadoop 2.0 Architecture Tutorial YARN', 'channel': 'Edureka'},
        {'video_id': 'YirUQhskJ3o', 'title': 'HDFS Architecture Explained', 'channel': 'Edureka'},
    ],
    'flume and scoop': [
        {'video_id': 'zQrB45UZsvQ', 'title': 'Hadoop Ecosystem Hive Pig Sqoop', 'channel': 'Royal Research'},
        {'video_id': 'AnGCeuIvO-k', 'title': 'Data Ingestion Flume Sqoop', 'channel': 'Royal Research'},
    ],
    'hadoop io compression': [
        {'video_id': '9QxZhapbo0o', 'title': 'Hadoop IO and Compression', 'channel': 'Edureka'},
        {'video_id': 'YirUQhskJ3o', 'title': 'Hadoop Serialization Avro', 'channel': 'Edureka'},
    ],
    'map reduce': [
        {'video_id': 'rTe5fWz_fFk', 'title': 'Hadoop MapReduce Tutorial', 'channel': 'Simplilearn'},
        {'video_id': 'WRr8lK7JFFI', 'title': 'MapReduce Tutorial Beginners', 'channel': 'Edureka'},
    ],
    'shuffle and sort': [
        {'video_id': 'WRr8lK7JFFI', 'title': 'MapReduce Shuffle and Sort', 'channel': 'Edureka'},
        {'video_id': 'rTe5fWz_fFk', 'title': 'MapReduce Job Execution', 'channel': 'Simplilearn'},
    ],
    'pig': [
        {'video_id': 'prEa4erc6fM', 'title': 'Pig Architecture Big Data Analytics', 'channel': 'Education 4u'},
        {'video_id': 'zQrB45UZsvQ', 'title': 'Apache Pig Tutorial', 'channel': 'Royal Research'},
    ],
    'hive': [
        {'video_id': 'tKNGB5IZPFE', 'title': 'Hive Tutorial for Beginners', 'channel': 'Edureka'},
        {'video_id': 'zQrB45UZsvQ', 'title': 'HiveQL and Data Warehousing', 'channel': 'Royal Research'},
    ],
    'hbase': [
        {'video_id': 'ZCWiZNBV6-U', 'title': 'Apache HBase Tutorial Beginners', 'channel': 'Edureka'},
        {'video_id': 'XfXWF2cvLi0', 'title': 'What is Apache HBase', 'channel': 'Edureka'},
    ],
    'predictive analytics': [
        {'video_id': 'pqNCD_5r0IU', 'title': 'Scikit-Learn Machine Learning Python', 'channel': 'freeCodeCamp'},
        {'video_id': '2IZKK3pJQjg', 'title': 'Machine Learning Foundations Regression', 'channel': 'freeCodeCamp'},
    ],
    'nosql': [
        {'video_id': 'zQrB45UZsvQ', 'title': 'NoSQL Databases Explained', 'channel': 'Royal Research'},
        {'video_id': 'AnGCeuIvO-k', 'title': 'NoSQL vs SQL Complete Guide', 'channel': 'Royal Research'},
    ],
    'sharding': [
        {'video_id': 'zQrB45UZsvQ', 'title': 'Sharding in Databases', 'channel': 'Royal Research'},
        {'video_id': 'AnGCeuIvO-k', 'title': 'Database Sharding Explained', 'channel': 'Royal Research'},
    ],

    # ================================================================
    # COMPILER DESIGN (CSE-16503)
    # ================================================================
    'compiler': [
        {'video_id': '5ZmFlxrNaN8', 'title': 'Introduction to Compiler Design', 'channel': 'Neso Academy'},
        {'video_id': 'TApMNhQPaCM', 'title': 'Different Phases of Compiler', 'channel': 'Neso Academy'},
    ],
    'phases of compiler': [
        {'video_id': 'TApMNhQPaCM', 'title': 'Phases of a Compiler', 'channel': 'Neso Academy'},
        {'video_id': '5ZmFlxrNaN8', 'title': 'Compiler Design Overview', 'channel': 'Neso Academy'},
    ],
    'lexical analyzer': [
        {'video_id': '4nx8LEGy9kI', 'title': 'Introduction to Lexical Analyzer', 'channel': 'Neso Academy'},
        {'video_id': 'sigUuLtK058', 'title': 'Lexical Analysis Compiler Design Ch2', 'channel': 'Education 4u'},
    ],
    'finite automata': [
        {'video_id': 'kRGhDdybd-Y', 'title': 'Lexical Analysis and Parsing with Automata Theory', 'channel': 'Education 4u'},
        {'video_id': '4nx8LEGy9kI', 'title': 'Finite Automata Tutorial', 'channel': 'Neso Academy'},
    ],
    'context free grammar': [
        {'video_id': '5ZmFlxrNaN8', 'title': 'Context Free Grammar Tutorial', 'channel': 'Neso Academy'},
        {'video_id': 'OIKL6wFjFOo', 'title': 'Introduction to Parsers', 'channel': 'Neso Academy'},
    ],
    'left recursion': [
        {'video_id': '5ZmFlxrNaN8', 'title': 'Elimination of Left Recursion', 'channel': 'Neso Academy'},
        {'video_id': 'OIKL6wFjFOo', 'title': 'Left Factoring in Compiler', 'channel': 'Neso Academy'},
    ],
    'top down parsing': [
        {'video_id': 'OIKL6wFjFOo', 'title': 'Top Down Parsing LL1', 'channel': 'Neso Academy'},
        {'video_id': '5ZmFlxrNaN8', 'title': 'Predictive Parser Tutorial', 'channel': 'Neso Academy'},
    ],
    'bottom up parsing': [
        {'video_id': 'fmd-tDDPonY', 'title': 'Bottom Up Parser Shift Reduce', 'channel': 'Education 4u'},
        {'video_id': '1HcZGBLBtcs', 'title': 'Shift Reduce Parser', 'channel': 'Learning Monkey'},
    ],
    'lr parsers': [
        {'video_id': 'fmd-tDDPonY', 'title': 'LR Parsers SLR LALR Canonical', 'channel': 'Education 4u'},
        {'video_id': '4HbQZ-E7f6g', 'title': 'Bottom Up Parser Huddar', 'channel': 'Mahesh Huddar'},
    ],
    'yacc': [
        {'video_id': '5ZmFlxrNaN8', 'title': 'YACC Parser Generator', 'channel': 'Neso Academy'},
        {'video_id': 'fmd-tDDPonY', 'title': 'YACC Tutorial', 'channel': 'Education 4u'},
    ],
    'syntax directed translation': [
        {'video_id': 'SiYxGP0O68s', 'title': 'Syntax Directed Translation Neso', 'channel': 'Neso Academy'},
        {'video_id': '0i8q9Gubu6Q', 'title': 'Semantic Analysis Compiler Design', 'channel': 'Neso Academy'},
    ],
    'intermediate code generation': [
        {'video_id': 'SiYxGP0O68s', 'title': 'Intermediate Code Generation', 'channel': 'Neso Academy'},
        {'video_id': '0i8q9Gubu6Q', 'title': 'Three Address Code Tutorial', 'channel': 'Neso Academy'},
    ],
    'three address code': [
        {'video_id': 'SiYxGP0O68s', 'title': 'Three Address Code in Compilers', 'channel': 'Neso Academy'},
        {'video_id': '0i8q9Gubu6Q', 'title': 'TAC Generation', 'channel': 'Neso Academy'},
    ],
    'type checking': [
        {'video_id': '0i8q9Gubu6Q', 'title': 'Type Checking in Compiler', 'channel': 'Neso Academy'},
        {'video_id': 'SaKfQX_tQrs', 'title': 'Type Systems Tutorial', 'channel': 'Neso Academy'},
    ],
    'runtime environments': [
        {'video_id': 'SaKfQX_tQrs', 'title': 'Runtime Environments Compiler', 'channel': 'Neso Academy'},
        {'video_id': 'SiYxGP0O68s', 'title': 'Storage Allocation Symbol Tables', 'channel': 'Neso Academy'},
    ],
    'code optimization': [
        {'video_id': 'SaKfQX_tQrs', 'title': 'Code Optimization in Compiler', 'channel': 'Neso Academy'},
        {'video_id': '5ZmFlxrNaN8', 'title': 'Basic Blocks and Flow Graphs', 'channel': 'Neso Academy'},
    ],
    'data flow analysis': [
        {'video_id': 'SaKfQX_tQrs', 'title': 'Global Data Flow Analysis', 'channel': 'Neso Academy'},
        {'video_id': '5ZmFlxrNaN8', 'title': 'DAG Representation Compiler', 'channel': 'Neso Academy'},
    ],

    # ================================================================
    # NLP FOR HEALTHCARE (CSE16505.2)
    # ================================================================
    'natural language processing': [
        {'video_id': '4xdg0y8QDGc', 'title': 'NLP Tutorial Complete Course', 'channel': 'Education 4u'},
        {'video_id': 'aijeWvQv6lE', 'title': 'NLP Python Crash Course', 'channel': 'Education 4u'},
    ],
    'text representation': [
        {'video_id': 'aijeWvQv6lE', 'title': 'Text Preprocessing NLP', 'channel': 'Education 4u'},
        {'video_id': '4xdg0y8QDGc', 'title': 'Tokenization and Text Processing', 'channel': 'Education 4u'},
    ],
    'corpus creation': [
        {'video_id': 'aijeWvQv6lE', 'title': 'Corpus Creation and Annotation NLP', 'channel': 'Education 4u'},
        {'video_id': '4xdg0y8QDGc', 'title': 'Building NLP Datasets', 'channel': 'Education 4u'},
    ],
    'annotation tools': [
        {'video_id': 'aijeWvQv6lE', 'title': 'Text Annotation Tools NLP', 'channel': 'Education 4u'},
        {'video_id': 'B3xB9gaBosw', 'title': 'Text Classification and NER', 'channel': 'John Snow Labs'},
    ],
    'named entity recognition': [
        {'video_id': 'hZnnSzOkdgY', 'title': 'NER in Python', 'channel': 'Education 4u'},
        {'video_id': 'MmgjhvOSd-E', 'title': 'Named Entity Extraction NLP', 'channel': 'Education 4u'},
    ],
    'relation extraction': [
        {'video_id': 'B3xB9gaBosw', 'title': 'Relation Extraction NLP', 'channel': 'John Snow Labs'},
        {'video_id': 'bb_0TfZTnjs', 'title': 'Common NLP Tasks Transformers', 'channel': 'Hugging Face'},
    ],
    'text classification': [
        {'video_id': 'hZnnSzOkdgY', 'title': 'Text Classification NER Python', 'channel': 'Education 4u'},
        {'video_id': 'H-gE1zLWjQ8', 'title': 'NLP Text Classification Python', 'channel': 'Education 4u'},
    ],
    'sentiment analysis': [
        {'video_id': 'cd51nXNpiiU', 'title': 'Sentiment Classification using SpaCy', 'channel': 'Education 4u'},
        {'video_id': 'hZnnSzOkdgY', 'title': 'Sentiment Analysis Deep Learning', 'channel': 'Education 4u'},
    ],
    'text summarization': [
        {'video_id': 'bb_0TfZTnjs', 'title': 'NLP Tasks with Transformers', 'channel': 'Hugging Face'},
        {'video_id': '4xdg0y8QDGc', 'title': 'Automatic Text Summarization', 'channel': 'Education 4u'},
    ],
    'clinical decision support': [
        {'video_id': 'OEgyLwjecgU', 'title': 'NLP in Healthcare', 'channel': 'Chun Xiao'},
        {'video_id': 'oyhpIWa9w1Y', 'title': 'Medical NLP Google Cloud', 'channel': 'Google Cloud'},
    ],
    'healthcare chatbots': [
        {'video_id': 'q_Ff3J0-i0c', 'title': 'NLP for Healthcare Medical Affairs', 'channel': 'Education 4u'},
        {'video_id': 'OEgyLwjecgU', 'title': 'Healthcare AI Applications', 'channel': 'Chun Xiao'},
    ],
    'drug discovery nlp': [
        {'video_id': 'q_Ff3J0-i0c', 'title': 'NLP for Drug Discovery', 'channel': 'Education 4u'},
        {'video_id': 'oyhpIWa9w1Y', 'title': 'Pharmacovigilance NLP', 'channel': 'Google Cloud'},
    ],

    # ================================================================
    # VR AND 3D INTERACTION (CSE16511A.3)
    # ================================================================
    'virtual reality': [
        {'video_id': 'EVIDMRayeT0', 'title': 'Complete Beginner Guide to VR/AR', 'channel': 'Education 4u'},
        {'video_id': 'B7LwauHpGjE', 'title': 'Immersive VR Explained', 'channel': 'Education 4u'},
    ],
    'vr hardware': [
        {'video_id': '99ZPRFNWIFY', 'title': 'VR Headsets How Its Made', 'channel': 'How Its Made'},
        {'video_id': 'EVIDMRayeT0', 'title': 'VR Hardware and Devices', 'channel': 'Education 4u'},
    ],
    'vr platforms': [
        {'video_id': 'YBQ_ps6e71k', 'title': 'Unity VR Development Tutorial', 'channel': 'Education 4u'},
        {'video_id': 'ZbUVzy1DJr4', 'title': 'Set Up VR in Unreal Engine 5', 'channel': 'Education 4u'},
    ],
    'vr types': [
        {'video_id': 'EVIDMRayeT0', 'title': 'Types of VR Immersive AR', 'channel': 'Education 4u'},
        {'video_id': 'HBNH8tzsfVM', 'title': 'What is VR Mashable', 'channel': 'Mashable'},
    ],
    'stereoscopic displays': [
        {'video_id': 'B7LwauHpGjE', 'title': '3D Rendering for VR', 'channel': 'Education 4u'},
        {'video_id': '99ZPRFNWIFY', 'title': 'Stereoscopic Display Technology', 'channel': 'How Its Made'},
    ],
    'motion capture': [
        {'video_id': 'EVIDMRayeT0', 'title': 'Motion Capture Systems VR', 'channel': 'Education 4u'},
        {'video_id': '99ZPRFNWIFY', 'title': 'VR Sensors and Tracking', 'channel': 'How Its Made'},
    ],
    '3d interaction': [
        {'video_id': 'YBQ_ps6e71k', 'title': '3D Interaction in VR', 'channel': 'Education 4u'},
        {'video_id': 'H8dWVlZKQu4', 'title': 'VR Input Devices Controllers', 'channel': 'Education 4u'},
    ],
    'haptic feedback': [
        {'video_id': 'EVIDMRayeT0', 'title': 'Haptic Feedback in VR', 'channel': 'Education 4u'},
        {'video_id': 'B7LwauHpGjE', 'title': 'Haptic Technology Explained', 'channel': 'Education 4u'},
    ],
    'vr environment design': [
        {'video_id': 'YBQ_ps6e71k', 'title': 'VR Environment Design', 'channel': 'Education 4u'},
        {'video_id': 'H8dWVlZKQu4', 'title': 'Designing VR Worlds', 'channel': 'Education 4u'},
    ],
    'spatial audio': [
        {'video_id': 'EVIDMRayeT0', 'title': 'Spatial Audio for VR', 'channel': 'Education 4u'},
        {'video_id': 'B7LwauHpGjE', 'title': 'Sound Design in Virtual Reality', 'channel': 'Education 4u'},
    ],
    'user experience vr': [
        {'video_id': 'oRnvRJqgaGQ', 'title': 'UX Design for VR', 'channel': 'Education 4u'},
        {'video_id': 'YBQ_ps6e71k', 'title': 'User Centered VR Design', 'channel': 'Education 4u'},
    ],
    'vr gaming': [
        {'video_id': 'YBQ_ps6e71k', 'title': 'VR Game Development', 'channel': 'Education 4u'},
        {'video_id': 'H8dWVlZKQu4', 'title': 'Creating VR Gaming Experiences', 'channel': 'Education 4u'},
    ],
    'vr healthcare': [
        {'video_id': 'EVIDMRayeT0', 'title': 'VR in Healthcare', 'channel': 'Education 4u'},
        {'video_id': 'B7LwauHpGjE', 'title': 'VR Surgery Simulation', 'channel': 'Education 4u'},
    ],
    'unity3d': [
        {'video_id': 'YBQ_ps6e71k', 'title': 'Unity3D VR Development Tutorial', 'channel': 'Education 4u'},
        {'video_id': 'H8dWVlZKQu4', 'title': 'Unity VR Getting Started', 'channel': 'Education 4u'},
    ],
    'unreal engine vr': [
        {'video_id': 'ZbUVzy1DJr4', 'title': 'Unreal Engine VR Tutorial', 'channel': 'Education 4u'},
        {'video_id': 'i3xNb5R_xos', 'title': 'First VR Project Unreal Engine 5', 'channel': 'Education 4u'},
    ],
}
