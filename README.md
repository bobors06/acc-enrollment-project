# Abuyog Community College Enrollment System

A clean, modular **Flask + SQLite** enrollment system organized around controller, view, and model responsibilities. It includes student registration/login, role-based access control (RBAC), an administrator dashboard, enrollment applications, status updates, CSRF protection, password hashing, and secure database access.

## Features

- Student signup, login, logout, profile, and enrollment application submission
- Role-based access control for `super_admin`, `admin`, and `student`
- Admin dashboard with student/application summaries
- Admin application review and status updates (`pending`, `approved`, `rejected`)
- Super admin can create additional admin users
- SQLite database with automatic schema creation and seed data
- Parameterized SQL queries (no string-concatenated user input)
- Password hashing via Werkzeug, session hardening, CSRF protection, validation, and security headers
- Responsive HTML/CSS interface with clear flash messages

## Quick start in VS Code

> Requires Python 3.10+.

### Windows PowerShell

```powershell
cd abuyog_enrollment_system
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python run.py
```

### macOS/Linux

```bash
cd abuyog_enrollment_system
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Open `http://127.0.0.1:5000`.

## Default administrator

The first run creates this account:

- **Username:** `superadmin`
- **Password:** `ChangeMe123!`
- **Role:** `super_admin`

Change this password immediately in a production deployment. You can override the seed credentials before the first run using `DEFAULT_ADMIN_USERNAME` and `DEFAULT_ADMIN_PASSWORD` in `.env`.

A demo student is also seeded:

- **Username:** `student1`
- **Password:** `Student123!`

## Project structure

```text
app/
  __init__.py              Application factory and configuration
  db.py                    SQLite connection, schema, and seed data
  security.py              CSRF, password, auth, and RBAC helpers
  models/                  Data-access/model layer
  controllers/             Route/controller layer
  templates/               View layer (Jinja HTML)
  static/                  CSS assets
run.py                     Development entry point
requirements.txt           Python dependencies
.env.example               Environment configuration template
tests/                     Automated tests
```

## Security notes

- Passwords are never stored in plaintext; `generate_password_hash` and `check_password_hash` are used.
- SQL is parameterized through SQLite placeholders.
- Every state-changing POST requires a session-backed CSRF token.
- Admin routes require an authenticated `admin` or `super_admin`; user routes require an authenticated student.
- Flask secret key, cookie flags, and seed credentials are configurable through environment variables.
- The development server is not intended for public production hosting. For deployment, use a production WSGI server, HTTPS, environment-managed secrets, database backups, and a reverse proxy.

## Run tests

```bash
pip install -r requirements.txt
pytest -q
```
