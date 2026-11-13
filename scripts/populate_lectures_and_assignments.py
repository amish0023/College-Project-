"""
Populate curated YouTube lectures, transcripts, AI notes, and adaptive assignments
for all 29 modules of the 5th semester subjects:
- Compiler Design (47)
- Artificial Intelligence (25)
- Big Data Analysis (31)
- NLP for Health Related Text (49)
- Introduction to Virtual Reality and 3D Interaction (48)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import database as db
from scripts.update_5th_sem_syllabus import SYLLABUS_DATA

def run():
    print("Beginning migration of curated YouTube lectures and adaptive assignments...")

    # Disable foreign key checks for clean update
    db.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.execute("SET SQL_SAFE_UPDATES = 0")

    # 1. Ensure Compiler Design has Module 1
    m1 = db.fetch_one("SELECT id FROM modules WHERE subject_id=47 AND sequence_no=1")
    if not m1:
        print("Recreating Compiler Design Module 1...")
        m1_id = db.execute(
            "INSERT INTO modules (subject_id, name, sequence_no, description) VALUES (47, %s, 1, %s)",
            ('Introduction to Compilers', 'Compiler vs Interpreter, phases of compiler, lexical analyzer, finite automata, parsing, LL(1)')
        )
        # Add topics for module 1
        m1_topics = [
            'Definition of compiler and interpreter and differences',
            'Phases of a compiler and translation passes',
            'Role of lexical analyzer and regular expressions',
            'Finite automata and Thompson construction',
            'Bootstrapping and LEX lexical analyzer generator',
            'Context free grammar parse trees and ambiguity',
            'Elimination of left recursion and left factoring',
            'Dangling-else ambiguity and predictive LL(1) parsing'
        ]
        for tname in m1_topics:
            db.execute("INSERT INTO topics (module_id, name, difficulty) VALUES (%s, %s, 'Medium')", (m1_id, tname))

    # 2. Build mapping of (subject_id, sequence_no) -> module_id
    rows = db.fetch_all("SELECT id, subject_id, sequence_no, name FROM modules WHERE subject_id IN (25, 31, 47, 48, 49)")
    mod_map = {(r['subject_id'], r['sequence_no']): r['id'] for r in rows}

    subject_id_map = {
        'Compiler Design': 47,
        'Artificial Intelligence': 25,
        'Big Data Analysis': 31,
        'NLP for Health Related Text': 49,
        'Introduction to Virtual Reality and 3D Interaction': 48,
    }

    total_lectures = 0
    total_assignments = 0
    total_questions = 0

    for sdata in SYLLABUS_DATA:
        sname = sdata['subject_name']
        sid = subject_id_map[sname]

        print(f"\nProcessing Subject: {sname} (ID: {sid})")

        for mdata in sdata['modules']:
            seq = mdata['seq']
            mid = mod_map.get((sid, seq))
            if not mid:
                print(f"  [WARN] Module seq {seq} not found for subject {sid}, skipping.")
                continue

            # Update module description and name
            db.execute(
                "UPDATE modules SET description=%s WHERE id=%s",
                (mdata['desc'], mid)
            )

            # Clean old lectures, transcripts, notes, assignments, questions for this module
            old_lecs = db.fetch_all("SELECT id FROM lectures WHERE module_id=%s", (mid,))
            for ol in old_lecs:
                lid = ol['id']
                db.execute("DELETE FROM lecture_progress WHERE lecture_id=%s", (lid,))
                db.execute("DELETE FROM transcripts WHERE lecture_id=%s", (lid,))
                db.execute("DELETE FROM lecture_notes WHERE lecture_id=%s", (lid,))
                db.execute("DELETE FROM lectures WHERE id=%s", (lid,))

            old_asg = db.fetch_all("SELECT id FROM assignments WHERE module_id=%s", (mid,))
            for oa in old_asg:
                aid = oa['id']
                db.execute("DELETE FROM assignment_answers WHERE attempt_id IN (SELECT id FROM assignment_attempts WHERE assignment_id=%s)", (aid,))
                db.execute("DELETE FROM assignment_attempts WHERE assignment_id=%s", (aid,))
                db.execute("DELETE FROM assignment_questions WHERE assignment_id=%s", (aid,))
                db.execute("DELETE FROM assignments WHERE id=%s", (aid,))

            # Insert curated lecture
            lec_id = db.execute(
                """INSERT INTO lectures (module_id, title, youtube_video_id, duration_seconds)
                   VALUES (%s, %s, %s, %s)""",
                (mid, mdata['video_title'], mdata['video_id'], mdata['duration'])
            )
            total_lectures += 1

            # Insert full transcript
            db.execute(
                "INSERT INTO transcripts (lecture_id, transcript_text) VALUES (%s, %s)",
                (lec_id, mdata['transcript'])
            )

            # Insert structured AI notes
            db.execute(
                """INSERT INTO lecture_notes 
                   (lecture_id, summary, key_concepts, important_points, revision_notes, possible_questions)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (lec_id, mdata['summary'], mdata['key_concepts'], mdata['important_points'], mdata['revision_notes'], mdata['possible_questions'])
            )

            # Insert adaptive assignment
            asg_id = db.execute(
                """INSERT INTO assignments (module_id, title, difficulty_mix)
                   VALUES (%s, %s, 'Adaptive (Easy, Medium, Hard)')""",
                (mid, f"{mdata['name']} Adaptive Assessment")
            )
            total_assignments += 1

            # Insert questions
            for q in mdata['questions']:
                if q['correct'] == 'A':
                    opt_a = q['a']
                    opt_b = q.get('b', 'Unrelated system process')
                    opt_c = q.get('c', 'Static hardware firmware allocation')
                    opt_d = q.get('d', 'None of the above')
                elif q['correct'] == 'B':
                    opt_a = q.get('a', 'Arbitrary transformation without evaluation')
                    opt_b = q['b']
                    opt_c = q.get('c', 'Deleting temporary local cache registers')
                    opt_d = q.get('d', 'None of the above')
                elif q['correct'] == 'C':
                    opt_a = q.get('a', 'Sequential buffer')
                    opt_b = q.get('b', 'Static hardware clock synchronization')
                    opt_c = q['c']
                    opt_d = q.get('d', 'None of the above')
                else:
                    opt_a = q.get('a', 'Option A')
                    opt_b = q.get('b', 'Option B')
                    opt_c = q.get('c', 'Option C')
                    opt_d = q.get('d', 'Correct D')

                db.execute(
                    """INSERT INTO assignment_questions 
                       (assignment_id, question_text, option_a, option_b, option_c, option_d, correct_option, difficulty, concept)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (asg_id, q['q'], opt_a, opt_b, opt_c, opt_d, q['correct'], q['diff'], mdata['name'])
                )
                total_questions += 1

            print(f"  -> Module {seq}: {mdata['name']} -> Lecture '{mdata['video_title']}' ({mdata['video_id']}) + Notes + 3 Questions")

    # 3. Ensure student topic performance records exist for all topics in active subjects
    for sid in [4, 3]:
        active_subs = db.fetch_all("SELECT subject_id, priority FROM student_subjects WHERE student_id=%s AND is_active=1", (sid,))
        for sub in active_subs:
            sub_topics = db.fetch_all(
                "SELECT t.id FROM topics t JOIN modules m ON m.id=t.module_id WHERE m.subject_id=%s",
                (sub['subject_id'],)
            )
            for top in sub_topics:
                db.execute(
                    """INSERT IGNORE INTO student_topic_performance 
                       (student_id, topic_id, quiz_score, accuracy, attempts, time_spent, previous_score, assignment_score, study_hours, difficulty, lecture_completion, improvement, mastery, priority_score, priority)
                       VALUES (%s, %s, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 'MODERATE', 50.0, %s)""",
                    (sid, top['id'], sub['priority'])
                )
        print(f"Synchronized topic performance for student {sid}")

    # Re-enable foreign key checks
    db.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.execute("SET SQL_SAFE_UPDATES = 1")

    print(f"\nMIGRATION COMPLETE!")
    print(f"Total Curated Lectures Added: {total_lectures}")
    print(f"Total Adaptive Assignments Added: {total_assignments}")
    print(f"Total MCQ Questions Added: {total_questions}")

    # 4. Regenerate adaptive plan for student 4
    from app import regenerate_adaptive_plan
    regenerate_adaptive_plan(4)
    print("Adaptive study plan successfully regenerated for student 4!")

if __name__ == '__main__':
    run()
