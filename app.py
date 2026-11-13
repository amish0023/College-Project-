"""PERSONALISED LEARNING
AI-Based Personalized Learning System for Student Performance Analysis and Adaptive Study Plan Generation
"""

#import os
import secrets
from datetime import date, datetime, timedelta
from flask import (
    Flask, render_template, request, redirect, url_for, session,
    flash, jsonify, abort
)
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from utils import database as db
from utils.auth import login_required, owns_subject
from utils.mastery import predict_mastery, calculate_priority, explain_priority
from utils.recommendations import build_recommendations
from utils.study_planner import make_weekly_plan
from utils.analytics import generate_weekly_insights

app = Flask(__name__)
app.config.from_object(Config)

# ---------------------------------------------------------
# CSRF PROTECTION & SECURITY HEADERS
# ---------------------------------------------------------
def csrf_token():
    if '_csrf' not in session:
        session['_csrf'] = secrets.token_urlsafe(24)
    return session['_csrf']

app.jinja_env.globals['csrf_token'] = csrf_token

@app.before_request
def csrf_guard():
    if request.method == 'POST' and request.endpoint not in {'login', 'register', 'lecture_progress'}:
        token = request.form.get('_csrf') or request.headers.get('X-CSRF-Token')
        if not token or token != session.get('_csrf'):
            abort(400, 'Invalid or missing CSRF security token.')

@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# ---------------------------------------------------------
# STUDENT HELPERS & DATA ISOLATION
# ---------------------------------------------------------
def current_student():
    sid = session.get('student_id')
    if not sid:
        return None
    return db.fetch_one('SELECT * FROM students WHERE id=%s', (sid,))

def current_preferences():
    sid = session.get('student_id')
    if not sid:
        return None
    return db.fetch_one('SELECT * FROM student_preferences WHERE student_id=%s', (sid,))

def student_topic_rows(student_id=None):
    sid = student_id or session.get('student_id')
    if not sid:
        return []
    sql = """
        SELECT stp.*, t.id AS topic_id, t.name AS topic_name, m.id AS module_id, m.name AS module_name,
               s.id AS subject_id, s.name AS subject_name, ss.priority AS subject_priority
        FROM student_topic_performance stp
        JOIN topics t ON t.id = stp.topic_id
        JOIN modules m ON m.id = t.module_id
        JOIN subjects s ON s.id = m.subject_id
        JOIN student_subjects ss ON ss.subject_id = s.id AND ss.student_id = stp.student_id
        WHERE stp.student_id = %s AND ss.is_active = 1
        ORDER BY stp.priority_score DESC
    """
    return db.fetch_all(sql, (sid,))

def get_greeting(name):
    hour = datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    return f"{greeting}, {name} 👋"

@app.context_processor
def inject_globals():
    student = current_student()
    greeting = get_greeting(student['full_name'].split()[0]) if student else "Welcome 👋"
    return {
        'current_student': student,
        'student_greeting': greeting,
        'now_year': datetime.now().year
    }

