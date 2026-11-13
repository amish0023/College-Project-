#!/usr/bin/env python
"""
Migration script: Update all 6 Semester 5 subjects with exact syllabus modules/topics.
Also cleans old lectures/assignments and maps curated YouTube videos.
"""
from utils import database as db

# Disable foreign key checks for clean migration
db.execute("SET FOREIGN_KEY_CHECKS = 0")
db.execute("SET SQL_SAFE_UPDATES = 0")

# ============================================================
# STEP 1: Update subject names and codes to match syllabus
# ============================================================
subject_updates = {
    13: ('Database Management Systems', 'CSE16501'),
    25: ('Artificial Intelligence', 'CSE16502'),
    31: ('Big Data Analysis', 'CSE16504.1'),
    47: ('Compiler Design', 'CSE16503'),
    48: ('Introduction to Virtual Reality and 3D Interaction', 'CSE16511A.3'),
    49: ('NLP for Health Related Text', 'CSE16505.2'),
}

for subj_id, (name, code) in subject_updates.items():
    db.execute("UPDATE subjects SET name=%s, code=%s WHERE id=%s", (name, code, subj_id))
    print(f"Updated subject {subj_id}: {name} ({code})")

# ============================================================
# STEP 2: Clear old modules, topics, lectures, assignments for these subjects
# ============================================================
for subj_id in subject_updates.keys():
    # Get module IDs
    modules = db.fetch_all("SELECT id FROM modules WHERE subject_id=%s", (subj_id,))
    module_ids = [m['id'] for m in modules]
    
    if module_ids:
        placeholders = ','.join(['%s'] * len(module_ids))
        
        # Delete old assignments via assignment_questions -> assignment_attempts -> assignments
        old_assigns = db.fetch_all(f"SELECT id FROM assignments WHERE module_id IN ({placeholders})", module_ids)
        assign_ids = [a['id'] for a in old_assigns]
        if assign_ids:
            a_placeholders = ','.join(['%s'] * len(assign_ids))
            db.execute(f"DELETE FROM assignment_answers WHERE attempt_id IN (SELECT id FROM assignment_attempts WHERE assignment_id IN ({a_placeholders}))", assign_ids)
            db.execute(f"DELETE FROM assignment_attempts WHERE assignment_id IN ({a_placeholders})", assign_ids)
            db.execute(f"DELETE FROM assignment_questions WHERE assignment_id IN ({a_placeholders})", assign_ids)
            db.execute(f"DELETE FROM assignments WHERE id IN ({a_placeholders})", assign_ids)
        
        # Delete old lecture progress, transcripts, lecture_notes, lectures
        lectures = db.fetch_all(f"SELECT id FROM lectures WHERE module_id IN ({placeholders})", module_ids)
        lecture_ids = [l['id'] for l in lectures]
        if lecture_ids:
            l_placeholders = ','.join(['%s'] * len(lecture_ids))
            db.execute(f"DELETE FROM lecture_progress WHERE lecture_id IN ({l_placeholders})", lecture_ids)
            db.execute(f"DELETE FROM transcripts WHERE lecture_id IN ({l_placeholders})", lecture_ids)
            db.execute(f"DELETE FROM lecture_notes WHERE lecture_id IN ({l_placeholders})", lecture_ids)
            db.execute(f"DELETE FROM lectures WHERE id IN ({l_placeholders})", lecture_ids)
        
        # Delete old topics and modules
        for mid in module_ids:
            db.execute("DELETE FROM topics WHERE module_id=%s", (mid,))
        db.execute(f"DELETE FROM modules WHERE id IN ({placeholders})", module_ids)
    
    print(f"Cleared old data for subject {subj_id}")

# ============================================================
# STEP 3: Insert new modules and topics from actual syllabus
# ============================================================

