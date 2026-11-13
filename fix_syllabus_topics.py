#!/usr/bin/env python
"""
Fix: Replace all old single topics with proper multi-topic structure for each module.
Also rebuild DBMS modules (only 1 module exists).
"""
from utils import database as db

db.execute("SET FOREIGN_KEY_CHECKS = 0")
db.execute("SET SQL_SAFE_UPDATES = 0")

# ============================================================
# STEP 1: Clean old topics, lectures, assignments for all 6 subjects
# ============================================================
for sid in [13, 25, 31, 47, 48, 49]:
    modules = db.fetch_all("SELECT id FROM modules WHERE subject_id=%s", (sid,))
    mids = [m['id'] for m in modules]
    if not mids:
        continue
    ph = ','.join(['%s'] * len(mids))
    # Clean assignments
    assigns = db.fetch_all(f"SELECT id FROM assignments WHERE module_id IN ({ph})", mids)
    aids = [a['id'] for a in assigns]
    if aids:
        aph = ','.join(['%s'] * len(aids))
        db.execute(f"DELETE FROM assignment_answers WHERE attempt_id IN (SELECT id FROM assignment_attempts WHERE assignment_id IN ({aph}))", aids)
        db.execute(f"DELETE FROM assignment_attempts WHERE assignment_id IN ({aph})", aids)
        db.execute(f"DELETE FROM assignment_questions WHERE assignment_id IN ({aph})", aids)
        db.execute(f"DELETE FROM assignments WHERE id IN ({aph})", aids)
    # Clean lectures
    lecs = db.fetch_all(f"SELECT id FROM lectures WHERE module_id IN ({ph})", mids)
    lids = [l['id'] for l in lecs]
    if lids:
        lph = ','.join(['%s'] * len(lids))
        db.execute(f"DELETE FROM lecture_progress WHERE lecture_id IN ({lph})", lids)
        db.execute(f"DELETE FROM transcripts WHERE lecture_id IN ({lph})", lids)
        db.execute(f"DELETE FROM lecture_notes WHERE lecture_id IN ({lph})", lids)
        db.execute(f"DELETE FROM lectures WHERE id IN ({lph})", lids)
    # Clean topics
    db.execute(f"DELETE FROM topics WHERE module_id IN ({ph})", mids)
    # Delete old modules and recreate
    db.execute(f"DELETE FROM modules WHERE id IN ({ph})", mids)
    print(f"Cleaned subject {sid}")

# ============================================================
# STEP 2: DBMS (13) - 6 modules with full topics
# ============================================================
dbms = [
    ('Introduction to Database Systems', 1, [
        'Database Systems Significance and Advantages',
        'Types of Databases and DBMS Environment',
        'Limitations of File Processing Systems',
        'Data Abstraction and Data Independence',
        'DBMS Architecture and Functions',
        'Formal Relational Query Languages',
        'Relational Algebra and Tuple Relational Calculus',
        'Domain Relational Calculus',
    ]),
    ('File Organization, Indexing and Hashing', 2, [
        'File Organization and Record Organization',
        'Data Dictionary Storage',
        'Basic Concepts of Indexing and Ordered Indices',
        'B+ Tree Index Files and Extensions',
        'Multiple Key Access',
        'Static and Dynamic Hashing',
        'Comparison of Indexing and Hashing',
        'Bitmap Index and Index Definition in SQL',
    ]),
    ('Data Models and Relational Database Design', 3, [
        'Evolution of Data Models',
        'Entity Relationship Model and ER Diagrams',
        'Extended Entity Relationship Model',
        'Relational Model and Logical View of Data',
        'Keys and Integrity Rules',
        'Relational Set Operators',
        'Database Normalization: 1NF 2NF 3NF BCNF 4NF 5NF',
        'Denormalization and Database Design',
    ]),
    ('Query Processing and Optimization', 4, [
        'Transaction Concept and Transaction Model',
        'Transaction Isolation Levels and Implementations',
        'Concurrency Controls and Lock Based Protocols',
        'Deadlock Handling and Time-stamp Based Protocols',
        'Validation Based Protocols',
        'Recovery System and Failure Classification',
        'Log Based Recovery and Advanced Recovery Techniques',
    ]),
    ('Transaction Management', 5, [
        'Graph Representation and Strongly Connected Components',
        'Traversal Methods: DFS and BFS',
        'Backtracking: 8-Queen Problem',
        'Backtracking: Knapsack Problem',
        'Branch and Bound: LC Searching and Bounding',
        'LC Branch and Bound Applications',
        '0/1 Knapsack and Travelling Salesman Problem',
    ]),
    ('SQL and Advanced SQL', 6, [
        'Introduction to SQL and SQL Data Definition',
        'Basic Structure of SQL Queries',
        'Set Operations and Null Values',
        'Aggregate Functions and Nested Sub-queries',
        'Modifications of Databases',
        'Join Expressions and Views',
        'Integrity Constraints and Schema Changes',
        'Authorization and Advanced SQL',
        'Dynamic SQL Embedded SQL Functions Procedures Triggers',
    ]),
]