# ---------------------------------------------------------
# ADAPTIVE REGENERATION LOOP
# ---------------------------------------------------------
def regenerate_adaptive_plan(student_id):
    """
    Core adaptive loop:
    Evaluates latest student topic performance, generates tailored AI recommendations,
    and updates the dynamic study plan and to-do tasks.
    """
    pref = db.fetch_one('SELECT * FROM student_preferences WHERE student_id=%s', (student_id,))
    if not pref:
        return
        
    topic_rows = student_topic_rows(student_id)
    if not topic_rows:
        # If student has selected subjects but no topic rows yet, initialize them
        initialize_student_topics(student_id)
        topic_rows = student_topic_rows(student_id)
        
    days_left = (pref['target_date'] - date.today()).days if pref.get('target_date') else None
    recommendations = build_recommendations(topic_rows, pref.get('hours_per_week', 10), days_left)
    
    # Store recommendations in database
    db.execute('DELETE FROM recommendations WHERE student_id=%s', (student_id,))
    for rec in recommendations:
        db.execute(
            """INSERT INTO recommendations (student_id, subject_id, topic_id, priority, priority_score, reason, activity, duration)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (student_id, rec['subject_id'], rec['topic_id'], rec['priority'], rec['priority_score'], rec['reason'], rec['activity'], rec['duration'])
        )
        
    # Mark old AI pending tasks as SUPERSEDED
    db.execute(
        "UPDATE study_tasks SET status='SUPERSEDED' WHERE student_id=%s AND source='AI' AND status='PENDING'",
        (student_id,)
    )
    
    # Generate new schedule
    new_plan_tasks = make_weekly_plan(
        recommendations,
        pref.get('preferred_days'),
        pref.get('session_duration'),
        pref.get('hours_per_week')
    )
    
    for task in new_plan_tasks:
        db.execute(
            """INSERT INTO study_tasks (student_id, subject_id, topic_id, title, description, priority, duration, due_date, status, source)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'PENDING', 'AI')""",
            (student_id, task['subject_id'], task['topic_id'], task['title'], task['description'], task['priority'], task['duration'], task['due_date'])
        )

def initialize_student_topics(student_id):
    """Initializes baseline performance rows for newly customized subjects."""
    selected_subjects = db.fetch_all(
        'SELECT subject_id, priority FROM student_subjects WHERE student_id=%s AND is_active=1',
        (student_id,)
    )
    for subj in selected_subjects:
        topics = db.fetch_all(
            'SELECT t.id FROM topics t JOIN modules m ON m.id = t.module_id WHERE m.subject_id=%s',
            (subj['subject_id'],)
        )
        for t in topics:
            db.execute(
                """INSERT IGNORE INTO student_topic_performance 
                   (student_id, topic_id, quiz_score, accuracy, attempts, time_spent, previous_score, assignment_score, study_hours, difficulty, lecture_completion, improvement, mastery, priority_score, priority)
                   VALUES (%s, %s, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 'MODERATE', 50.0, %s)""",
                (student_id, t['id'], subj['priority'])
            )

# ---------------------------------------------------------
# AUTHENTICATION & LOGIN FLOW
# ---------------------------------------------------------
@app.route('/')
def index():
    if session.get('student_id'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('student_id'):
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        roll_number = request.form.get('roll_number', '').strip() or None
        
        if len(full_name) < 2:
            flash('Please enter your full name.', 'danger')
        elif not email or '@' not in email:
            flash('Please enter a valid email address.', 'danger')
        elif len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match.', 'danger')
        elif db.fetch_one('SELECT id FROM students WHERE email=%s', (email,)):
            flash('An account with this email already exists.', 'danger')
        else:
            hashed = generate_password_hash(password)
            sid = db.execute(
                'INSERT INTO students (full_name, email, password_hash, roll_number) VALUES (%s, %s, %s, %s)',
                (full_name, email, hashed, roll_number)
            )
            session.clear()
            session['student_id'] = sid
            csrf_token()
            flash('Welcome to Personalised Learning! Please choose your semester to get started.', 'success')
            return redirect(url_for('select_semester'))
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('student_id'):
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        student = db.fetch_one('SELECT * FROM students WHERE email=%s', (email,))
        if student and check_password_hash(student['password_hash'], password):
            session.clear()
            session['student_id'] = student['id']
            csrf_token()
            
            # Step 1: Check semester
            if student['current_semester'] is None:
                return redirect(url_for('select_semester'))
                
            # Step 2: Check subjects
            has_subjects = db.fetch_one(
                'SELECT 1 FROM student_subjects WHERE student_id=%s AND is_active=1',
                (student['id'],)
            )
            if not has_subjects:
                return redirect(url_for('select_subjects'))
                
            # Step 3: Check preferences
            pref = db.fetch_one('SELECT 1 FROM student_preferences WHERE student_id=%s', (student['id'],))
            if not pref:
                return redirect(url_for('onboarding'))
                
            return redirect(url_for('dashboard'))
            
        flash('Invalid email address or password.', 'danger')
        
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('You have been securely logged out.', 'info')
    return redirect(url_for('login'))

# ---------------------------------------------------------
# ONBOARDING FLOW: SEMESTER & SUBJECT CUSTOMIZATION
# ---------------------------------------------------------
@app.route('/select-semester', methods=['GET', 'POST'])
@login_required
def select_semester():
    student = current_student()
    if request.method == 'POST':
        semester_val = request.form.get('semester')
        
        # Strict backend validation (Section 7)
        if not semester_val or not semester_val.isdigit() or int(semester_val) not in range(1, 9):
            flash('Invalid semester selection. Choose between Semester 1 and 8.', 'danger')
            return redirect(url_for('select_semester'))
            
        sem_num = int(semester_val)
        db.execute('UPDATE students SET current_semester=%s WHERE id=%s', (sem_num, session['student_id']))
        flash(f'Semester {sem_num} selected successfully! Now customize your subjects.', 'success')
        return redirect(url_for('select_subjects'))
        
    semesters = db.fetch_all('SELECT * FROM semesters ORDER BY semester_number')
    return render_template('select_semester.html', semesters=semesters, current_sem=student.get('current_semester'))

@app.route('/select-subjects', methods=['GET', 'POST'])
@login_required
def select_subjects():
    student = current_student()
    sem_num = student.get('current_semester')
    if not sem_num:
        flash('Please choose your semester first.', 'warning')
        return redirect(url_for('select_semester'))
        
    if request.method == 'POST':
        selected_ids = request.form.getlist('subjects')
        if not selected_ids:
            flash('Please select at least one subject to focus on.', 'warning')
            return redirect(url_for('select_subjects'))
            
        # Deactivate previous active subjects for this student
        db.execute('UPDATE student_subjects SET is_active=0 WHERE student_id=%s', (session['student_id'],))
        
        for sub_id in selected_ids:
            priority = request.form.get(f'priority_{sub_id}', 'MEDIUM')
            if priority not in {'HIGH', 'MEDIUM', 'LOW'}:
                priority = 'MEDIUM'
            db.execute(
                """INSERT INTO student_subjects (student_id, subject_id, priority, is_active)
                   VALUES (%s, %s, %s, 1)
                   ON DUPLICATE KEY UPDATE is_active=1, priority=VALUES(priority)""",
                (session['student_id'], int(sub_id), priority)
            )
            
        initialize_student_topics(session['student_id'])
        
        pref = current_preferences()
        if not pref:
            flash('Subjects saved! Now let us customize your study goals and preferences.', 'success')
            return redirect(url_for('onboarding'))
        else:
            regenerate_adaptive_plan(session['student_id'])
            flash('Subjects customized successfully! Your adaptive plan has been refreshed.', 'success')
            return redirect(url_for('dashboard'))
            
    # Fetch semester subjects
    semester_row = db.fetch_one('SELECT id FROM semesters WHERE semester_number=%s', (sem_num,))
    subjects = []
    if semester_row:
        subjects = db.fetch_all(
            """SELECT s.* FROM subjects s
               JOIN semester_subjects ss ON ss.subject_id = s.id
               WHERE ss.semester_id = %s ORDER BY s.name""",
            (semester_row['id'],)
        )
        
    student_sub_rows = db.fetch_all(
        'SELECT subject_id, priority FROM student_subjects WHERE student_id=%s AND is_active=1',
        (session['student_id'],)
    )
    current_selected = {row['subject_id']: row['priority'] for row in student_sub_rows}
    
    return render_template('select_subjects.html', semester_num=sem_num, subjects=subjects, current_selected=current_selected)

@app.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    if request.method == 'POST':
        goal = request.form.get('learning_goal', '').strip()
        target_date_val = request.form.get('target_date', '')
        hours = request.form.get('hours_per_week', 10)
        days = request.form.getlist('preferred_days')
        duration = request.form.get('session_duration', 45)
        learning_style = request.form.get('learning_style', 'Balanced')
        
        if not goal or not target_date_val:
            flash('Please specify both your learning goal and target completion date.', 'danger')
            return redirect(url_for('onboarding'))
            
        try:
            target_date = datetime.strptime(target_date_val, '%Y-%m-%d').date()
            if target_date <= date.today():
                flash('Target date must be in the future.', 'warning')
                return redirect(url_for('onboarding'))
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('onboarding'))
            
        preferred_days_str = ",".join(days) if days else "Monday,Wednesday,Friday"
        
        db.execute(
            """INSERT INTO student_preferences (student_id, learning_goal, target_date, hours_per_week, preferred_days, session_duration, learning_style)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE 
                 learning_goal=VALUES(learning_goal),
                 target_date=VALUES(target_date),
                 hours_per_week=VALUES(hours_per_week),
                 preferred_days=VALUES(preferred_days),
                 session_duration=VALUES(session_duration),
                 learning_style=VALUES(learning_style)""",
            (session['student_id'], goal, target_date, int(hours), preferred_days_str, int(duration), learning_style)
        )
        
        regenerate_adaptive_plan(session['student_id'])
        flash('Preferences saved! Welcome to your personalized dashboard.', 'success')
        return redirect(url_for('dashboard'))
        
    pref = current_preferences()
    return render_template('onboarding.html', pref=pref)

# ---------------------------------------------------------
# DASHBOARD & PROFILE
# ---------------------------------------------------------
@app.route('/dashboard')
@login_required
def dashboard():
    student = current_student()
    if not student.get('current_semester'):
        return redirect(url_for('select_semester'))
        
    pref = current_preferences()
    if not pref:
        return redirect(url_for('onboarding'))
        
    sid = session['student_id']
    topic_rows = student_topic_rows(sid)
    
    # Days until target
    days_remaining = None
    if pref.get('target_date'):
        days_remaining = max(0, (pref['target_date'] - date.today()).days)
        
    # Aggregate Stats
    attempt_stats = db.fetch_one(
        """SELECT COUNT(*) AS total_attempts,
                  COALESCE(ROUND(AVG(accuracy), 1), 0.0) AS avg_accuracy,
                  COALESCE(ROUND(AVG(score), 1), 0.0) AS avg_score
           FROM assignment_attempts WHERE student_id=%s""",
        (sid,)
    )
    
    lecture_stats = db.fetch_one(
        "SELECT COUNT(*) AS completed_lectures FROM lecture_progress WHERE student_id=%s AND status='COMPLETED'",
        (sid,)
    )
    
    study_hours_data = db.fetch_one(
        "SELECT COALESCE(ROUND(SUM(time_spent_minutes)/60.0, 1), 0.0) AS total_hours FROM assignment_attempts WHERE student_id=%s",
        (sid,)
    )
    
    # Recommendations
    recommendations = db.fetch_all(
        """SELECT r.*, t.name AS topic_name, s.name AS subject_name
           FROM recommendations r
           JOIN topics t ON t.id = r.topic_id
           JOIN subjects s ON s.id = r.subject_id
           WHERE r.student_id=%s ORDER BY r.priority_score DESC LIMIT 4""",
        (sid,)
    )
    
    # Pending tasks for today/upcoming
    today = date.today()
    tasks = db.fetch_all(
        """SELECT * FROM study_tasks 
           WHERE student_id=%s AND status='PENDING' 
           ORDER BY due_date ASC, priority='HIGH' DESC LIMIT 6""",
        (sid,)
    )
    
    # Mastery counts
    strong_topics = [t for t in topic_rows if t.get('mastery') == 'STRONG']
    moderate_topics = [t for t in topic_rows if t.get('mastery') == 'MODERATE']
    weak_topics = [t for t in topic_rows if t.get('mastery') == 'WEAK']
    
    # Chart.js Data
    # 1. Performance trend (last 7 attempts)
    recent_attempts = db.fetch_all(
        """SELECT aa.score, aa.accuracy, DATE_FORMAT(aa.submitted_at, '%%b %%d') AS submit_date
           FROM assignment_attempts aa
           WHERE aa.student_id=%s
           ORDER BY aa.submitted_at ASC LIMIT 7""",
        (sid,)
    )
    
    # 2. Subject Performance
    subject_perf = db.fetch_all(
        """SELECT s.name, COALESCE(ROUND(AVG(stp.accuracy), 1), 0) AS avg_acc
           FROM student_subjects ss
           JOIN subjects s ON s.id = ss.subject_id
           LEFT JOIN modules m ON m.subject_id = s.id
           LEFT JOIN topics t ON t.module_id = m.id
           LEFT JOIN student_topic_performance stp ON stp.topic_id = t.id AND stp.student_id = ss.student_id
           WHERE ss.student_id=%s AND ss.is_active=1
           GROUP BY s.id, s.name""",
        (sid,)
    )
    
    return render_template(
        'dashboard.html',
        student=student,
        pref=pref,
        days_remaining=days_remaining,
        attempt_stats=attempt_stats,
        lecture_stats=lecture_stats,
        study_hours_data=study_hours_data,
        recommendations=recommendations,
        tasks=tasks,
        strong_topics=strong_topics,
        moderate_topics=moderate_topics,
        weak_topics=weak_topics,
        recent_attempts=recent_attempts,
        subject_perf=subject_perf
    )

@app.route('/profile')
@login_required
def profile():
    student = current_student()
    pref = current_preferences()
    student_subjects = db.fetch_all(
        """SELECT s.*, ss.priority
           FROM student_subjects ss
           JOIN subjects s ON s.id = ss.subject_id
           WHERE ss.student_id=%s AND ss.is_active=1""",
        (session['student_id'],)
    )
    return render_template('profile.html', student=student, pref=pref, subjects=student_subjects)

@app.route('/profile/update', methods=['POST'])
@login_required
def profile_update():
    goal = request.form.get('learning_goal', '').strip()
    target_date_val = request.form.get('target_date', '')
    hours = request.form.get('hours_per_week', 10)
    duration = request.form.get('session_duration', 45)
    learning_style = request.form.get('learning_style', 'Balanced')
    days = request.form.getlist('preferred_days')
    
    if goal and target_date_val:
        try:
            target_date = datetime.strptime(target_date_val, '%Y-%m-%d').date()
            preferred_days_str = ",".join(days) if days else "Monday,Wednesday,Friday"
            db.execute(
                """UPDATE student_preferences 
                   SET learning_goal=%s, target_date=%s, hours_per_week=%s, session_duration=%s, learning_style=%s, preferred_days=%s
                   WHERE student_id=%s""",
                (goal, target_date, int(hours), int(duration), learning_style, preferred_days_str, session['student_id'])
            )
            regenerate_adaptive_plan(session['student_id'])
            flash('Profile updated successfully!', 'success')
        except ValueError:
            flash('Invalid date format.', 'danger')
    return redirect(url_for('profile'))

@app.route('/change-semester', methods=['GET', 'POST'])
@login_required
def change_semester():
    """
    Section 46: Changing semester updates semester and prompts subject customization
    while strictly PRESERVING previous historical performance.
    """
    if request.method == 'POST':
        semester_val = request.form.get('semester')
        if not semester_val or not semester_val.isdigit() or int(semester_val) not in range(1, 9):
            flash('Please choose a valid semester (1–8).', 'danger')
            return redirect(url_for('change_semester'))
            
        sem_num = int(semester_val)
        db.execute('UPDATE students SET current_semester=%s WHERE id=%s', (sem_num, session['student_id']))
        # Archive previous active subjects (preserve history)
        db.execute('UPDATE student_subjects SET is_active=0 WHERE student_id=%s', (session['student_id'],))
        flash(f'Switched to Semester {sem_num}. Please select your subjects for this semester.', 'success')
        return redirect(url_for('select_subjects'))
        
    student = current_student()
    semesters = db.fetch_all('SELECT * FROM semesters ORDER BY semester_number')
    return render_template('change_semester.html', semesters=semesters, current_sem=student.get('current_semester'))

# ---------------------------------------------------------
# SUBJECTS & MODULES
# ---------------------------------------------------------
@app.route('/subjects')
@login_required
def subjects():
    student = current_student()
    sid = session['student_id']
    items = db.fetch_all(
        """SELECT s.*, ss.priority,
                  COUNT(DISTINCT m.id) AS total_modules,
                  ROUND(COALESCE(AVG(lp.progress_percentage), 0.0), 1) AS progress
           FROM student_subjects ss
           JOIN subjects s ON s.id = ss.subject_id
           LEFT JOIN modules m ON m.subject_id = s.id
           LEFT JOIN lectures l ON l.module_id = m.id
           LEFT JOIN lecture_progress lp ON lp.lecture_id = l.id AND lp.student_id = ss.student_id
           WHERE ss.student_id=%s AND ss.is_active=1
           GROUP BY s.id, ss.priority
           ORDER BY ss.priority='HIGH' DESC, s.name ASC""",
        (sid,)
    )
    return render_template('subjects.html', subjects=items, current_sem=student.get('current_semester'))

@app.route('/subjects/<int:subject_id>')
@login_required
def subject_detail(subject_id):
    sid = session['student_id']
    subject = db.fetch_one('SELECT * FROM subjects WHERE id=%s', (subject_id,))
    if not subject:
        abort(404)
        
    modules = db.fetch_all(
        'SELECT * FROM modules WHERE subject_id=%s ORDER BY sequence_no ASC',
        (subject_id,)
    )
    
    for m in modules:
        # Fetch bifurcated topic lectures with student watch progress
        m['topics'] = db.fetch_all("""
            SELECT t.id AS topic_id, t.name AS topic_name, t.difficulty,
                   l.id AS lecture_id, l.title AS lecture_title, l.youtube_video_id, l.duration_seconds,
                   COALESCE(lp.status, 'NOT_STARTED') AS watch_status,
                   COALESCE(lp.progress_percentage, 0.0) AS watch_progress
            FROM topics t
            LEFT JOIN lectures l ON l.topic_id = t.id
            LEFT JOIN lecture_progress lp ON lp.lecture_id = l.id AND lp.student_id = %s
            WHERE t.module_id = %s
            ORDER BY t.id ASC
        """, (sid, m['id']))
        
        # Check module assignment
        asg = db.fetch_one('SELECT * FROM assignments WHERE module_id=%s', (m['id'],))
        m['assignment'] = asg
        m['assignment_id'] = asg['id'] if asg else None
        
        # Check if assignment is unlocked (any lecture completed in module)
        has_completed_lec = any(top['watch_status'] == 'COMPLETED' for top in m['topics'])
        if not has_completed_lec:
            master_comp = db.fetch_one("""
                SELECT 1 FROM lecture_progress lp
                JOIN lectures l ON l.id = lp.lecture_id
                WHERE lp.student_id=%s AND l.module_id=%s AND lp.status='COMPLETED'
                LIMIT 1
            """, (sid, m['id']))
            has_completed_lec = bool(master_comp)
        m['assignment_unlocked'] = has_completed_lec
        
        if m['topics']:
            comp_count = sum(1 for top in m['topics'] if top['watch_status'] == 'COMPLETED')
            avg_pct = sum(float(top['watch_progress']) for top in m['topics']) / len(m['topics'])
            m['completed_topics'] = comp_count
            m['total_topics'] = len(m['topics'])
            m['watch_progress'] = round(avg_pct, 1)
            m['lecture_status'] = 'COMPLETED' if comp_count == len(m['topics']) else ('IN_PROGRESS' if comp_count > 0 or avg_pct > 0 else 'NOT_STARTED')
            # Use first topic lecture ID as quick entry if module clicked
            m['first_lecture_id'] = m['topics'][0]['lecture_id'] if m['topics'] else None
        else:
            m['completed_topics'] = 0
            m['total_topics'] = 0
            m['watch_progress'] = 0.0
            m['lecture_status'] = 'NOT_STARTED'
            m['first_lecture_id'] = None

    is_enrolled = owns_subject(subject_id, sid, db)
    return render_template('subject_detail.html', subject=subject, modules=modules, is_enrolled=is_enrolled)

@app.route('/subjects/add', methods=['POST'])
@login_required
def add_subject():
    sub_id = request.form.get('subject_id')
    priority = request.form.get('priority', 'MEDIUM')
    if sub_id and sub_id.isdigit():
        db.execute(
            """INSERT INTO student_subjects (student_id, subject_id, priority, is_active)
               VALUES (%s, %s, %s, 1)
               ON DUPLICATE KEY UPDATE is_active=1, priority=VALUES(priority)""",
            (session['student_id'], int(sub_id), priority)
        )
        initialize_student_topics(session['student_id'])
        regenerate_adaptive_plan(session['student_id'])
        flash('Subject added to your active curriculum.', 'success')
    return redirect(url_for('subjects'))

@app.route('/subjects/remove/<int:subject_id>', methods=['POST'])
@login_required
def remove_subject(subject_id):
    db.execute(
        'UPDATE student_subjects SET is_active=0 WHERE student_id=%s AND subject_id=%s',
        (session['student_id'], subject_id)
    )
    regenerate_adaptive_plan(session['student_id'])
    flash('Subject removed from active list.', 'info')
    return redirect(url_for('subjects'))

@app.route('/modules/<int:module_id>')
@login_required
def module(module_id):
    sid = session['student_id']
    mod = db.fetch_one("""
        SELECT m.*, s.name AS subject_name, s.id AS subject_id
        FROM modules m
        JOIN subjects s ON s.id = m.subject_id
        WHERE m.id = %s
    """, (module_id,))
    if not mod:
        abort(404)
        
    topic_lectures = db.fetch_all("""
        SELECT t.id AS topic_id, t.name AS topic_name, t.difficulty,
               l.id AS lecture_id, l.title AS lecture_title, l.youtube_video_id, l.duration_seconds,
               COALESCE(lp.status, 'NOT_STARTED') AS watch_status,
               COALESCE(lp.progress_percentage, 0.0) AS watch_progress
        FROM topics t
        LEFT JOIN lectures l ON l.topic_id = t.id
        LEFT JOIN lecture_progress lp ON lp.lecture_id = l.id AND lp.student_id = %s
        WHERE t.module_id = %s
        ORDER BY t.id ASC
    """, (sid, module_id))
    
    asg = db.fetch_one('SELECT * FROM assignments WHERE module_id=%s', (module_id,))
    has_completed_lec = any(tl['watch_status'] == 'COMPLETED' for tl in topic_lectures)
    if not has_completed_lec:
        master_comp = db.fetch_one("""
            SELECT 1 FROM lecture_progress lp
            JOIN lectures l ON l.id = lp.lecture_id
            WHERE lp.student_id=%s AND l.module_id=%s AND lp.status='COMPLETED'
            LIMIT 1
        """, (sid, module_id))
        has_completed_lec = bool(master_comp)
        
    total_topics = len(topic_lectures)
    comp_topics = sum(1 for tl in topic_lectures if tl['watch_status'] == 'COMPLETED')
    overall_progress = round(sum(float(tl['watch_progress']) for tl in topic_lectures) / total_topics, 1) if total_topics else 0.0
    
    return render_template(
        'module.html',
        module=mod,
        topic_lectures=topic_lectures,
        assignment=asg,
        assignment_unlocked=has_completed_lec,
        total_topics=total_topics,
        comp_topics=comp_topics,
        overall_progress=overall_progress
    )

# ---------------------------------------------------------
# LECTURES & WATCH PROGRESS TRACKING
# ---------------------------------------------------------
@app.route('/lecture/<int:lecture_id>')
@login_required
def lecture(lecture_id):
    sid = session['student_id']
    row = db.fetch_one("""
        SELECT l.*, m.id AS module_id, m.name AS module_name, m.sequence_no AS module_seq,
               s.id AS subject_id, s.name AS subject_name,
               t.id AS topic_id, COALESCE(t.name, l.title) AS topic_name,
               COALESCE(lp.status, 'NOT_STARTED') AS watch_status,
               COALESCE(lp.progress_percentage, 0.0) AS watch_progress,
               COALESCE(lp.watched_seconds, 0.0) AS watched_seconds
        FROM lectures l
        JOIN modules m ON m.id = l.module_id
        JOIN subjects s ON s.id = m.subject_id
        LEFT JOIN topics t ON t.id = l.topic_id
        LEFT JOIN lecture_progress lp ON lp.lecture_id = l.id AND lp.student_id = %s
        WHERE l.id = %s
    """, (sid, lecture_id))
    if not row:
        abort(404)
        
    transcript = db.fetch_one('SELECT * FROM transcripts WHERE lecture_id=%s', (lecture_id,))
    notes = db.fetch_one('SELECT * FROM lecture_notes WHERE lecture_id=%s', (lecture_id,))
    assignment = db.fetch_one('SELECT * FROM assignments WHERE module_id=%s', (row['module_id'],))
    
    sibling_lectures = db.fetch_all("""
        SELECT l.id, l.title, t.name AS topic_name,
               COALESCE(lp.status, 'NOT_STARTED') AS watch_status
        FROM lectures l
        JOIN topics t ON t.id = l.topic_id
        LEFT JOIN lecture_progress lp ON lp.lecture_id = l.id AND lp.student_id = %s
        WHERE l.module_id = %s
        ORDER BY t.id ASC
    """, (sid, row['module_id']))
    
    prev_lec = None
    next_lec = None
    for idx, sl in enumerate(sibling_lectures):
        if sl['id'] == lecture_id:
            if idx > 0:
                prev_lec = sibling_lectures[idx - 1]
            if idx < len(sibling_lectures) - 1:
                next_lec = sibling_lectures[idx + 1]
            break
            
    # Check if assignment unlocked (completed this lecture or any in module)
    assignment_unlocked = (row['watch_status'] == 'COMPLETED')
    if not assignment_unlocked:
        comp_check = db.fetch_one("""
            SELECT 1 FROM lecture_progress lp
            JOIN lectures l ON l.id = lp.lecture_id
            WHERE lp.student_id=%s AND l.module_id=%s AND lp.status='COMPLETED'
            LIMIT 1
        """, (sid, row['module_id']))
        assignment_unlocked = bool(comp_check)
    
    return render_template(
        'lecture.html',
        lecture=row,
        transcript=transcript,
        notes=notes,
        assignment=assignment,
        assignment_unlocked=assignment_unlocked,
        prev_lecture=prev_lec,
        next_lecture=next_lec,
        sibling_lectures=sibling_lectures
    )

@app.route('/lecture/<int:lecture_id>/progress', methods=['POST'])
@login_required
def lecture_progress(lecture_id):
    """
    Live watch tracking endpoint invoked by YouTube IFrame API.
    Section 19: Tracks started_at, last_watched_at, watched_seconds, progress_percentage, completion_status.
    """
    sid = session['student_id']
    data = request.get_json(silent=True) or {}
    watched = max(0.0, float(data.get('watched_seconds', 0.0)))
    duration = float(data.get('duration_seconds', 600.0))
    
    pct = min(100.0, round((watched / duration) * 100.0, 1)) if duration > 0 else 0.0
    status = 'COMPLETED' if pct >= 90.0 else ('IN_PROGRESS' if watched > 0 else 'NOT_STARTED')
    
    db.execute(
        """INSERT INTO lecture_progress (student_id, lecture_id, started_at, last_watched_at, watched_seconds, progress_percentage, status)
           VALUES (%s, %s, NOW(), NOW(), %s, %s, %s)
           ON DUPLICATE KEY UPDATE 
             last_watched_at = NOW(),
             watched_seconds = GREATEST(watched_seconds, VALUES(watched_seconds)),
             progress_percentage = GREATEST(progress_percentage, VALUES(progress_percentage)),
             status = IF(status='COMPLETED', 'COMPLETED', VALUES(status))""",
        (sid, lecture_id, watched, pct, status)
    )
    
    # Update topic performance lecture completion
    lecture_row = db.fetch_one('SELECT module_id, topic_id FROM lectures WHERE id=%s', (lecture_id,))
    if lecture_row and lecture_row['topic_id']:
        db.execute(
            """UPDATE student_topic_performance 
               SET lecture_completion=GREATEST(lecture_completion, %s)
               WHERE student_id=%s AND topic_id=%s""",
            (pct, sid, lecture_row['topic_id'])
        )
    elif lecture_row:
        topic_row = db.fetch_one('SELECT id FROM topics WHERE module_id=%s', (lecture_row['module_id'],))
        if topic_row:
            db.execute(
                """UPDATE student_topic_performance 
                   SET lecture_completion=GREATEST(lecture_completion, %s)
                   WHERE student_id=%s AND topic_id=%s""",
                (pct, sid, topic_row['id'])
            )
            
    return jsonify({'success': True, 'progress': pct, 'status': status})

@app.route('/lecture/<int:lecture_id>/complete', methods=['POST'])
@login_required
def complete_lecture(lecture_id):
    """
    Section 19 & 20: Completion is enforced on server:
    Cannot complete unless recorded watch percentage >= 90%.
    """
    sid = session['student_id']
    prog = db.fetch_one(
        'SELECT progress_percentage FROM lecture_progress WHERE student_id=%s AND lecture_id=%s',
        (sid, lecture_id)
    )
    if not prog or prog['progress_percentage'] < 90.0:
        return jsonify({
            'success': False,
            'error': 'You must watch at least 90% of the lecture video before marking it as complete.'
        }), 403
        
    db.execute(
        """UPDATE lecture_progress 
           SET status='COMPLETED', progress_percentage=100.0, completed_at=NOW() 
           WHERE student_id=%s AND lecture_id=%s""",
        (sid, lecture_id)
    )
    
    # Update topic performance
    lecture_row = db.fetch_one('SELECT module_id, topic_id FROM lectures WHERE id=%s', (lecture_id,))
    if lecture_row and lecture_row['topic_id']:
        db.execute(
            """UPDATE student_topic_performance 
               SET lecture_completion=100.0 
               WHERE student_id=%s AND topic_id=%s""",
            (sid, lecture_row['topic_id'])
        )
    elif lecture_row:
        topic_row = db.fetch_one('SELECT id FROM topics WHERE module_id=%s', (lecture_row['module_id'],))
        if topic_row:
            db.execute(
                """UPDATE student_topic_performance 
                   SET lecture_completion=100.0 
                   WHERE student_id=%s AND topic_id=%s""",
                (sid, topic_row['id'])
            )
            
    return jsonify({'success': True, 'status': 'COMPLETED'})

@app.route('/lecture/<int:lecture_id>/transcript')
@login_required
def lecture_transcript(lecture_id):
    transcript = db.fetch_one('SELECT * FROM transcripts WHERE lecture_id=%s', (lecture_id,))
    return jsonify(transcript or {'transcript_text': 'No transcript available.'})

@app.route('/lecture/<int:lecture_id>/notes')
@login_required
def lecture_notes_json(lecture_id):
    notes = db.fetch_one('SELECT * FROM lecture_notes WHERE lecture_id=%s', (lecture_id,))
    return jsonify(notes or {})

# ---------------------------------------------------------
# ASSIGNMENTS (STRICT BACKEND LOCKING + ADAPTIVE EVALUATION)
# ---------------------------------------------------------
def get_verified_assignment(assignment_id, student_id):
    """
    Critical business rule (Section 20):
    Assignment is LOCKED if lecture is NOT_STARTED or IN_PROGRESS.
    Unlocked ONLY if at least one lecture in the module is COMPLETED.
    """
    assignment = db.fetch_one(
        """SELECT a.*, m.name AS module_name, m.subject_id, s.name AS subject_name,
                  (SELECT t.id FROM topics t WHERE t.module_id=m.id ORDER BY t.id ASC LIMIT 1) AS topic_id,
                  (SELECT t.name FROM topics t WHERE t.module_id=m.id ORDER BY t.id ASC LIMIT 1) AS topic_name
           FROM assignments a
           JOIN modules m ON m.id = a.module_id
           JOIN subjects s ON s.id = m.subject_id
           WHERE a.id = %s""",
        (assignment_id,)
    )
    if not assignment:
        abort(404, 'Assignment not found.')
        
    # Backend lock check: checks if student completed ANY lecture for this module
    progress = db.fetch_one(
        """SELECT 1 FROM lecture_progress lp
           JOIN lectures l ON l.id = lp.lecture_id
           WHERE lp.student_id=%s AND l.module_id=%s AND lp.status='COMPLETED'
           LIMIT 1""",
        (student_id, assignment['module_id'])
    )
    if not progress:
        abort(403, 'Assignment is locked! You must complete at least one topic lecture in this module first.')
        
    return assignment

@app.route('/assignment/<int:assignment_id>')
@login_required
def assignment(assignment_id):
    sid = session['student_id']
    assignment_data = get_verified_assignment(assignment_id, sid)
    
    # Adaptive question selection considering student topic performance (Section 23)
    perf = db.fetch_one(
        'SELECT mastery FROM student_topic_performance WHERE student_id=%s AND topic_id=%s',
        (sid, assignment_data['topic_id'])
    )
    mastery_state = perf['mastery'] if perf else 'MODERATE'
    
    questions = db.fetch_all(
        'SELECT id, assignment_id, question_text, option_a, option_b, option_c, option_d, difficulty, concept FROM assignment_questions WHERE assignment_id=%s ORDER BY id ASC',
        (assignment_id,)
    )
    
    return render_template(
        'assignment.html',
        assignment=assignment_data,
        questions=questions,
        mastery=mastery_state
    )

@app.route('/assignment/<int:assignment_id>/submit', methods=['POST'])
@login_required
def submit_assignment(assignment_id):
    sid = session['student_id']
    assignment_data = get_verified_assignment(assignment_id, sid)
    
    questions = db.fetch_all(
        'SELECT * FROM assignment_questions WHERE assignment_id=%s',
        (assignment_id,)
    )
    if not questions:
        flash('No questions found in this assignment.', 'danger')
        return redirect(url_for('dashboard'))
        
    correct_count = 0
    submitted_answers = {}
    
    for q in questions:
        selected = request.form.get(f'q_{q["id"]}')
        is_corr = (selected == q['correct_option'])
        if is_corr:
            correct_count += 1
        submitted_answers[q['id']] = {
            'selected': selected,
            'is_correct': is_corr,
            'correct_option': q['correct_option'],
            'explanation': f"Concept: {q['concept']} ({q['difficulty']})"
        }
        
    total_questions = len(questions)
    incorrect_count = total_questions - correct_count
    accuracy = round((correct_count / total_questions) * 100.0, 2) if total_questions > 0 else 0.0
    score = accuracy
    time_spent = max(1, int(request.form.get('time_spent_minutes', 5)))
    
    # 1. Store attempt (NEVER overwrite historical performance - Section 25)
    attempt_id = db.execute(
        """INSERT INTO assignment_attempts 
           (student_id, assignment_id, score, accuracy, correct_answers, incorrect_answers, time_spent_minutes)
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (sid, assignment_id, score, accuracy, correct_count, incorrect_count, time_spent)
    )
    
    # 2. Store individual answers
    for q_id, ans in submitted_answers.items():
        db.execute(
            """INSERT INTO assignment_answers (attempt_id, question_id, selected_option, is_correct)
               VALUES (%s, %s, %s, %s)""",
            (attempt_id, q_id, ans['selected'], ans['is_correct'])
        )
        
    # 3. Retrieve historical topic metrics for ML feature engineering
    topic_id = assignment_data['topic_id']
    prev_perf = db.fetch_one(
        'SELECT * FROM student_topic_performance WHERE student_id=%s AND topic_id=%s',
        (sid, topic_id)
    )
    
    past_attempts = int(prev_perf['attempts']) + 1 if prev_perf else 1
    previous_score = float(prev_perf['assignment_score']) if prev_perf and prev_perf['assignment_score'] > 0 else score
    improvement = round(score - previous_score, 2)
    tot_time = float(prev_perf['time_spent'] if prev_perf else 0.0) + time_spent
    study_hours = round(tot_time / 60.0, 2)
    
    # Compile the exact 10 features for ML model (Section 26)
    metrics = {
        'quiz_score': score,
        'accuracy': accuracy,
        'attempts': past_attempts,
        'time_spent': time_spent,
        'previous_score': previous_score,
        'assignment_score': score,
        'study_hours': study_hours,
        'difficulty': 2,
        'lecture_completion': 100.0,
        'improvement': improvement
    }
    
    # Real ML prediction (Section 27)
    predicted_mastery = predict_mastery(metrics)
    priority_score, priority_level = calculate_priority(metrics)
    
    # 4. Upsert student_topic_performance
    db.execute(
        """INSERT INTO student_topic_performance 
           (student_id, topic_id, quiz_score, accuracy, attempts, time_spent, previous_score, assignment_score, study_hours, difficulty, lecture_completion, improvement, mastery, priority_score, priority)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 2, 100.0, %s, %s, %s, %s)
           ON DUPLICATE KEY UPDATE 
             quiz_score = VALUES(quiz_score),
             accuracy = ROUND((accuracy * (attempts) + VALUES(accuracy)) / (attempts + 1), 2),
             attempts = attempts + 1,
             time_spent = time_spent + VALUES(time_spent),
             previous_score = assignment_score,
             assignment_score = VALUES(assignment_score),
             study_hours = study_hours + VALUES(study_hours),
             improvement = VALUES(improvement),
             mastery = VALUES(mastery),
             priority_score = VALUES(priority_score),
             priority = VALUES(priority)""",
        (sid, topic_id, score, accuracy, past_attempts, time_spent, previous_score, score, study_hours, improvement, predicted_mastery, priority_score, priority_level)
    )
    
    # 5. Core Adaptive Loop: Update recommendations & regenerate future study plan (Section 34)
    regenerate_adaptive_plan(sid)
    
    flash(f'Assignment submitted! Your score: {score:.1f}%. Topic Mastery evaluated as: {predicted_mastery}.', 'success')
    return redirect(url_for('assignment_result', attempt_id=attempt_id))

