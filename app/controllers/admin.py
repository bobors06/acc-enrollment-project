from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlite3 import IntegrityError
from werkzeug.security import generate_password_hash
from ..models import application, user
from ..security import roles_required, validate_csrf

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@roles_required("admin", "super_admin")
def dashboard():
    return render_template("admin/dashboard.html", title="Admin dashboard", total_students=user.count_by_role("student"), total_applications=application.count_by_status(), pending=application.count_by_status("pending"), approved=application.count_by_status("approved"), rejected=application.count_by_status("rejected"))

@admin_bp.route("/applications")
@roles_required("admin", "super_admin")
def applications():
    return render_template("admin/applications.html", title="Applications", applications=application.list_all())

@admin_bp.post("/applications/<int:application_id>/status")
@roles_required("admin", "super_admin")
def update_application(application_id):
    validate_csrf()
    status = request.form.get("status", "")
    notes = request.form.get("notes", "").strip()[:500]
    if status not in ("pending", "approved", "rejected"):
        flash("Invalid status.", "danger")
    elif not application.find_by_id(application_id):
        flash("Application not found.", "danger")
    else:
        application.update_status(application_id, status, notes)
        flash("Application status updated.", "success")
    return redirect(url_for("admin.applications"))

@admin_bp.route("/students")
@roles_required("admin", "super_admin")
def students():
    return render_template("admin/students.html", title="Students", students=user.list_students())

@admin_bp.route("/admins/new", methods=("GET", "POST"))
@roles_required("super_admin")
def create_admin():
    if request.method == "POST":
        validate_csrf()
        values = {key: request.form.get(key, "").strip() for key in ("username", "first_name", "last_name", "email")}
        password = request.form.get("password", "")
        if not all(values.values()) or len(password) < 8:
            flash("All fields are required and the password must have 8+ characters.", "danger")
        else:
            try:
                user.create_admin(values["username"][:50], generate_password_hash(password), values["first_name"][:60], values["last_name"][:60], values["email"][:120])
            except IntegrityError:
                flash("That username is already in use.", "danger")
            else:
                flash("Administrator account created.", "success")
                return redirect(url_for("admin.dashboard"))
    return render_template("admin/new_admin.html", title="Create administrator")
