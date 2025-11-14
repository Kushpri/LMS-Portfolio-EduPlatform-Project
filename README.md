# Mini LMS — Portfolio Edu Platform 🎓  

A lightweight **Learning Management System (LMS)** built with **Flask** for portfolio and interview use.  
It lets users register, log in, browse courses, track lesson completion, and watch linked learning resources.

> 💼 Repository: `LMS-Portfolio-EduPlatform-Project`

---

## ✨ Features

- ✅ **User Authentication**
  - Register, login, logout
  - Passwords stored securely using hashing

- 📚 **Courses & Lessons**
  - Pre-seeded demo courses:
    - *Python for Beginners*
    - *Frontend Fundamentals*
  - Each course has multiple lessons

- 📈 **Progress Tracking**
  - Users can mark lessons as **Completed**
  - Completion stored in SQLite database (`lms.db`)
  - Progress shown as **percentage for each course**

- 🎥 **Video & Resource Links**
  - Each course page has:
    - Embedded YouTube video
    - Helpful external links (docs / full course)

- 🧩 **AJAX-based “Mark Complete”**
  - `Mark complete` button sends an AJAX request to `/complete`
  - Progress bar updates **without reloading** the page

- 💻 **Clean UI**
  - Centralized layout using `base.html`
  - Responsive layout with modern card-style design
  - Styled with custom **CSS** (`styles.css`)

---

## 🛠 Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy  
- **Database:** SQLite (`lms.db`)  
- **Frontend:** HTML, CSS, basic JavaScript (AJAX with `fetch`)  
- **Auth & Security:** Werkzeug password hashing  
- **Environment:** Python 3.x, virtualenv (recommended)

---

## 🗂 Project Structure

```bash
ONLINE LEARNING PLATFORM/
│
├── app.py                     # Main Flask application
├── lms.db                     # SQLite database (auto-created)
├── .gitignore                 # Ignore venv, db, cache files (recommended)
│
├── App/
│   └── static/
│       ├── styles.css         # Main stylesheet
│       └── script.js          # JS for "Mark complete" (AJAX)
│
├── templates/
│   ├── base.html              # Base layout (nav, container, footer)
│   ├── index.html             # Public home page – available courses
│   ├── login.html             # Login page
│   ├── register.html          # Register page
│   ├── dashboard.html         # User dashboard with search + progress
│   └── course.html            # Course details + lessons + video/resources
│
└── venv/                      # (Local virtual environment – not needed on GitHub)


ℹ️ For real projects, venv/ and lms.db should be excluded using .gitignore.
For this portfolio demo, they may temporarily appear in the repo.

🚀 How to Run Locally
1️⃣ Clone the repository
git clone https://github.com/Kushpri/LMS-Portfolio-EduPlatform-Project.git
cd LMS-Portfolio-EduPlatform-Project

2️⃣ (Optional but recommended) Create a virtual environment
python -m venv venv
# On Windows (CMD):
venv\Scripts\activate.bat
# On PowerShell:
venv\Scripts\Activate.ps1

3️⃣ Install dependencies
pip install flask flask_sqlalchemy werkzeug


(If you have a requirements.txt later, you can use pip install -r requirements.txt.)

4️⃣ Run the app
python app.py


If everything is correct, you should see Flask running on:

http://127.0.0.1:5000


Open that URL in your browser.

🔑 Demo Credentials

You can log in using the default seeded demo user:

Username: demo

Password: demo123

Or create a new account via the Register page.

🧮 How Progress Tracking Works

When a user clicks “Mark complete” on a lesson:

A POST request is sent to /complete via fetch (AJAX).

The backend stores the completion in the Progress table.

The course completion percentage is recalculated.

The progress bar and text on the UI update live using JavaScript.

This is great to show in interviews:

SQLAlchemy models

Relationships (User, Course, Lesson, Progress)

API endpoint + frontend integration

📌 Possible Future Improvements

Add admin panel to create/edit courses from UI

Add user profile page and learning history

Add pagination and more course categories

Support for file uploads (notes, assignments)

Deploy on Render / Railway / Azure / AWS / Heroku alternative

📄 License

This project is intended for personal learning and portfolio use.
You may adapt it for your own portfolio; just give credit to the original author.

💬 Summary (for Recruiters)

“I built a mini Learning Management System in Flask where users can register, log in, browse courses, mark lessons as complete with AJAX, and track progress stored in SQLite. The project shows my skills in backend development with Flask + SQLAlchemy, frontend templates, basic JavaScript, and clean project structuring suitable for production-style apps.”

---

## 👩‍💻 Author & Contact

**Priti Kushwaha**  
Aspiring Software Engineer | Full-Stack & Data Enthusiast

**📬 Contact**
- 🔗 **LinkedIn:** https://www.linkedin.com/m/in/priti-kushwaha-ab4a5b236/  
- 🐙 **GitHub:** https://github.com/Kushpri

If you liked this project or have opportunities, feel free to reach out! 😊
