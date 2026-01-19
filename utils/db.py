"""
Database utility module
SQLite database for storing user data and test results
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "english358.db")


def get_connection() -> sqlite3.Connection:
    """Get database connection"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables"""
    conn = get_connection()
    cursor = conn.cursor()

    # Users table with phone and registration status
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            full_name TEXT,
            phone TEXT,
            grade INTEGER DEFAULT 0,
            is_registered INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Test results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            test_id TEXT NOT NULL,
            grade INTEGER NOT NULL,
            topic TEXT,
            correct_answers INTEGER DEFAULT 0,
            total_questions INTEGER DEFAULT 0,
            score REAL DEFAULT 0,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (telegram_id)
        )
    """)

    # Completed tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completed_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task_id TEXT NOT NULL,
            task_type TEXT NOT NULL,
            grade INTEGER NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (telegram_id)
        )
    """)

    # User progress table (for tracking current test state)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            test_id TEXT,
            current_question INTEGER DEFAULT 0,
            correct_count INTEGER DEFAULT 0,
            answers TEXT,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (telegram_id)
        )
    """)

    conn.commit()
    conn.close()


def add_user(telegram_id: int, username: Optional[str] = None) -> bool:
    """Add new user (initial, not registered)"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (telegram_id, username, is_registered)
            VALUES (?, ?, 0)
            ON CONFLICT(telegram_id) DO UPDATE SET
                username = excluded.username,
                last_active = CURRENT_TIMESTAMP
        """, (telegram_id, username))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False
    finally:
        conn.close()


def complete_registration(telegram_id: int, phone: str, full_name: str) -> bool:
    """Complete user registration with phone and name"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE users SET
                phone = ?,
                full_name = ?,
                is_registered = 1,
                last_active = CURRENT_TIMESTAMP
            WHERE telegram_id = ?
        """, (phone, full_name, telegram_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error completing registration: {e}")
        return False
    finally:
        conn.close()


def get_user(telegram_id: int) -> Optional[Dict[str, Any]]:
    """Get user by telegram_id"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def is_user_registered(telegram_id: int) -> bool:
    """Check if user completed registration"""
    user = get_user(telegram_id)
    if user and user.get("is_registered") == 1:
        return True
    return False


def update_user_grade(telegram_id: int, grade: int) -> bool:
    """Update user's grade"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE users SET grade = ?, last_active = CURRENT_TIMESTAMP
            WHERE telegram_id = ?
        """, (grade, telegram_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating grade: {e}")
        return False
    finally:
        conn.close()


def save_test_result(
    user_id: int,
    test_id: str,
    grade: int,
    topic: str,
    correct_answers: int,
    total_questions: int
) -> bool:
    """Save test result"""
    conn = get_connection()
    cursor = conn.cursor()

    score = (correct_answers / total_questions * 100) if total_questions > 0 else 0

    try:
        cursor.execute("""
            INSERT INTO test_results
            (user_id, test_id, grade, topic, correct_answers, total_questions, score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, test_id, grade, topic, correct_answers, total_questions, score))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving test result: {e}")
        return False
    finally:
        conn.close()


def get_user_test_results(telegram_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """Get user's test results"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM test_results
        WHERE user_id = ?
        ORDER BY completed_at DESC
        LIMIT ?
    """, (telegram_id, limit))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def save_completed_task(user_id: int, task_id: str, task_type: str, grade: int) -> bool:
    """Save completed task"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO completed_tasks (user_id, task_id, task_type, grade)
            VALUES (?, ?, ?, ?)
        """, (user_id, task_id, task_type, grade))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving task: {e}")
        return False
    finally:
        conn.close()


def get_user_stats(telegram_id: int) -> Dict[str, Any]:
    """Get user statistics"""
    conn = get_connection()
    cursor = conn.cursor()

    # Total tests
    cursor.execute("""
        SELECT COUNT(*) as total, AVG(score) as avg_score
        FROM test_results WHERE user_id = ?
    """, (telegram_id,))
    test_stats = cursor.fetchone()

    # Total tasks
    cursor.execute("""
        SELECT COUNT(*) as total FROM completed_tasks WHERE user_id = ?
    """, (telegram_id,))
    task_stats = cursor.fetchone()

    conn.close()

    return {
        "total_tests": test_stats["total"] if test_stats else 0,
        "avg_score": round(test_stats["avg_score"], 1) if test_stats and test_stats["avg_score"] else 0,
        "total_tasks": task_stats["total"] if task_stats else 0
    }


# Progress tracking for ongoing tests
def save_user_progress(user_id: int, test_id: str, current_question: int, correct_count: int, answers: str) -> bool:
    """Save user's current test progress"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # First delete existing progress
        cursor.execute("DELETE FROM user_progress WHERE user_id = ?", (user_id,))
        # Then insert new progress
        cursor.execute("""
            INSERT INTO user_progress (user_id, test_id, current_question, correct_count, answers)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, test_id, current_question, correct_count, answers))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving progress: {e}")
        return False
    finally:
        conn.close()


def get_user_progress(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user's current test progress"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_progress WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def clear_user_progress(user_id: int) -> bool:
    """Clear user's test progress"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM user_progress WHERE user_id = ?", (user_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error clearing progress: {e}")
        return False
    finally:
        conn.close()


def get_all_users() -> List[Dict[str, Any]]:
    """Get all registered users"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE is_registered = 1 ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_daily_top_users(limit: int = 3) -> List[Dict[str, Any]]:
    """Get top active users for today based on test results"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.full_name,
            u.telegram_id,
            COUNT(tr.id) as tests_count,
            ROUND(AVG(tr.score), 1) as avg_score,
            SUM(tr.correct_answers) as total_correct,
            SUM(tr.total_questions) as total_questions
        FROM users u
        JOIN test_results tr ON u.telegram_id = tr.user_id
        WHERE DATE(tr.completed_at) = DATE('now', 'localtime')
            AND u.is_registered = 1
        GROUP BY u.telegram_id
        ORDER BY tests_count DESC, avg_score DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_weekly_top_users(limit: int = 10) -> List[Dict[str, Any]]:
    """Get top active users for current week based on test results"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.full_name,
            u.telegram_id,
            COUNT(tr.id) as tests_count,
            ROUND(AVG(tr.score), 1) as avg_score,
            SUM(tr.correct_answers) as total_correct,
            SUM(tr.total_questions) as total_questions
        FROM users u
        JOIN test_results tr ON u.telegram_id = tr.user_id
        WHERE tr.completed_at >= DATE('now', '-7 days')
            AND u.is_registered = 1
        GROUP BY u.telegram_id
        ORDER BY tests_count DESC, avg_score DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]
