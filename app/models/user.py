from ..db import get_db


def find_by_username(username):
    return get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()


def find_by_id(user_id):
    return get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def create_student(username, password_hash, first_name, last_name, email):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO users (username, password_hash, role, first_name, last_name, email) VALUES (?, ?, 'student', ?, ?, ?)",
        (username, password_hash, first_name, last_name, email),
    )
    db.commit()
    return cursor.lastrowid


def create_admin(username, password_hash, first_name, last_name, email, role="admin"):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO users (username, password_hash, role, first_name, last_name, email) VALUES (?, ?, ?, ?, ?, ?)",
        (username, password_hash, role, first_name, last_name, email),
    )
    db.commit()
    return cursor.lastrowid


def list_students():
    return get_db().execute("SELECT * FROM users WHERE role = 'student' ORDER BY created_at DESC").fetchall()


def count_by_role(role):
    return get_db().execute("SELECT COUNT(*) AS count FROM users WHERE role = ?", (role,)).fetchone()["count"]