# ============================================================
# STEP 3: AI (25) - 6 modules with full topics
# ============================================================
ai = [
    ('Introduction to Artificial Intelligence', 1, [
        'Definition and Future of Artificial Intelligence',
        'Characteristics of Intelligent Agents',
        'Typical Intelligent Agents and Problem Solving Approach',
    ]),
    ('Problem Solving Methods', 2, [
        'Problem Solving Methods and Search Strategies',
        'Uninformed Search Algorithms',
        'Informed Search and Heuristics',
        'Local Search Algorithms and Optimization',
        'Constraint Satisfaction Problems',
        'Constraint Propagation and Backtracking Search',
        'Game Playing and Alpha Beta Pruning',
        'Stochastic Games and Optimal Decisions',
    ]),
    ('Knowledge Representation', 3, [
        'First Order Predicate Logic',
        'Prolog Programming and Unification',
        'Forward Chaining and Backward Chaining',
        'Resolution and Knowledge Representation',
        'Ontological Engineering and Categories',
        'Reasoning Systems for Categories',
        'Reasoning with Default Information',
    ]),
    ('Software Agents', 4, [
        'Architecture for Intelligent Agents',
        'Agent Communication',
        'Negotiation Bargaining and Argumentation',
        'Trust and Reputation in Multi-Agent Systems',
    ]),
    ('Learning Processes', 5, [
        'Supervised Unsupervised and Reinforcement Learning',
        'Identifying the Type of Learning Process',
        'Uncertainty and Probability in AI',
        'Linear Regression and Support Vector Machine',
        'Decision Trees and Random Forest',
    ]),
    ('AI Applications', 6, [
        'Language Models and Information Retrieval',
        'Information Extraction and NLP',
        'Machine Translation and Speech Recognition',
        'Robot Hardware Perception and Planning',
    ]),
]

# ============================================================
# STEP 4: Big Data Analysis (31) - 6 modules
# ============================================================
bigdata = [
    ('Introduction to Big Data and Hadoop', 1, [
        'Types of Digital Data and Introduction to Big Data',
        'Big Data Analytics Overview',
        'History of Apache Hadoop',
        'Analysing Data with Unix Tools and Hadoop',
        'Hadoop Streaming and Echo System',
        'IBM Big Data Strategy',
    ]),
    ('HDFS: Hadoop Distributed File System', 2, [
        'Design of HDFS and HDFS Concepts',
        'Command Line Interface and Hadoop File System',
        'Data Flow and Data Ingest with Flume and Scoop',
        'Hadoop Archives and Hadoop IO',
        'Compression Serialization and Avro',
        'File-Based Data Structures',
    ]),
    ('MapReduce', 3, [
        'Anatomy of a MapReduce Job Run',
        'Failures and Job Scheduling',
        'Shuffle and Sort Phase',
        'Task Execution in MapReduce',
        'MapReduce Types and Formats',
        'MapReduce Features',
    ]),
    ('Hadoop Ecosystem', 4, [
        'Introduction to Pig and Execution Modes',
        'Pig Latin and Data Processing Operators',
        'Hive Shell Services and Metastore',
        'HiveQL Tables and Querying Data',
        'HBase Concepts and RDBMS Comparison',
        'BigSQL Introduction',
    ]),
    ('Predictive Analytics', 5, [
        'Simple Linear Regression',
        'Multiple Linear Regression',
        'Interpretation of Regression Coefficients',
        'Visualizations and Visual Data Analysis',
        'Interaction Techniques and Applications',
    ]),
    ('NoSQL', 6, [
        'Introduction to NoSQL and Aggregate Data Models',
        'Key-Value and Document Data Models',
        'Graph Databases and Schemaless Databases',
        'Materialized Views and Distribution Models',
        'Sharding and Replication',
        'MapReduce Partitioning and Combining',
    ]),
]

