import secrets
from functools import wraps
from flask import abort, flash, redirect, request, session, url_for
from werkzeug.security import check_password_hash
from .models.user import find_by_id


def csrf_token():
    """Create/reuse a per-session CSRF token for state-changing forms."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def validate_csrf():
    expected = session.get("csrf_token")
    supplied = request.form.get("csrf_token", "")
    if not expected or not secrets.compare_digest(expected, supplied):
        abort(400, description="Invalid or missing CSRF token.")


def login_user(user):
    session.clear()
    session["user_id"] = user["id"]
    session["role"] = user["role"]
    csrf_token()


def logout_user():
    session.clear()


def current_user():
    user_id = session.get("user_id")
    return find_by_id(user_id) if user_id else None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = current_user()
            if not user:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("auth.login"))
            if user["role"] not in roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


def authenticate(username, password):
    from .models.user import find_by_username
    user = find_by_username(username)
    return user if user and check_password_hash(user["password_hash"], password) else None
