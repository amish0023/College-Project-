import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'personalised-learning-secret-key-production-ready')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'personalised_learning')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'personalised_learning')
    MYSQL_CURSORCLASS = 'DictCursor'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # Explainable AI Topic Priority Weights (Section 30)
    PRIORITY_WEIGHTS = {
        'weakness': 0.25,
        'inaccuracy': 0.20,
        'repeated_mistakes': 0.15,
        'time_difficulty': 0.10,
        'previous_performance': 0.10,
        'improvement': 0.10,
        'completion': 0.10
    }