@app.route('/assignment-result/<int:attempt_id>')
@login_required
def assignment_result(attempt_id):
    sid = session['student_id']
    attempt = db.fetch_one(
        """SELECT aa.*, a.title AS assignment_title, m.name AS module_name, s.name AS subject_name,
                  t.name AS topic_name, stp.mastery, stp.priority
           FROM assignment_attempts aa
           JOIN assignments a ON a.id = aa.assignment_id
           JOIN modules m ON m.id = a.module_id
           JOIN subjects s ON s.id = m.subject_id
           JOIN topics t ON t.module_id = m.id
           LEFT JOIN student_topic_performance stp ON stp.student_id = aa.student_id AND stp.topic_id = t.id
           WHERE aa.id=%s AND aa.student_id=%s""",
        (attempt_id, sid)
    )
    if not attempt:
        abort(404)
        
    answers = db.fetch_all(
        """SELECT ans.*, q.question_text, q.option_a, q.option_b, q.option_c, q.option_d, q.correct_option, q.difficulty, q.concept
           FROM assignment_answers ans
           JOIN assignment_questions q ON q.id = ans.question_id
           WHERE ans.attempt_id=%s ORDER BY q.id ASC""",
        (attempt_id,)
    )
    
    return render_template('assignment_result.html', attempt=attempt, answers=answers)

