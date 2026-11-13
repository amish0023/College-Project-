"""Robust parameterized MySQL data access layer using PyMySQL."""
from contextlib import contextmanager
import pymysql
import pymysql.cursors
from flask import has_app_context, current_app
from config import Config


@contextmanager
def connection():
    if has_app_context():
        cfg = current_app.config
    else:
        cfg = Config.__dict__
        
    db_name = cfg.get('MYSQL_DB') or cfg.get('MYSQL_DATABASE') or 'personalised_learning'
    conn = pymysql.connect(
        host=cfg.get('MYSQL_HOST', '127.0.0.1'),
        port=int(cfg.get('MYSQL_PORT', 3306)),
        user=cfg.get('MYSQL_USER', 'root'),
        password=cfg.get('MYSQL_PASSWORD', ''),
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor,
        charset='utf8mb4',
        autocommit=False
    )
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetch_one(sql, params=()):
    with connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()


def fetch_all(sql, params=()):
    with connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()


def execute(sql, params=()):
    with connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.lastrowid
