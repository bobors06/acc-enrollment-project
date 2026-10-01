from pathlib import Path
from flask import Flask, render_template
from config import Config
from .db import close_db, init_db
from .controllers.auth import auth_bp
from .controllers.student import student_bp
from .controllers.admin import admin_bp


def create_app(test_config=None):
    """Application factory: creates a configured Flask app for dev, tests, or deployment."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.teardown_appcontext(close_db)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)

    @app.before_request
    def ensure_csrf_token():
        """Initialize the session CSRF token for every new browser session."""
        from .security import csrf_token
        csrf_token()

    @app.context_processor
    def inject_helpers():
        from .security import csrf_token
        return {"csrf_token": csrf_token}

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", title="Page not found", message="The page you requested does not exist."), 404

    @app.errorhandler(500)
    def server_error(_error):
        return render_template("error.html", title="Server error", message="Something went wrong. Please try again."), 500

    with app.app_context():
        init_db()
    return app
