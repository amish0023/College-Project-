#!/usr/bin/env python
"""Verify Semester 5 subjects and modules were added correctly"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from utils.database import fetch_all

# Get all Semester 5 subjects
sql = '''
SELECT s.name, s.code, COUNT(m.id) as module_count
FROM subjects s
LEFT JOIN modules m ON s.id = m.subject_id
WHERE s.id IN (
    SELECT subject_id FROM semester_subjects 
    WHERE semester_id = (SELECT id FROM semesters WHERE semester_number = 5)
)
GROUP BY s.id, s.name, s.code
ORDER BY s.name;
'''

results = fetch_all(sql)
print('=== SEMESTER 5 SUBJECTS AND MODULES ===\n')
for row in results:
    print(f'✓ {row["name"]} ({row["code"]}) - {row["module_count"]} modules')

print('\n=== MODULE DETAILS ===\n')

# Get all modules for the new subjects
for subject_name in ['Compiler Design', 'Introduction to Virtual Reality and 3D Gaming', 'NHRT', 'Big Data Analytics', 'Database Management Systems', 'Artificial Intelligence']:
    sql = '''
    SELECT m.name, m.sequence_no
    FROM modules m
    WHERE m.subject_id = (SELECT id FROM subjects WHERE name = %s)
    ORDER BY m.sequence_no;
    '''
    modules = fetch_all(sql, (subject_name,))
    if modules:
        print(f'📚 {subject_name}:')
        for mod in modules:
            print(f'   {mod["sequence_no"]}. {mod["name"]}')
        print()
