"""Authentication and student authorization helpers."""
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('student_id'):
            flash('Please sign in to access your learning portal.', 'warning')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


def owns_subject(subject_id, student_id, db_module):
    row = db_module.fetch_one(
        'SELECT 1 FROM student_subjects WHERE student_id=%s AND subject_id=%s AND is_active=1',
        (student_id, subject_id)
    )
    return bool(row)
