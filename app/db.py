import sqlite3
from flask import current_app, g
from werkzeug.security import generate_password_hash

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('super_admin', 'admin', 'student')),
    first_name TEXT NOT NULL DEFAULT '',
    last_name TEXT NOT NULL DEFAULT '',
    email TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    program TEXT NOT NULL,
    school_year TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
    notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE
);
"""


def get_db():
    """Return one request-scoped SQLite connection with foreign keys enabled."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(SCHEMA)
    admin_username = current_app.config["DEFAULT_ADMIN_USERNAME"]
    admin_password = current_app.config["DEFAULT_ADMIN_PASSWORD"]
    existing = db.execute("SELECT id FROM users WHERE username = ?", (admin_username,)).fetchone()
    if not existing:
        db.execute(
            "INSERT INTO users (username, password_hash, role, first_name, last_name, email) VALUES (?, ?, ?, ?, ?, ?)",
            (admin_username, generate_password_hash(admin_password), "super_admin", "System", "Administrator", "admin@abuyogcc.edu.ph"),
        )
    demo = db.execute("SELECT id FROM users WHERE username = ?", ("student1",)).fetchone()
    if not demo:
        db.execute(
            "INSERT INTO users (username, password_hash, role, first_name, last_name, email) VALUES (?, ?, ?, ?, ?, ?)",
            ("student1", generate_password_hash("Student123!"), "student", "Juan", "Dela Cruz", "student@example.com"),
        )
    db.commit()
