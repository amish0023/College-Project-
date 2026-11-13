-- =========================================================
-- SEMESTER 5 NEW SUBJECTS & MODULES
-- Add new subjects for Semester 5: DBMS, Big Data Analytics, 
-- Artificial Intelligence, Compiler Design, VR & 3D Gaming, NHRT
-- =========================================================

-- Step 1: Ensure all required subjects exist
INSERT INTO subjects (name, code, description) VALUES
('Compiler Design', 'CS505', 'Lexical analysis, parsing, semantic analysis, code generation, and optimization techniques.'),
('Introduction to Virtual Reality and 3D Gaming', 'CS506', 'VR fundamentals, 3D graphics, game engines, spatial computing, and interactive environments.'),
('NHRT', 'CS507', 'Advanced topics in networking, hardware architecture, and real-time systems integration.')
ON DUPLICATE KEY UPDATE description=VALUES(description);

-- Step 2: Map new subjects to Semester 5
INSERT INTO semester_subjects (semester_id, subject_id)
SELECT s.id, sub.id FROM semesters s, subjects sub
WHERE s.semester_number=5 AND sub.name IN (
    'DBMS',
    'Database Management Systems',
    'Big Data Analytics',
    'Artificial Intelligence',
    'Compiler Design',
    'Introduction to Virtual Reality and 3D Gaming',
    'NHRT'
) ON DUPLICATE KEY UPDATE semester_id=VALUES(semester_id);

-- =========================================================
-- MODULES FOR COMPILER DESIGN
-- =========================================================
INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Lexical Analysis & Tokenization', 1, 'Scanning phase, token recognition, symbol tables, and lexeme extraction.' FROM subjects WHERE name='Compiler Design'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Syntax Analysis & Parsing', 2, 'Context-free grammars, LL(1) and LR parsing, parse trees, and error recovery.' FROM subjects WHERE name='Compiler Design'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Semantic Analysis & Type Checking', 3, 'Abstract syntax trees, type systems, semantic validation, and attribute grammars.' FROM subjects WHERE name='Compiler Design'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Intermediate Code Generation', 4, 'Three-address code, DAG representation, symbol table management, and code translation.' FROM subjects WHERE name='Compiler Design'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Code Optimization', 5, 'Peephole optimization, loop optimization, constant folding, and register allocation.' FROM subjects WHERE name='Compiler Design'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Code Generation & Runtime', 6, 'Target code generation, assembly language, runtime environments, and linking.' FROM subjects WHERE name='Compiler Design'
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- =========================================================
-- MODULES FOR VIRTUAL REALITY & 3D GAMING
-- =========================================================
INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'VR Fundamentals & Hardware', 1, 'Head-mounted displays, tracking systems, motion controllers, and VR architectures.' FROM subjects WHERE name='Introduction to Virtual Reality and 3D Gaming'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, '3D Graphics & Rendering', 2, 'Coordinate systems, transformation matrices, lighting models, and shader programming.' FROM subjects WHERE name='Introduction to Virtual Reality and 3D Gaming'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Game Engine Architecture', 3, 'Scene graphs, physics engines, collision detection, and game loop design.' FROM subjects WHERE name='Introduction to Virtual Reality and 3D Gaming'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, '3D Modeling & Animation', 4, 'Mesh creation, skeletal animation, keyframe animation, and rigging.' FROM subjects WHERE name='Introduction to Virtual Reality and 3D Gaming'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Interactive VR Development', 5, 'User interaction, spatial UI, gesture recognition, and VR application design.' FROM subjects WHERE name='Introduction to Virtual Reality and 3D Gaming'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Game Design & Development Tools', 6, 'Unity/Unreal Engine, asset pipelines, debugging, and performance optimization.' FROM subjects WHERE name='Introduction to Virtual Reality and 3D Gaming'
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- =========================================================
-- MODULES FOR NHRT (Network Hardware & Real-Time Systems)
-- =========================================================
INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Network Hardware & Protocols', 1, 'Network interface cards, switching, routing hardware, and protocol implementation.' FROM subjects WHERE name='NHRT'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Real-Time System Principles', 2, 'Hard and soft real-time constraints, task scheduling, and deadline management.' FROM subjects WHERE name='NHRT'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Embedded Systems & IoT', 3, 'Microcontroller programming, sensor interfaces, and embedded real-time OS.' FROM subjects WHERE name='NHRT'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Real-Time Communication', 4, 'Time-synchronization, low-latency protocols, and deterministic networking.' FROM subjects WHERE name='NHRT'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Performance Analysis & Tuning', 5, 'Latency analysis, throughput optimization, and hardware utilization.' FROM subjects WHERE name='NHRT'
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- =========================================================
-- MODULES FOR BIG DATA ANALYTICS (if not already defined)
-- =========================================================
INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Big Data Fundamentals', 1, 'Volume, variety, velocity concepts, distributed computing, and data ecosystems.' FROM subjects WHERE name='Big Data Analytics'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Hadoop & MapReduce', 2, 'HDFS architecture, MapReduce programming, job scheduling, and cluster management.' FROM subjects WHERE name='Big Data Analytics'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Apache Spark', 3, 'RDD abstraction, DataFrames, Spark SQL, and distributed machine learning.' FROM subjects WHERE name='Big Data Analytics'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Data Processing & Pipelines', 4, 'ETL processes, data cleaning, stream processing, and event handling.' FROM subjects WHERE name='Big Data Analytics'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'NoSQL Databases', 5, 'Document stores, key-value stores, graph databases, and data modeling.' FROM subjects WHERE name='Big Data Analytics'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Analytics & Visualization', 6, 'Data aggregation, reporting, dashboard creation, and business intelligence.' FROM subjects WHERE name='Big Data Analytics'
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- =========================================================
-- MODULES FOR DATABASE MANAGEMENT SYSTEMS (DBMS) 
-- Assuming it refers to the existing subject, verify modules exist
-- =========================================================
-- If additional modules needed:
INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Distributed Databases', 5, 'Data partitioning, replication, consistency models, and CAP theorem.' FROM subjects WHERE name='Database Management Systems'
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- =========================================================
-- MODULES FOR ARTIFICIAL INTELLIGENCE (verify existing modules)
-- =========================================================
-- Additional AI modules if needed:
INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Machine Learning Integration', 3, 'Integration of ML algorithms with AI systems, learning from experience.' FROM subjects WHERE name='Artificial Intelligence'
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO modules (subject_id, name, sequence_no, description)
SELECT id, 'Expert Systems & Planning', 4, 'Rule-based systems, inference engines, planning algorithms, and goal-oriented search.' FROM subjects WHERE name='Artificial Intelligence'
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- =========================================================
-- Generate Topics for newly added modules
-- =========================================================
INSERT INTO topics (module_id, name, difficulty, description)
SELECT m.id, CONCAT(m.name, ' - Core Concepts'), 'Medium', CONCAT('Foundational understanding of ', m.name)
FROM modules m
WHERE m.id NOT IN (SELECT DISTINCT module_id FROM topics)
ON DUPLICATE KEY UPDATE difficulty=VALUES(difficulty);

-- =========================================================
-- UPDATE: Clarification for Semester 5 Configuration
-- =========================================================
-- Current Semester 5 subjects mapping has been updated.
-- All 6 requested subjects should now be available for Semester 5:
-- 1. Database Management Systems (DBMS)
-- 2. Big Data Analytics
-- 3. Artificial Intelligence
-- 4. Compiler Design (NEW)
-- 5. Introduction to Virtual Reality and 3D Gaming (NEW)
-- 6. NHRT (NEW)
