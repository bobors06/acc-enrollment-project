from flask import Blueprint, flash, redirect, render_template, request, url_for
from ..models.application import create, list_for_student
from ..security import current_user, login_required, validate_csrf

student_bp = Blueprint("student", __name__, url_prefix="/student")
PROGRAMS = ("Bachelor of Science in Information Technology", "Bachelor of Elementary Education", "Bachelor of Business Administration", "Associate in Computer Technology")

@student_bp.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    return render_template("student/dashboard.html", title="Student dashboard", user=user, applications=list_for_student(user["id"]))

@student_bp.route("/apply", methods=("GET", "POST"))
@login_required
def apply():
    if request.method == "POST":
        validate_csrf()
        program = request.form.get("program", "")
        school_year = request.form.get("school_year", "").strip()[:20]
        notes = request.form.get("notes", "").strip()[:500]
        if program not in PROGRAMS or not school_year:
            flash("Choose a valid program and school year.", "danger")
        else:
            create(current_user()["id"], program, school_year, notes)
            flash("Enrollment application submitted for review.", "success")
            return redirect(url_for("student.dashboard"))
    return render_template("student/apply.html", title="Apply for enrollment", programs=PROGRAMS)