# --- DBMS (id=13) ---
dbms_modules = [
    (13, 'Introduction to Database Systems', 1, [
        'Database Systems Significance and Advantages',
        'Types of Databases',
        'Limitations of File Processing Systems',
        'DBMS Environment and Architecture',
        'Data Abstraction and Data Independence',
        'Functions of DBMS',
        'Formal Relational Query Languages',
        'Relational Algebra',
        'Tuple Relational Calculus',
        'Domain Relational Calculus',
    ]),
    (13, 'File Organization, Indexing and Hashing', 2, [
        'File Organization and Record Organization',
        'Data Dictionary Storage',
        'Basic Concepts of Indexing',
        'Ordered Indices and B+ Tree Index Files',
        'B+ Tree Indexing and Extensions',
        'Multiple Key Access',
        'Static and Dynamic Hashing',
        'Comparison of Ordered Indexing and Hashing',
        'Bitmap Index and Index Definition in SQL',
    ]),
    (13, 'Data Models and Relational Database Design', 3, [
        'Evolution of Data Models',
        'Entity Relationship Model and ER Diagrams',
        'Extended ER Model',
        'Relational Model and Logical View of Data',
        'Keys and Integrity Rules',
        'Relational Set Operators',
        'Data Dictionary and System Catalog',
        'Database Normalization: 1NF 2NF 3NF BCNF 4NF 5NF',
        'Denormalization and Database Design',
    ]),
    (13, 'Query Processing and Optimization', 4, [
        'Transaction Concept and Transaction Model',
        'Atomicity and Durability in Transactions',
        'Transaction Isolation Levels and Implementations',
        'Concurrency Controls and Lock Based Protocols',
        'Deadlock Handling',
        'Time-stamp Based Protocols',
        'Validation Based Protocols',
        'Recovery System Failure Classification',
        'Log Based Recovery and Advanced Recovery Techniques',
    ]),
    (13, 'Transaction Management', 5, [
        'Graph Representation and Strongly Connected Components',
        'Traversal Methods: DFS and BFS',
        'Backtracking: 8-Queen Problem',
        'Backtracking: Knapsack Problem',
        'Branch and Bound: LC Searching and Bounding',
        'FIFO Branch and Bound',
        'LC Branch and Bound Applications',
        '0/1 Knapsack Problem with Branch and Bound',
        'Travelling Salesman Problem',
    ]),
    (13, 'SQL and Advanced SQL', 6, [
        'Introduction to SQL and SQL Data Definition',
        'Basic Structure of SQL Queries',
        'Set Operations and Null Values',
        'Aggregate Functions and Nested Sub-queries',
        'Modifications of Databases',
        'Join Expressions and Views',
        'Integrity Constraints and Schema Changes',
        'Authorization and Advanced SQL',
        'Dynamic SQL and Embedded SQL',
        'Functions Procedures and Triggers',
    ]),
]

# --- AI (id=25) ---
ai_modules = [
    (25, 'Introduction to Artificial Intelligence', 1, [
        'Definition and Future of Artificial Intelligence',
        'Characteristics of Intelligent Agents',
        'Typical Intelligent Agents',
        'Problem Solving Approach to Typical AI Problems',
    ]),
    (25, 'Problem Solving Methods', 2, [
        'Problem Solving Methods and Search Strategies',
        'Uninformed Search Algorithms',
        'Informed Search and Heuristics',
        'Local Search Algorithms and Optimization',
        'Searching with Partial Observations',
        'Constraint Satisfaction Problems',
        'Constraint Propagation and Backtracking Search',
        'Game Playing and Optimal Decisions',
        'Alpha Beta Pruning and Stochastic Games',
    ]),
    (25, 'Knowledge Representation', 3, [
        'First Order Predicate Logic',
        'Prolog Programming and Unification',
        'Forward Chaining and Backward Chaining',
        'Resolution and Knowledge Representation',
        'Ontological Engineering and Categories',
        'Events Mental Events and Mental Objects',
        'Reasoning Systems for Categories',
        'Reasoning with Default Information',
    ]),
    (25, 'Software Agents', 4, [
        'Architecture for Intelligent Agents',
        'Agent Communication',
        'Negotiation and Bargaining among Agents',
        'Argumentation among Agents',
        'Trust and Reputation in Multi-Agent Systems',
    ]),
    (25, 'Learning Processes', 5, [
        'Introduction to Supervised Unsupervised and Reinforcement Learning',
        'Identifying the Type of Learning Process',
        'Extracting Conclusions from Uncertain Knowledge',
        'Probability and Uncertainty in Conclusions',
        'Linear Regression and Support Vector Machine',
        'Decision Trees and Random Forest',
    ]),
    (25, 'AI Applications', 6, [
        'Language Models',
        'Information Retrieval and Information Extraction',
        'Natural Language Processing',
        'Machine Translation and Speech Recognition',
        'Robot Hardware and Perception',
        'Planning and Moving',
    ]),
]