# ---------------------------------------------------------
# PERFORMANCE & EXPLAINABLE AI RECOMMENDATIONS
# ---------------------------------------------------------
@app.route('/performance')
@login_required
def performance():
    sid = session['student_id']
    rows = student_topic_rows(sid)
    
    overall = db.fetch_one(
        """SELECT COUNT(*) AS total_attempts,
                  COALESCE(ROUND(AVG(accuracy), 1), 0.0) AS avg_accuracy,
                  COALESCE(ROUND(AVG(score), 1), 0.0) AS avg_score,
                  COALESCE(ROUND(SUM(time_spent_minutes)/60.0, 1), 0.0) AS total_study_hours
           FROM assignment_attempts WHERE student_id=%s""",
        (sid,)
    )
    
    attempts_history = db.fetch_all(
        """SELECT aa.*, a.title AS assignment_title, m.name AS module_name, s.name AS subject_name
           FROM assignment_attempts aa
           JOIN assignments a ON a.id = aa.assignment_id
           JOIN modules m ON m.id = a.module_id
           JOIN subjects s ON s.id = m.subject_id
           WHERE aa.student_id=%s
           ORDER BY aa.submitted_at DESC LIMIT 15""",
        (sid,)
    )
    
    return render_template(
        'performance.html',
        rows=rows,
        overall=overall,
        attempts=attempts_history
    )

