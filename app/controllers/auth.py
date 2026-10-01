from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash
from sqlite3 import IntegrityError
from ..models.user import create_student
from ..security import authenticate, csrf_token, login_user, logout_user, validate_csrf

auth_bp = Blueprint("auth", __name__)


def _clean(value, max_length=120):
    return " ".join(value.strip().split())[:max_length]


@auth_bp.route("/")
def home():
    return render_template("home.html", title="Welcome")


@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        validate_csrf()
        username = _clean(request.form.get("username", ""), 50)
        password = request.form.get("password", "")
        user = authenticate(username, password)
        if not user:
            flash("Invalid username or password.", "danger")
        else:
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for("admin.dashboard" if user["role"] in ("admin", "super_admin") else "student.dashboard"))
    return render_template("auth/login.html", title="Log in")


@auth_bp.route("/signup", methods=("GET", "POST"))
def signup():
    if request.method == "POST":
        validate_csrf()
        username = _clean(request.form.get("username", ""), 50)
        password = request.form.get("password", "")
        first_name = _clean(request.form.get("first_name", ""), 60)
        last_name = _clean(request.form.get("last_name", ""), 60)
        email = _clean(request.form.get("email", ""), 120)
        if not all((username, password, first_name, last_name, email)):
            flash("All fields are required.", "danger")
        elif len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
        elif "@" not in email:
            flash("Enter a valid email address.", "danger")
        else:
            try:
                create_student(username, generate_password_hash(password), first_name, last_name, email)
            except IntegrityError:
                flash("That username is already in use.", "danger")
            else:
                flash("Account created. You can now log in.", "success")
                return redirect(url_for("auth.login"))
    return render_template("auth/signup.html", title="Student signup")


@auth_bp.post("/logout")
def logout():
    validate_csrf()
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.home"))