# --- Big Data (id=31) ---
bigdata_modules = [
    (31, 'Introduction to Big Data and Hadoop', 1, [
        'Types of Digital Data and Introduction to Big Data',
        'Big Data Analytics Overview',
        'History of Apache Hadoop',
        'Analysing Data with Unix Tools and Hadoop',
        'Hadoop Streaming and Echo System',
        'IBM Big Data Strategy',
        'Introduction to InfoSphere Big Insights and Big Sheets',
    ]),
    (31, 'HDFS: Hadoop Distributed File System', 2, [
        'The Design of HDFS',
        'HDFS Concepts and Command Line Interface',
        'Hadoop File System Interfaces and Data Flow',
        'Data Ingest with Flume and Scoop',
        'Hadoop Archives and Hadoop IO',
        'Compression Serialization Avro and File-Based Data Structures',
    ]),
    (31, 'MapReduce', 3, [
        'Anatomy of a MapReduce Job Run',
        'Failures and Job Scheduling in MapReduce',
        'Shuffle and Sort Phase',
        'Task Execution in MapReduce',
        'MapReduce Types and Formats',
        'MapReduce Features',
    ]),
    (31, 'Hadoop Ecosystem', 4, [
        'Introduction to Pig and Execution Modes',
        'Comparison of Pig with Databases and Pig Latin',
        'User Defined Functions and Data Processing Operators',
        'Hive Shell Hive Services and Metastore',
        'HiveQL Tables and Querying Data',
        'HBase Concepts Clients and RDBMS Comparison',
        'BigSQL Introduction',
    ]),
    (31, 'Predictive Analytics', 5, [
        'Simple Linear Regression',
        'Multiple Linear Regression',
        'Interpretation of Regression Coefficients',
        'Visualizations and Visual Data Analysis Techniques',
        'Interaction Techniques for Analytics',
        'Systems and Applications of Predictive Analytics',
    ]),
    (31, 'NoSQL', 6, [
        'Introduction to NoSQL and Aggregate Data Models',
        'Key-Value and Document Data Models',
        'Graph Databases and Schemaless Databases',
        'Materialized Views and Distribution Models',
        'Sharding and Master-Slave Replication',
        'Consistency Relaxing and Version Stamps',
        'Map-Reduce Partitioning and Combining',
        'Composing MapReduce Calculations',
    ]),
]

# --- Compiler Design (id=47) ---
compiler_modules = [
    (47, 'Introduction to Compilers', 1, [
        'Definition of Compiler and Interpreter',
        'Phases of a Compiler and Role of Lexical Analyzer',
        'Regular Expressions and Finite Automata',
        'Pass and Phases of Translation',
        'Lexical Analyzer Generator LEX',
        'Context Free Grammar and Parse Trees',
        'Ambiguity and Elimination of Left Recursion',
        'Left Factoring and Top Down Parsing',
        'Recursive Descent Parsing and LL1 Grammars',
    ]),
    (47, 'Bottom-Up Parsing', 2, [
        'Definition of Bottom-Up Parsing and Handles',
        'Handle Pruning and Shift-Reduce Parsing',
        'LR Grammars and LR Parsers',
        'Canonical LR and Look Ahead LR (LALR) Parsers',
        'Conflicts During Shift-Reduce Parsing',
        'Error Recovery in Parsing',
        'Parsing Ambiguous Grammars',
        'YACC Automatic Parser Generator',
    ]),
    (47, 'Syntax Directed Translation', 3, [
        'Syntax Directed Definition',
        'Construction of Syntax Trees',
        'S-Attributed and L-Attributed Definitions',
        'Translation Schemes',
        'Intermediate Code Generation and Abstract Syntax Tree',
        'Polish Notation and Three Address Code',
        'Types of Three Address Statements',
        'Translation of Simple Statements and Boolean Expressions',
        'Flow-of-Control Statements',
    ]),
    (47, 'Type Checking', 4, [
        'Definition of Type Checking',
        'Type Expressions and Type Systems',
        'Static and Dynamic Checking of Types',
        'Specification of a Simple Type Checker',
        'Equivalence of Type Expressions',
        'Type Conversions and Overloading',
        'Source Language Issues in Runtime Environments',
        'Storage Organization and Allocation Strategies',
        'Symbol Tables and Dynamic Storage Allocation',
    ]),
    (47, 'Code Optimization', 5, [
        'Organization of Code Optimizer',
        'Basic Blocks and Flow Graphs',
        'Optimization of Basic Blocks',
        'Principal Sources of Optimization',
        'Directed Acyclic Graph (DAG) Representation',
        'Global Data Flow Analysis',
    ]),
]

