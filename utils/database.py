import sqlite3
from pathlib import Path
from datetime import datetime

# Base folder = project root (springboard_intern)
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "app.db"


def get_connection():
    """Return a connection to the SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # ensure /data exists
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Users table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            resume_path TEXT
        );
        """
    )

    # Resume Analysis table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS resume_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            extracted_text TEXT NOT NULL,
            analysis_scores TEXT,
            strengths TEXT,
            weaknesses TEXT,
            identified_skills TEXT,
            recommended_skills TEXT,
            analysis_timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )

    # Job Recommendations table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS job_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_title TEXT,
            company_name TEXT,
            location TEXT,
            job_description TEXT,
            job_url TEXT,
            match_percentage REAL,
            scraping_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )

    conn.commit()
    conn.close()


def create_user(full_name: str, email: str, password_hash: str):
    """Insert a new user into the users table."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO users (full_name, email, password_hash, registration_date)
        VALUES (?, ?, ?, ?)
        """,
        (full_name, email, password_hash, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()


def get_user_by_email(email: str):
    """Fetch a single user row by email. Return dict or None."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return dict(row)


def save_resume_analysis(user_id: int, extracted_text: str,
                         analysis_scores: str = None,
                         strengths: str = None,
                         weaknesses: str = None,
                         identified_skills: str = None,
                         recommended_skills: str = None):
    """Save resume analysis data for a user."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO resume_analysis (
            user_id, extracted_text, analysis_scores,
            strengths, weaknesses, identified_skills,
            recommended_skills, analysis_timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            extracted_text,
            analysis_scores,
            strengths,
            weaknesses,
            identified_skills,
            recommended_skills,
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()
    conn.close()


def get_latest_resume_analysis(user_id: int):
    """Get the most recent resume analysis for a user."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM resume_analysis
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,)
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return dict(row)


def save_job_recommendation(user_id: int,
                            job_title: str,
                            company_name: str,
                            location: str,
                            job_description: str,
                            job_url: str,
                            match_percentage: float):
    """Insert a single job recommendation."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO job_recommendations (
            user_id, job_title, company_name, location,
            job_description, job_url, match_percentage, scraping_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            job_title,
            company_name,
            location,
            job_description,
            job_url,
            match_percentage,
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()
    conn.close()


def get_job_recommendations_for_user(user_id: int):
    """Fetch all job recommendations for a user."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM job_recommendations
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def update_user_resume_path(user_id: int, resume_path: str):
    """Update the stored resume path for a user."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE users
        SET resume_path = ?
        WHERE id = ?
        """,
        (resume_path, user_id)
    )
    conn.commit()
    conn.close()