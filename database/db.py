"""
Database connection and initialization
"""
import sqlite3
import threading
from pathlib import Path
from config import DB_PATH

# Thread-local storage for database connections
_thread_local = threading.local()


def get_connection():
    """Get thread-safe database connection"""
    if not hasattr(_thread_local, 'connection') or _thread_local.connection is None:
        _thread_local.connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        _thread_local.connection.row_factory = sqlite3.Row
    return _thread_local.connection


def close_connection():
    """Close database connection"""
    if hasattr(_thread_local, 'connection') and _thread_local.connection is not None:
        _thread_local.connection.close()
        _thread_local.connection = None


def init_database():
    """Initialize database with schema"""
    from database.migrations import create_tables
    create_tables()


def execute_query(query, params=()):
    """Execute query and return results"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise


def fetch_one(query, params=()):
    """Fetch single row"""
    cursor = execute_query(query, params)
    return cursor.fetchone()


def fetch_all(query, params=()):
    """Fetch all rows"""
    cursor = execute_query(query, params)
    return cursor.fetchall()


def insert(query, params=()):
    """Insert and return last row id"""
    cursor = execute_query(query, params)
    return cursor.lastrowid


def update(query, params=()):
    """Update and return rows affected"""
    cursor = execute_query(query, params)
    return cursor.rowcount


def delete(query, params=()):
    """Delete and return rows affected"""
    cursor = execute_query(query, params)
    return cursor.rowcount