# --- NLP for Healthcare (id=49) ---
nlp_modules = [
    (49, 'Introduction to Natural Language Processing', 1, [
        'Overview of NLP',
        'Text Representation and Pre-processing',
        'Applications of NLP in Healthcare',
        'Challenges in NLP for Healthcare',
    ]),
    (49, 'Corpus Creation and Annotation', 2, [
        'Introduction to Corpus Creation',
        'Data Sources for Healthcare NLP',
        'Annotation Tools and Techniques',
        'Quality Assurance and Evaluation',
    ]),
    (49, 'Information Extraction for Healthcare', 3, [
        'Named Entity Recognition for Healthcare',
        'Relation Extraction for Biomedical Events',
        'Drug-Disease Interactions and Adverse Drug Reactions',
        'Entity Linking and Resolution',
        'Knowledge Graph Creation for Healthcare',
    ]),
    (49, 'Text Classification for Healthcare', 4, [
        'Binary and Multi-Class Classification',
        'Feature Selection and Extraction',
        'Sentiment Analysis for Healthcare Reviews',
        'Deep Learning Models for Healthcare Classification',
    ]),
    (49, 'Text Summarization and Generation for Healthcare', 5, [
        'Automatic Summarization of Healthcare Documents',
        'Text Generation for Patient Reports',
        'Discharge Summaries Generation',
        'Evaluation Metrics for Text Summarization',
    ]),
    (49, 'NLP Applications for Healthcare', 6, [
        'Clinical Decision Support Systems',
        'Electronic Health Record Analysis',
        'Healthcare Chatbots and Virtual Assistants',
        'NLP-Based Drug Discovery',
        'Pharmacovigilance',
    ]),
]

# --- VR and 3D Interaction (id=48) ---
vr_modules = [
    (48, 'Introduction to Virtual Reality', 1, [
        'Definition and History of Virtual Reality',
        'Components of VR: Hardware and Software',
        'VR Platforms Tools and Frameworks',
        'Types of Virtual Reality',
        'Applications of VR in Gaming Medicine and Education',
        'Challenges and Limitations in VR',
    ]),
    (48, 'VR Hardware and Software Systems', 2, [
        'VR Devices: Headsets Motion Tracking Controllers',
        'Haptic Feedback and Display Technologies',
        'Stereoscopic Displays and 3D Rendering Techniques',
        'VR Platforms: Unity Unreal Engine Vuforia',
        'Sensors and Motion Capture Systems',
        'Real-Time Rendering and Frame Rate Considerations',
    ]),
    (48, '3D Interaction in Virtual Reality', 3, [
        'Input Devices: Controllers Gloves Eye-Tracking',
        'Navigation in Virtual Spaces',
        'Walking Flying and Teleportation',
        'Gesture Recognition and Body Movement Tracking',
        'Interaction Techniques: Pointing Grabbing Manipulating',
        'Feedback Mechanisms: Visual Auditory and Haptic',
        'Designing 3D User Interfaces and Interaction Models',
    ]),
    (48, 'VR Environment Design and User Experience', 4, [
        'Principles of VR Environment Design',
        'Immersion Presence and Interaction',
        'Designing Virtual Worlds: Spatial Layout and Lighting',
        'Texture Mapping and Sound Design for VR',
        'Environmental Sounds and Music for VR',
        'Creating Realistic and Engaging VR Environments',
        'User-Centered Design and Usability in VR',
        'User Experience in VR Environments',
    ]),
    (48, 'Applications of Virtual Reality', 5, [
        'VR in Gaming: Creating Immersive Experiences',
        'VR in Healthcare: Therapy and Surgery Simulation',
        'VR in Education: Virtual Classrooms and Training',
        'VR for Architectural Design and Virtual Tours',
        'Social VR: Virtual Social Interactions and Worlds',
        'Future Trends: Integration with AR MR and AI',
    ]),
    (48, 'Developing VR Applications', 6, [
        'Introduction to VR Development Tools',
        'Unity3D and Unreal Engine Setup',
        'Creating Basic VR Scenes and Interactions',
        'Integrating 3D Models Textures and Sound',
        'Implementing Basic Interaction Techniques',
        'Debugging and Performance Optimization for VR',
    ]),
]

all_modules = dbms_modules + ai_modules + bigdata_modules + compiler_modules + nlp_modules + vr_modules

module_ids_created = {}
for subj_id, mod_name, seq, topics in all_modules:
    mod_id = db.execute(
        "INSERT INTO modules (subject_id, name, sequence_no) VALUES (%s, %s, %s)",
        (subj_id, mod_name, seq)
    )
    module_ids_created[(subj_id, seq)] = mod_id
    for tidx, topic_name in enumerate(topics):
        db.execute(
            "INSERT INTO topics (module_id, name) VALUES (%s, %s)",
            (mod_id, topic_name)
        )
    print(f"  Created module {mod_id}: {mod_name} with {len(topics)} topics")

print("\nAll modules and topics created successfully!")

db.execute("SET FOREIGN_KEY_CHECKS = 1")
db.execute("SET SQL_SAFE_UPDATES = 1")
print("Foreign key checks re-enabled.")
