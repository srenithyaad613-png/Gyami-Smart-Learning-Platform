from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import sqlite3
from pathlib import Path
from datetime import datetime, date, timedelta
import hashlib
import json

BASE = Path(__file__).resolve().parent
DB = BASE / "Gyami.db"

app = FastAPI(title="Gyami Smart Learning Platform", version="1.0")

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def init_db():
    c = conn()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS courses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        progress INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS user_progress(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        progress INTEGER DEFAULT 0,
        updated_at TEXT NOT NULL,
        UNIQUE(user_id, course_id)
    );
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS assignments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        due_date TEXT,
        completed INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS focus_sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        minutes INTEGER NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS quiz_results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        quiz_name TEXT NOT NULL,
        score INTEGER NOT NULL,
        total INTEGER NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS journal(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        mood TEXT NOT NULL,
        text TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS notifications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        seen INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    );
    """)
    count = c.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    if count == 0:
        c.executemany(
            "INSERT INTO courses(title,category,description) VALUES(?,?,?)",
            [
                ("Python Basics", "Programming", "Variables, data types, conditions, loops and functions."),
                ("Web Development", "Technology", "HTML, CSS and JavaScript fundamentals."),
                ("Database Essentials", "Technology", "Tables, queries, relationships and SQLite basics."),
                ("Artificial Intelligence", "AI", "AI concepts, responsible use and everyday applications."),
                ("Environmental Sustainability", "Innovation", "Technology ideas for cleaner and smarter living.")
            ]
        )
    c.commit()
    c.close()

init_db()

class Signup(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class ProgressIn(BaseModel):
    user_id: int
    course_id: int
    progress: int

class NoteIn(BaseModel):
    user_id: int
    title: str
    content: str

class AssignmentIn(BaseModel):
    user_id: int
    title: str
    due_date: str = ""

class FocusIn(BaseModel):
    user_id: int
    minutes: int

class QuizIn(BaseModel):
    user_id: int
    quiz_name: str
    score: int
    total: int

class JournalIn(BaseModel):
    user_id: int
    mood: str
    text: str

class AIIn(BaseModel):
    user_id: int
    message: str

def now():
    return datetime.now().isoformat(timespec="seconds")

def add_notification(user_id, message):
    c = conn()
    c.execute("INSERT INTO notifications(user_id,message,created_at) VALUES(?,?,?)",
              (user_id, message, now()))
    c.commit()
    c.close()

@app.get("/", response_class=HTMLResponse)
def home():
    return page("index.html")

@app.get("/{name}.html", response_class=HTMLResponse)
def html_page(name: str):
    return page(name + ".html")

@app.get("/css/style.css")
def css():
    return HTMLResponse((BASE/"css"/"style.css").read_text(encoding="utf-8"), media_type="text/css")

@app.get("/js/{name}")
def js(name: str):
    p = BASE/"js"/name
    if p.exists():
        return HTMLResponse(p.read_text(encoding="utf-8"), media_type="application/javascript")
    return JSONResponse({"error":"Not found"}, status_code=404)

def page(filename):
    p = BASE / filename
    if not p.exists():
        return HTMLResponse("<h1>Page not found</h1>", status_code=404)
    return p.read_text(encoding="utf-8")

@app.get("/api/health")
def health():
    return {"success": True, "message": "Gyami backend is running"}

@app.post("/api/signup")
def signup(x: Signup):
    c = conn()
    try:
        cur = c.execute("INSERT INTO users(name,email,password,created_at) VALUES(?,?,?,?)",
                        (x.name.strip(), x.email.strip().lower(), hash_password(x.password), now()))
        uid = cur.lastrowid
        c.commit()
        add_notification(uid, "Welcome to Gyami! Your learning journey starts today.")
        return {"success": True, "message": "Account created successfully!", "user": {"id":uid,"name":x.name.strip(),"email":x.email.strip().lower()}}
    except sqlite3.IntegrityError:
        return {"success": False, "message": "An account with this email already exists."}
    finally:
        c.close()

@app.post("/api/login")
def login(x: Login):
    c = conn()
    u = c.execute("SELECT id,name,email FROM users WHERE email=? AND password=?",
                  (x.email.strip().lower(), hash_password(x.password))).fetchone()
    c.close()
    if not u:
        return {"success": False, "message": "Invalid email or password."}
    return {"success": True, "message": "Login successful!", "user": dict(u)}

@app.get("/api/user/{uid}")
def user(uid: int):
    c = conn()
    u = c.execute("SELECT id,name,email,created_at FROM users WHERE id=?", (uid,)).fetchone()
    c.close()
    return {"success": bool(u), "user": dict(u) if u else None}

@app.get("/api/courses")
def courses():
    c = conn()
    rows = c.execute("SELECT * FROM courses ORDER BY id").fetchall()
    c.close()
    return {"success": True, "courses": [dict(r) for r in rows]}

@app.post("/api/progress")
def save_progress(x: ProgressIn):
    p = max(0, min(100, x.progress))
    c = conn()
    c.execute("""INSERT INTO user_progress(user_id,course_id,progress,updated_at)
                 VALUES(?,?,?,?)
                 ON CONFLICT(user_id,course_id) DO UPDATE SET progress=excluded.progress,updated_at=excluded.updated_at""",
              (x.user_id,x.course_id,p,now()))
    c.commit(); c.close()
    return {"success": True, "progress": p}

@app.get("/api/progress/{uid}")
def progress(uid: int):
    c = conn()
    rows = c.execute("""SELECT c.id,c.title,c.category,c.description,
                        COALESCE(up.progress,0) progress
                        FROM courses c LEFT JOIN user_progress up
                        ON c.id=up.course_id AND up.user_id=?
                        ORDER BY c.id""",(uid,)).fetchall()
    focus = c.execute("SELECT COALESCE(SUM(minutes),0) FROM focus_sessions WHERE user_id=?",(uid,)).fetchone()[0]
    notes = c.execute("SELECT COUNT(*) FROM notes WHERE user_id=?",(uid,)).fetchone()[0]
    quizzes = c.execute("SELECT COUNT(*) FROM quiz_results WHERE user_id=?",(uid,)).fetchone()[0]
    c.close()
    vals=[r["progress"] for r in rows]
    overall=round(sum(vals)/len(vals)) if vals else 0
    return {"success":True,"courses":[dict(r) for r in rows],"overall":overall,"focus_minutes":focus,"notes":notes,"quiz_attempts":quizzes}

@app.post("/api/notes")
def create_note(x: NoteIn):
    c=conn()
    cur=c.execute("INSERT INTO notes(user_id,title,content,created_at) VALUES(?,?,?,?)",
                  (x.user_id,x.title.strip(),x.content.strip(),now()))
    c.commit(); nid=cur.lastrowid; c.close()
    return {"success":True,"id":nid}

@app.get("/api/notes/{uid}")
def notes(uid:int):
    c=conn(); rows=c.execute("SELECT * FROM notes WHERE user_id=? ORDER BY id DESC",(uid,)).fetchall(); c.close()
    return {"success":True,"notes":[dict(r) for r in rows]}

@app.delete("/api/notes/{nid}")
def delete_note(nid:int):
    c=conn(); c.execute("DELETE FROM notes WHERE id=?",(nid,)); c.commit(); c.close()
    return {"success":True}

@app.post("/api/assignments")
def create_assignment(x: AssignmentIn):
    c=conn(); cur=c.execute("INSERT INTO assignments(user_id,title,due_date,created_at) VALUES(?,?,?,?)",
                             (x.user_id,x.title.strip(),x.due_date,now()))
    c.commit(); aid=cur.lastrowid; c.close()
    return {"success":True,"id":aid}

@app.get("/api/assignments/{uid}")
def assignments(uid:int):
    c=conn(); rows=c.execute("SELECT * FROM assignments WHERE user_id=? ORDER BY completed,due_date,id",(uid,)).fetchall(); c.close()
    return {"success":True,"assignments":[dict(r) for r in rows]}

@app.patch("/api/assignments/{aid}")
def complete_assignment(aid:int):
    c=conn(); c.execute("UPDATE assignments SET completed=CASE completed WHEN 0 THEN 1 ELSE 0 END WHERE id=?",(aid,)); c.commit(); c.close()
    return {"success":True}

@app.post("/api/focus")
def focus(x: FocusIn):
    minutes=max(1,min(600,x.minutes))
    c=conn(); c.execute("INSERT INTO focus_sessions(user_id,minutes,created_at) VALUES(?,?,?)",(x.user_id,minutes,now())); c.commit(); c.close()
    if minutes >= 25: add_notification(x.user_id,f"Great focus session! You studied for {minutes} minutes.")
    return {"success":True}

@app.get("/api/focus/{uid}")
def focus_history(uid:int):
    c=conn(); rows=c.execute("SELECT * FROM focus_sessions WHERE user_id=? ORDER BY id DESC LIMIT 20",(uid,)).fetchall(); c.close()
    return {"success":True,"sessions":[dict(r) for r in rows]}

@app.post("/api/quiz")
def quiz(x: QuizIn):
    c=conn(); c.execute("INSERT INTO quiz_results(user_id,quiz_name,score,total,created_at) VALUES(?,?,?,?,?)",
                         (x.user_id,x.quiz_name,x.score,x.total,now())); c.commit(); c.close()
    add_notification(x.user_id,f"Quiz completed: {x.score}/{x.total}. Keep learning!")
    return {"success":True}

@app.get("/api/tests/{uid}")
def tests(uid:int):
    c=conn(); rows=c.execute("SELECT * FROM quiz_results WHERE user_id=? ORDER BY id DESC",(uid,)).fetchall(); c.close()
    return {"success":True,"tests":[dict(r) for r in rows]}

@app.post("/api/journal")
def journal(x: JournalIn):
    c=conn(); c.execute("INSERT INTO journal(user_id,mood,text,created_at) VALUES(?,?,?,?)",(x.user_id,x.mood,x.text,now())); c.commit(); c.close()
    return {"success":True}

@app.get("/api/activity/{uid}")
def activity(uid:int):
    c=conn()
    notifications=c.execute("SELECT * FROM notifications WHERE user_id=? ORDER BY id DESC LIMIT 10",(uid,)).fetchall()
    quiz=c.execute("SELECT * FROM quiz_results WHERE user_id=? ORDER BY id DESC LIMIT 10",(uid,)).fetchall()
    focus=c.execute("SELECT * FROM focus_sessions WHERE user_id=? ORDER BY id DESC LIMIT 10",(uid,)).fetchall()
    c.close()
    return {"success":True,"notifications":[dict(x) for x in notifications],"quizzes":[dict(x) for x in quiz],"focus":[dict(x) for x in focus]}

@app.post("/api/ai")
def ai(x: AIIn):
    q=x.message.lower()
    if any(w in q for w in ["python","coding","programming"]):
        answer="Try this study path: variables → data types → operators → if/else → loops → functions. Practice one tiny program after each topic."
    elif any(w in q for w in ["exam","test","study"]):
        answer="Use a 25-minute focus block, pick one topic, write a 5-line summary, then solve 3 questions without looking at notes."
    elif "time" in q or "schedule" in q:
        answer="Try: 25 min study + 5 min break, repeated three times. Finish with 10 minutes of revision and plan tomorrow's first task."
    elif "motivat" in q:
        answer="Make the next step tiny. Open the topic, study for five minutes, and let momentum do the rest."
    else:
        answer="I can help you plan study sessions, explain beginner topics, suggest revision methods, and organize your learning. Tell me the subject and what you are stuck on."
    return {"success":True,"answer":answer}

# Helpful demo endpoint for checking the app without any special setup.
@app.get("/api/status")
def status():
    c=conn()
    users=c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    notes=c.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    c.close()
    return {"success":True,"app":"Gyami","database":"SQLite","users":users,"notes":notes}