# ============================================================
# STEP 5: Compiler Design (47) - 5 modules
# ============================================================
compiler = [
    ('Introduction to Compilers', 1, [
        'Definition of Compiler and Interpreter',
        'Phases of a Compiler and Lexical Analyzer',
        'Regular Expressions and Finite Automata',
        'LEX Lexical Analyzer Generator',
        'Context Free Grammar and Parse Trees',
        'Elimination of Left Recursion and Left Factoring',
        'Top Down Parsing and LL1 Grammars',
        'Recursive Descent and Predictive Parsers',
    ]),
    ('Bottom-Up Parsing', 2, [
        'Bottom-Up Parsing and Handles',
        'Handle Pruning and Shift-Reduce Parsing',
        'LR Grammars and Simple LR Parsers',
        'Canonical LR and LALR Parsers',
        'Conflicts in Shift-Reduce Parsing',
        'Error Recovery in Parsing',
        'YACC Automatic Parser Generator',
    ]),
    ('Syntax Directed Translation', 3, [
        'Syntax Directed Definition',
        'Construction of Syntax Trees',
        'S-Attributed and L-Attributed Definitions',
        'Translation Schemes',
        'Intermediate Code Generation and AST',
        'Polish Notation and Three Address Code',
        'Translation of Statements and Boolean Expressions',
    ]),
    ('Type Checking', 4, [
        'Definition of Type Checking',
        'Type Expressions and Type Systems',
        'Static and Dynamic Checking of Types',
        'Specification of a Simple Type Checker',
        'Type Conversions and Overloading',
        'Runtime Environments and Storage Organization',
        'Symbol Tables and Dynamic Storage Allocation',
    ]),
    ('Code Optimization', 5, [
        'Organization of Code Optimizer',
        'Basic Blocks and Flow Graphs',
        'Optimization of Basic Blocks',
        'Principal Sources of Optimization',
        'DAG Representation of Basic Blocks',
        'Global Data Flow Analysis',
    ]),
]

# ============================================================
# STEP 6: NLP for Healthcare (49) - 6 modules
# ============================================================
nlp = [
    ('Introduction to Natural Language Processing', 1, [
        'Overview of NLP',
        'Text Representation and Pre-processing',
        'Applications of NLP in Healthcare',
        'Challenges in NLP for Healthcare',
    ]),
    ('Corpus Creation and Annotation', 2, [
        'Introduction to Corpus Creation',
        'Data Sources for Healthcare NLP',
        'Annotation Tools and Techniques',
        'Quality Assurance and Evaluation',
    ]),
    ('Information Extraction for Healthcare', 3, [
        'Named Entity Recognition for Healthcare',
        'Relation Extraction for Biomedical Events',
        'Drug-Disease Interactions and ADR',
        'Entity Linking and Resolution',
        'Knowledge Graph Creation for Healthcare',
    ]),
    ('Text Classification for Healthcare', 4, [
        'Binary and Multi-Class Classification',
        'Feature Selection and Extraction',
        'Sentiment Analysis for Healthcare Reviews',
        'Deep Learning Models for Healthcare Classification',
    ]),
    ('Text Summarization and Generation', 5, [
        'Automatic Summarization of Healthcare Documents',
        'Text Generation for Patient Reports',
        'Discharge Summaries Generation',
        'Evaluation Metrics for Text Summarization',
    ]),
    ('NLP Applications for Healthcare', 6, [
        'Clinical Decision Support Systems',
        'Electronic Health Record Analysis',
        'Healthcare Chatbots and Virtual Assistants',
        'NLP-Based Drug Discovery and Pharmacovigilance',
    ]),
]

