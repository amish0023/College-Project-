-- =========================================================
-- FIX: Properly map all 6 subjects to Semester 5
-- =========================================================

-- Remove old Semester 5 mappings that we want to replace
DELETE FROM semester_subjects 
WHERE semester_id = (SELECT id FROM semesters WHERE semester_number = 5)
AND subject_id IN (
    SELECT id FROM subjects WHERE name IN (
        'Machine Learning', 'Computer Networks', 'Advanced Database Systems',
        'Software Engineering', 'Web Development'
    )
);

-- Map the desired 6 subjects to Semester 5
INSERT INTO semester_subjects (semester_id, subject_id)
SELECT s.id, sub.id FROM semesters s, subjects sub
WHERE s.semester_number=5 AND sub.name IN (
    'Database Management Systems',
    'Big Data Analytics',
    'Artificial Intelligence',
    'Compiler Design',
    'Introduction to Virtual Reality and 3D Gaming',
    'NHRT'
) ON DUPLICATE KEY UPDATE semester_id=VALUES(semester_id);

-- =========================================================
-- VERIFY: Check Semester 5 now has the 6 subjects
-- =========================================================
SELECT CONCAT('✓ Added to Semester 5: ', s.name, ' (', s.code, ')') as status
FROM subjects s
WHERE s.id IN (
    SELECT subject_id FROM semester_subjects 
    WHERE semester_id = (SELECT id FROM semesters WHERE semester_number = 5)
)
ORDER BY s.name;
