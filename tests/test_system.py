"""Comprehensive automated test suite for PERSONALISED LEARNING system."""
import unittest
import json
from app import app
from utils import database as db

class SystemTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True
        
        # Clean test user if exists
        cls.test_email = 'test_student_amish@university.edu'
        existing = db.fetch_one('SELECT id FROM students WHERE email=%s', (cls.test_email,))
        if existing:
            db.execute('DELETE FROM students WHERE id=%s', (existing['id'],))

    def test_01_registration(self):
        """Test registration with valid inputs."""
        res = self.client.post('/register', data={
            'full_name': 'Amish Sharma',
            'email': self.test_email,
            'password': 'password123',
            'confirm_password': 'password123',
            'roll_number': 'TEST-CSE-001'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Choose Your Semester', res.data)
        
        # Verify student exists in DB with current_semester NULL
        student = db.fetch_one('SELECT * FROM students WHERE email=%s', (self.test_email,))
        self.assertIsNotNone(student)
        self.assertEqual(student['full_name'], 'Amish Sharma')
        self.assertIsNone(student['current_semester'])

    def test_02_semester_validation_and_selection(self):
        """Test semester validation: reject 0, 9, -1, 'abc' and accept 1 to 8."""
        with self.client.session_transaction() as sess:
            student = db.fetch_one('SELECT id FROM students WHERE email=%s', (self.test_email,))
            sess['student_id'] = student['id']
            csrf = 'test-token'
            sess['_csrf'] = csrf

        # Test invalid semesters
        for invalid in ['0', '9', '-1', 'abc']:
            res = self.client.post('/select-semester', data={
                'semester': invalid,
                '_csrf': 'test-token'
            }, follow_redirects=True)
            self.assertIn(b'Invalid semester selection', res.data)

        # Test valid semester (e.g. Semester 2 for Data Structures)
        res = self.client.post('/select-semester', data={
            'semester': '2',
            '_csrf': 'test-token'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Customize Your Subjects', res.data)

        # Verify DB updated
        student = db.fetch_one('SELECT current_semester FROM students WHERE email=%s', (self.test_email,))
        self.assertEqual(student['current_semester'], 2)

    def test_03_semester_specific_subjects_and_customization(self):
        """Test that semester 2 displays Data Structures, and student can customize with priority."""
        with self.client.session_transaction() as sess:
            student = db.fetch_one('SELECT id FROM students WHERE email=%s', (self.test_email,))
            sess['student_id'] = student['id']
            sess['_csrf'] = 'test-token'

        # Get subjects for Sem 2
        res = self.client.get('/select-subjects')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Data Structures', res.data)

        # Find Data Structures ID
        ds_subj = db.fetch_one("SELECT id FROM subjects WHERE name='Data Structures'")
        self.assertIsNotNone(ds_subj)

        # Post customization with HIGH priority
        res = self.client.post('/select-subjects', data={
            'subjects': [str(ds_subj['id'])],
            f'priority_{ds_subj["id"]}': 'HIGH',
            '_csrf': 'test-token'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Learning Preferences', res.data)

        # Verify student_subjects in DB
        student = db.fetch_one('SELECT id FROM students WHERE email=%s', (self.test_email,))
        ss = db.fetch_one(
            'SELECT * FROM student_subjects WHERE student_id=%s AND subject_id=%s AND is_active=1',
            (student['id'], ds_subj['id'])
        )
        self.assertIsNotNone(ss)
        self.assertEqual(ss['priority'], 'HIGH')

    def test_04_onboarding_and_learning_target(self):
        """Test learning goals and preferences setup."""
        with self.client.session_transaction() as sess:
            student = db.fetch_one('SELECT id FROM students WHERE email=%s', (self.test_email,))
            sess['student_id'] = student['id']
            sess['_csrf'] = 'test-token'

        res = self.client.post('/onboarding', data={
            'learning_goal': 'Master Data Structures & Problem Solving',
            'target_date': '2026-12-31',
            'hours_per_week': '12',
            'preferred_days': ['Monday', 'Wednesday', 'Friday', 'Saturday'],
            'session_duration': '45',
            'learning_style': 'Video + Practice',
            '_csrf': 'test-token'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Personalised Learning', res.data)
        self.assertIn(b'Good', res.data)
        self.assertIn(b'Amish', res.data) # Displays actual authenticated student's name!

    def test_05_lecture_watch_tracking_and_assignment_locking(self):
        """
        Critical Business Rule Verification:
        1. Assignment is locked when lecture is NOT_STARTED.
        2. Direct URL access to assignment is blocked (HTTP 403).
        3. Video watch progress below 90% leaves assignment locked.
        4. When lecture reaches 90% and is marked complete, assignment unlocks.
        """
        student = db.fetch_one('SELECT id FROM students WHERE email=%s', (self.test_email,))
        sid = student['id']
        with self.client.session_transaction() as sess:
            sess['student_id'] = sid
            sess['_csrf'] = 'test-token'

        # Find Linked Lists module and assignment
        ds_subj = db.fetch_one("SELECT id FROM subjects WHERE name='Data Structures'")
        mod = db.fetch_one("SELECT id FROM modules WHERE subject_id=%s AND name='Linked Lists'", (ds_subj['id'],))
        lecture = db.fetch_one("SELECT id FROM lectures WHERE module_id=%s", (mod['id'],))
        assignment = db.fetch_one("SELECT id FROM assignments WHERE module_id=%s", (mod['id'],))

        self.assertIsNotNone(lecture)
        self.assertIsNotNone(assignment)

        # 1. Assignment is locked before watching
        res = self.client.get(f'/assignment/{assignment["id"]}')
        self.assertEqual(res.status_code, 403) # Strict backend enforcement!

        # 2. Watch 50% (300 seconds out of 600)
        res = self.client.post(f'/lecture/{lecture["id"]}/progress', json={
            'watched_seconds': 300,
            'duration_seconds': 600
        }, headers={'X-CSRF-Token': 'test-token'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['progress'], 50.0)
        self.assertEqual(data['status'], 'IN_PROGRESS')

        # Trying to complete before 90% must be rejected
        res = self.client.post(f'/lecture/{lecture["id"]}/complete', headers={'X-CSRF-Token': 'test-token'})
        self.assertEqual(res.status_code, 403)

        # Assignment still locked!
        res = self.client.get(f'/assignment/{assignment["id"]}')
        self.assertEqual(res.status_code, 403)

        # 3. Watch 95% (570 seconds out of 600)
        res = self.client.post(f'/lecture/{lecture["id"]}/progress', json={
            'watched_seconds': 570,
            'duration_seconds': 600
        }, headers={'X-CSRF-Token': 'test-token'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(data['progress'], 90.0)

        # 4. Mark complete on server
        res = self.client.post(f'/lecture/{lecture["id"]}/complete', headers={'X-CSRF-Token': 'test-token'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'COMPLETED')

        # 5. Assignment is now UNLOCKED!
        res = self.client.get(f'/assignment/{assignment["id"]}')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Linked Lists', res.data)

    def test_06_assignment_submission_and_adaptive_ml_loop(self):
        """
        Test assignment submission, ML model prediction, Explainable AI reasons,
        and automatic study plan update.
        """
        student = db.fetch_one('SELECT id FROM students WHERE email=%s', (self.test_email,))
        sid = student['id']
        with self.client.session_transaction() as sess:
            sess['student_id'] = sid
            sess['_csrf'] = 'test-token'

        ds_subj = db.fetch_one("SELECT id FROM subjects WHERE name='Data Structures'")
        mod = db.fetch_one("SELECT id FROM modules WHERE subject_id=%s AND name='Linked Lists'", (ds_subj['id'],))
        assignment = db.fetch_one("SELECT id FROM assignments WHERE module_id=%s", (mod['id'],))
        questions = db.fetch_all("SELECT * FROM assignment_questions WHERE assignment_id=%s", (assignment['id'],))

        # Submit answers (answering questions)
        form_data = {
            '_csrf': 'test-token',
            'time_spent_minutes': '8'
        }
        for q in questions:
            form_data[f'q_{q["id"]}'] = q['correct_option']

        res = self.client.post(f'/assignment/{assignment["id"]}/submit', data=form_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'100', res.data) # 100% score

        # Verify historical attempt is stored (Section 25)
        attempt = db.fetch_one('SELECT * FROM assignment_attempts WHERE student_id=%s AND assignment_id=%s', (sid, assignment['id']))
        self.assertIsNotNone(attempt)
        self.assertEqual(float(attempt['score']), 100.0)

        # Verify ML Topic Mastery is evaluated and stored
        topic = db.fetch_one('SELECT id FROM topics WHERE module_id=%s', (mod['id'],))
        perf = db.fetch_one('SELECT * FROM student_topic_performance WHERE student_id=%s AND topic_id=%s', (sid, topic['id']))
        self.assertIsNotNone(perf)
        self.assertIn(perf['mastery'], ['STRONG', 'MODERATE', 'WEAK'])

        # Verify AI study tasks were generated
        tasks = db.fetch_all("SELECT * FROM study_tasks WHERE student_id=%s AND source='AI' AND status='PENDING'", (sid,))
        self.assertGreater(len(tasks), 0)

    def test_07_weekly_report_generation(self):
        """Test weekly report aggregation and insight generation."""
        student = db.fetch_one('SELECT id FROM students WHERE email=%s', (self.test_email,))
        sid = student['id']
        with self.client.session_transaction() as sess:
            sess['student_id'] = sid
            sess['_csrf'] = 'test-token'

        res = self.client.post('/weekly-report/generate', data={'_csrf': 'test-token'}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Weekly Performance Report', res.data)
        self.assertIn(b'AI Performance Insights', res.data)

        # Verify report exists in DB
        report = db.fetch_one('SELECT * FROM weekly_reports WHERE student_id=%s', (sid,))
        self.assertIsNotNone(report)
        self.assertGreater(len(report['insights']), 10)

    def test_08_todo_task_management(self):
        """Test adding, completing, and deleting to-do tasks."""
        student = db.fetch_one('SELECT id FROM students WHERE email=%s', (self.test_email,))
        sid = student['id']
        with self.client.session_transaction() as sess:
            sess['student_id'] = sid
            sess['_csrf'] = 'test-token'

        # Add custom task
        res = self.client.post('/todo', data={
            'title': 'Test LeetCode Tree Practice',
            'description': 'Solve 5 binary tree problems',
            'priority': 'HIGH',
            'duration': '45',
            'due_date': '2026-09-05',
            '_csrf': 'test-token'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Test LeetCode Tree Practice', res.data)

        task = db.fetch_one("SELECT * FROM study_tasks WHERE student_id=%s AND title='Test LeetCode Tree Practice'", (sid,))
        self.assertIsNotNone(task)
        self.assertEqual(task['status'], 'PENDING')

        # Complete task
        res = self.client.post(f'/todo/{task["id"]}/complete', data={'_csrf': 'test-token'}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        completed_task = db.fetch_one('SELECT * FROM study_tasks WHERE id=%s', (task['id'],))
        self.assertEqual(completed_task['status'], 'COMPLETED')

        # Delete task
        res = self.client.post(f'/todo/{task["id"]}/delete', data={'_csrf': 'test-token'}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        deleted_task = db.fetch_one('SELECT * FROM study_tasks WHERE id=%s', (task['id'],))
        self.assertIsNone(deleted_task)

    def test_09_semester_change_preserves_history(self):
        """
        Section 46: When semester changes, confirm change, update semester,
        load new semester subjects, prompt customization, PRESERVE old performance history.
        """
        student = db.fetch_one('SELECT id FROM students WHERE email=%s', (self.test_email,))
        sid = student['id']
        with self.client.session_transaction() as sess:
            sess['student_id'] = sid
            sess['_csrf'] = 'test-token'

        # Initial attempts count
        attempts_before = db.fetch_all('SELECT id FROM assignment_attempts WHERE student_id=%s', (sid,))
        self.assertGreater(len(attempts_before), 0)

        # Switch from Semester 2 to Semester 5
        res = self.client.post('/change-semester', data={
            'semester': '5',
            '_csrf': 'test-token'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Semester 5', res.data)
        self.assertIn(b'Compiler Design', res.data)

        # Verify historical attempts are NOT deleted!
        attempts_after = db.fetch_all('SELECT id FROM assignment_attempts WHERE student_id=%s', (sid,))
        self.assertEqual(len(attempts_before), len(attempts_after))

        # Verify student semester is updated
        updated_student = db.fetch_one('SELECT current_semester FROM students WHERE id=%s', (sid,))
        self.assertEqual(updated_student['current_semester'], 5)

if __name__ == '__main__':
    unittest.main()
