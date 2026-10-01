from ..db import get_db


def create(student_id, program, school_year, notes):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO applications (student_id, program, school_year, notes) VALUES (?, ?, ?, ?)",
        (student_id, program, school_year, notes),
    )
    db.commit()
    return cursor.lastrowid


def list_for_student(student_id):
    return get_db().execute("SELECT * FROM applications WHERE student_id = ? ORDER BY created_at DESC", (student_id,)).fetchall()


def list_all():
    return get_db().execute(
        "SELECT applications.*, users.username, users.first_name, users.last_name, users.email FROM applications JOIN users ON users.id = applications.student_id ORDER BY applications.created_at DESC"
    ).fetchall()


def find_by_id(application_id):
    return get_db().execute("SELECT * FROM applications WHERE id = ?", (application_id,)).fetchone()


def update_status(application_id, status, notes):
    db = get_db()
    db.execute("UPDATE applications SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (status, notes, application_id))
    db.commit()


def count_by_status(status=None):
    db = get_db()
    if status:
        return db.execute("SELECT COUNT(*) AS count FROM applications WHERE status = ?", (status,)).fetchone()["count"]
    return db.execute("SELECT COUNT(*) AS count FROM applications").fetchone()["count"]