@app.route('/weak-topics')
@login_required
def weak_topics():
    sid = session['student_id']
    rows = [r for r in student_topic_rows(sid) if r.get('mastery') == 'WEAK' or r.get('priority') == 'HIGH']
    return jsonify(rows)

@app.route('/recommendations')
@login_required
def recommendations():
    sid = session['student_id']
    pref = current_preferences()
    rows = student_topic_rows(sid)
    days_left = (pref['target_date'] - date.today()).days if pref and pref.get('target_date') else None
    
    recs = build_recommendations(rows, pref.get('hours_per_week', 10) if pref else 10, days_left)
    return render_template('recommendations.html', recommendations=recs, pref=pref)

# ---------------------------------------------------------
# ADAPTIVE STUDY PLAN & TO-DO LIST
# ---------------------------------------------------------
@app.route('/study-plan')
@login_required
def study_plan():
    sid = session['student_id']
    today = date.today()
    
    tasks = db.fetch_all(
        """SELECT st.*, s.name AS subject_name, t.name AS topic_name
           FROM study_tasks st
           LEFT JOIN subjects s ON s.id = st.subject_id
           LEFT JOIN topics t ON t.id = st.topic_id
           WHERE st.student_id=%s AND st.status IN ('PENDING', 'COMPLETED')
           ORDER BY st.due_date ASC, st.priority='HIGH' DESC""",
        (sid,)
    )
    
    today_tasks = [t for t in tasks if t['due_date'] == today]
    this_week_tasks = [t for t in tasks if today < t['due_date'] <= today + timedelta(days=7)]
    upcoming_tasks = [t for t in tasks if t['due_date'] > today + timedelta(days=7)]
    
    pref = current_preferences()
    return render_template(
        'study_plan.html',
        today_tasks=today_tasks,
        this_week_tasks=this_week_tasks,
        upcoming_tasks=upcoming_tasks,
        pref=pref
    )