# ============================================================
# STEP 7: VR and 3D Interaction (48) - 6 modules
# ============================================================
vr = [
    ('Introduction to Virtual Reality', 1, [
        'Definition and History of Virtual Reality',
        'Components of VR: Hardware and Software',
        'VR Platforms Tools and Frameworks',
        'Types of Virtual Reality: Immersive Non-Immersive AR',
        'Applications of VR in Gaming Medicine Education',
        'Challenges and Limitations in VR',
    ]),
    ('VR Hardware and Software Systems', 2, [
        'VR Devices: Headsets Motion Tracking Controllers',
        'Haptic Feedback and Display Technologies',
        'Stereoscopic Displays and 3D Rendering',
        'VR Platforms: Unity Unreal Engine Vuforia',
        'Sensors and Motion Capture Systems',
        'Real-Time Rendering and Frame Rate',
    ]),
    ('3D Interaction in Virtual Reality', 3, [
        'Input Devices: Controllers Gloves Eye-Tracking',
        'Navigation in Virtual Spaces',
        'Walking Flying and Teleportation',
        'Gesture Recognition and Body Movement',
        'Interaction Techniques: Pointing Grabbing Manipulating',
        'Feedback Mechanisms: Visual Auditory Haptic',
        'Designing 3D User Interfaces',
    ]),
    ('VR Environment Design and UX', 4, [
        'Principles of VR Environment Design',
        'Immersion Presence and Interaction',
        'Designing Virtual Worlds: Spatial Layout Lighting',
        'Texture Mapping and Sound Design for VR',
        'Creating Realistic VR Environments',
        'User-Centered Design and Usability in VR',
    ]),
    ('Applications of Virtual Reality', 5, [
        'VR in Gaming: Immersive Experiences',
        'VR in Healthcare: Therapy and Surgery Simulation',
        'VR in Education: Virtual Classrooms',
        'VR for Architectural Design and Virtual Tours',
        'Social VR: Virtual Social Interactions',
        'Future Trends: AR MR and AI Integration',
    ]),
    ('Developing VR Applications', 6, [
        'Introduction to VR Development Tools',
        'Unity3D and Unreal Engine Setup',
        'Creating Basic VR Scenes and Interactions',
        'Integrating 3D Models Textures and Sound',
        'Implementing Interaction Techniques in VR',
        'Debugging and Performance Optimization',
    ]),
]

# ============================================================
# INSERT ALL
# ============================================================
all_data = {
    13: dbms,
    25: ai,
    31: bigdata,
    47: compiler,
    49: nlp,
    48: vr,
}

for subj_id, modules_list in all_data.items():
    for mod_name, seq, topics in modules_list:
        mod_id = db.execute(
            "INSERT INTO modules (subject_id, name, sequence_no) VALUES (%s, %s, %s)",
            (subj_id, mod_name, seq)
        )
        for tname in topics:
            db.execute("INSERT INTO topics (module_id, name) VALUES (%s, %s)", (mod_id, tname))
        print(f"  [{subj_id}] Module {seq}: {mod_name} -> {len(topics)} topics")

db.execute("SET FOREIGN_KEY_CHECKS = 1")
db.execute("SET SQL_SAFE_UPDATES = 1")

# Summary
for sid in [13, 25, 31, 47, 48, 49]:
    mods = db.fetch_all("SELECT COUNT(*) as mc FROM modules WHERE subject_id=%s", (sid,))
    tcount = db.fetch_all(
        "SELECT COUNT(*) as tc FROM topics t JOIN modules m ON m.id=t.module_id WHERE m.subject_id=%s", (sid,)
    )
    print(f"Subject {sid}: {mods[0]['mc']} modules, {tcount[0]['tc']} topics")

print("\nDone! All syllabus modules and topics updated.")
