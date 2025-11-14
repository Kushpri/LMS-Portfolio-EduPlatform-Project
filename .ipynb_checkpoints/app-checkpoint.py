# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "lms.db")

app = Flask(__name__, static_folder="App/static", template_folder="templates")
app.config["SECRET_KEY"] = "dev-secret-key-change-in-prod"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=True)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=False)
    # optional timestamp can be added

# --- Helper functions ---
def create_and_seed_db():
    with app.app_context():
        if not os.path.exists(DB_PATH):
            db.create_all()
            demo = User(username="demo", password_hash=generate_password_hash("demo123"))
            db.session.add(demo)

            c1 = Course(title="Python Basics", description="Intro to Python and fundamentals.")
            c2 = Course(title="Web Dev with Flask", description="Mini project with Flask.")
            db.session.add_all([c1, c2])
            db.session.flush()

            lessons = [
                Lesson(course_id=c1.id, title="Variables & Types", content="Learn about variables."),
                Lesson(course_id=c1.id, title="Control Flow", content="If/else and loops."),
                Lesson(course_id=c2.id, title="Flask Basics", content="Routing, templates, run app."),
                Lesson(course_id=c2.id, title="Forms & DB", content="Saving data with SQLAlchemy."),
            ]
            db.session.add_all(lessons)
            db.session.commit()
        else:
            db.create_all()


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return User.query.get(uid)

# --- Routes ---
@app.route("/")
def index():
    # show public landing page with course list
    courses = Course.query.all()
    return render_template("index.html", courses=courses, user=current_user())

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Please provide username and password.", "warning")
            return redirect(url_for("register"))
        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "danger")
            return redirect(url_for("register"))
        u = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(u)
        db.session.commit()
        flash("Account created. You can log in now.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", user=current_user())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        u = User.query.filter_by(username=username).first()
        if u and u.check_password(password):
            session["user_id"] = u.id
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.", "danger")
        return redirect(url_for("login"))
    return render_template("login.html", user=current_user())

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out.", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    # show list of courses and progress
    courses = Course.query.all()
    # compute progress for each course (percentage of lessons completed)
    courses_data = []
    for c in courses:
        lessons = Lesson.query.filter_by(course_id=c.id).all()
        total = len(lessons)
        if total == 0:
            pct = 0
        else:
            completed = Progress.query.filter(Progress.user_id == user.id, Progress.lesson_id.in_([l.id for l in lessons])).count()
            pct = int((completed / total) * 100)
        courses_data.append({"course": c, "progress_pct": pct})
    return render_template("dashboard.html", user=user, courses_data=courses_data)

@app.route("/course/<int:course_id>")
def course(course_id):
    user = current_user()
    course = Course.query.get_or_404(course_id)
    lessons = Lesson.query.filter_by(course_id=course_id).all()
    completed_lesson_ids = []
    if user:
        completed_lesson_ids = [p.lesson_id for p in Progress.query.filter_by(user_id=user.id).all()]
    return render_template("course.html", user=user, course=course, lessons=lessons, completed_ids=completed_lesson_ids)

@app.route("/complete", methods=["POST"])
def complete():
    """AJAX endpoint to mark lesson complete. JSON in: {'lesson_id': 2}"""
    user = current_user()
    if not user:
        return jsonify({"success": False, "error": "not_logged_in"}), 401
    data = request.get_json() or {}
    lesson_id = data.get("lesson_id")
    if not lesson_id:
        return jsonify({"success": False, "error": "no_lesson_id"}), 400
    # ensure lesson exists
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"success": False, "error": "lesson_not_found"}), 404
    # check existing
    existing = Progress.query.filter_by(user_id=user.id, lesson_id=lesson.id).first()
    if not existing:
        p = Progress(user_id=user.id, lesson_id=lesson.id)
        db.session.add(p)
        db.session.commit()
    # compute updated progress percent for that course
    lessons = Lesson.query.filter_by(course_id=lesson.course_id).all()
    total = len(lessons)
    completed = Progress.query.filter(Progress.user_id == user.id, Progress.lesson_id.in_([l.id for l in lessons])).count()
    pct = int((completed / total) * 100) if total else 0
    return jsonify({"success": True, "progress_pct": pct})

# --- run/initialization ---
if __name__ == "__main__":
    create_and_seed_db()
    # Run app; in dev we keep debug True
    app.run(debug=True)