@app.route('/study-plan/generate', methods=['POST'])
@login_required
def generate_study_plan():
    regenerate_adaptive_plan(session['student_id'])
    flash('Adaptive study plan regenerated with latest ML mastery and priority evidence.', 'success')
    return redirect(url_for('study_plan'))

@app.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    sid = session['student_id']
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'MEDIUM')
        duration = request.form.get('duration', 30)
        due_date_val = request.form.get('due_date') or str(date.today())
        
        if title:
            db.execute(
                """INSERT INTO study_tasks (student_id, title, description, priority, duration, due_date, status, source)
                   VALUES (%s, %s, %s, %s, %s, %s, 'PENDING', 'MANUAL')""",
                (sid, title, description, priority, int(duration), due_date_val)
            )
            flash('Task added to your To-Do list.', 'success')
        return redirect(url_for('todo'))
        
    tasks = db.fetch_all(
        'SELECT * FROM study_tasks WHERE student_id=%s AND status IN (\'PENDING\', \'COMPLETED\') ORDER BY due_date ASC, priority=\'HIGH\' DESC',
        (sid,)
    )
    return render_template('todo.html', tasks=tasks, today=date.today())

@app.route('/todo/add', methods=['POST'])
@login_required
def add_todo():
    return todo()

@app.route('/todo/<int:task_id>/complete', methods=['POST'])
@login_required
def complete_todo(task_id):
    db.execute(
        "UPDATE study_tasks SET status='COMPLETED', completed_at=NOW() WHERE id=%s AND student_id=%s",
        (task_id, session['student_id'])
    )
    flash('Task marked as completed! Keep up the momentum.', 'success')
    return redirect(request.referrer or url_for('todo'))

@app.route('/todo/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_todo(task_id):
    db.execute(
        'DELETE FROM study_tasks WHERE id=%s AND student_id=%s',
        (task_id, session['student_id'])
    )
    flash('Task removed.', 'info')
    return redirect(request.referrer or url_for('todo'))

# ---------------------------------------------------------
# WEEKLY REPORT
# ---------------------------------------------------------
@app.route('/weekly-report')
@login_required
def weekly_report():
    sid = session['student_id']
    report = db.fetch_one(
        'SELECT * FROM weekly_reports WHERE student_id=%s ORDER BY week_start DESC LIMIT 1',
        (sid,)
    )
    past_reports = db.fetch_all(
        'SELECT * FROM weekly_reports WHERE student_id=%s ORDER BY week_start DESC LIMIT 5',
        (sid,)
    )
    return render_template('weekly_report.html', report=report, past_reports=past_reports)

@app.route('/weekly-report/generate', methods=['POST'])
@login_required
def generate_weekly_report():
    sid = session['student_id']
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Calculate stats for the week
    week_attempts = db.fetch_one(
        """SELECT COUNT(*) AS assignments_completed,
                  COALESCE(ROUND(AVG(accuracy), 1), 0.0) AS average_accuracy,
                  COALESCE(ROUND(AVG(score), 1), 0.0) AS overall_score,
                  COALESCE(ROUND(SUM(time_spent_minutes)/60.0, 1), 0.0) AS study_hours
           FROM assignment_attempts
           WHERE student_id=%s AND DATE(submitted_at) BETWEEN %s AND %s""",
        (sid, start_of_week, end_of_week)
    )
    
    lectures_completed_row = db.fetch_one(
        """SELECT COUNT(*) AS total
           FROM lecture_progress
           WHERE student_id=%s AND status='COMPLETED' AND DATE(completed_at) BETWEEN %s AND %s""",
        (sid, start_of_week, end_of_week)
    )
    
    stats = {
        'assignments_completed': week_attempts['assignments_completed'] or 0,
        'average_accuracy': week_attempts['average_accuracy'] or 0.0,
        'overall_score': week_attempts['overall_score'] or 0.0,
        'study_hours': week_attempts['study_hours'] or 0.0,
        'lectures_completed': lectures_completed_row['total'] or 0
    }
    
    # Topic mastery categorization
    topic_rows = student_topic_rows(sid)
    strong = [r['topic_name'] for r in topic_rows if r.get('mastery') == 'STRONG']
    weak = [r['topic_name'] for r in topic_rows if r.get('mastery') == 'WEAK']
    
    previous_report = db.fetch_one(
        'SELECT * FROM weekly_reports WHERE student_id=%s AND week_start < %s ORDER BY week_start DESC LIMIT 1',
        (sid, start_of_week)
    )
    
    insights = generate_weekly_insights(stats, strong, weak, previous_report)
    next_focus = weak[0] if weak else ("Consistent revision" if strong else "Lecture study")
    
    db.execute(
        """INSERT INTO weekly_reports 
           (student_id, week_start, week_end, overall_score, study_hours, lectures_completed, assignments_completed, average_accuracy, topics_mastered, weak_topics, insights, next_focus)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           ON DUPLICATE KEY UPDATE
             overall_score = VALUES(overall_score),
             study_hours = VALUES(study_hours),
             lectures_completed = VALUES(lectures_completed),
             assignments_completed = VALUES(assignments_completed),
             average_accuracy = VALUES(average_accuracy),
             topics_mastered = VALUES(topics_mastered),
             weak_topics = VALUES(weak_topics),
             insights = VALUES(insights),
             next_focus = VALUES(next_focus)""",
        (sid, start_of_week, end_of_week, stats['overall_score'], stats['study_hours'], stats['lectures_completed'], stats['assignments_completed'], stats['average_accuracy'], ", ".join(strong[:5]), ", ".join(weak[:5]), insights, next_focus)
    )
    
    flash('Weekly performance report generated with customized insights!', 'success')
    return redirect(url_for('weekly_report'))

# ---------------------------------------------------------
# ERROR HANDLERS
# ---------------------------------------------------------
@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/error.html', code=400, title='Bad Request', message=str(e)), 400

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/error.html', code=403, title='Locked / Forbidden', message=str(e)), 403

@app.errorhandler(404)
def not_found(e):
    return render_template('errors/error.html', code=404, title='Page Not Found', message='The requested resource was not found on this server.'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/error.html', code=500, title='Server Error', message='An unexpected internal error occurred. Please try again.'), 500

# ---------------------------------------------------------
# RUN ENTRY POINT
# ---------------------------------------------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
