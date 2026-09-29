# 🎓 Gyami Smart Learning Platform

A modern web-based smart learning platform designed to help students organize their learning, track progress, take quizzes, manage notes, use focused study sessions, and interact with a smart study assistant.

## ✨ Features

### 👤 Student Login & Signup

* Student registration with name, email, and password
* Secure password hashing using SHA-256
* Login authentication
* Student information stored in SQLite database

### 📊 Personal Dashboard

* Personalized student dashboard
* Course progress overview
* Assignment and task information
* Quick access to major learning tools
* Student profile section
* Recent learning activity

### 📚 Courses

Includes learning areas such as:

* Python Basics
* Web Development
* Database Essentials
* Artificial Intelligence
* Environmental Sustainability

Students can view courses and track their progress.

### 📖 Digital Books & Resources

A dedicated digital resource section containing learning materials related to:

* Python
* Web Development
* Databases
* Artificial Intelligence
* Environmental Sustainability
* Smart Learning

### 📝 Smart Notes

Students can:

* Create personal notes
* View saved notes
* Delete notes
* Store notes persistently using the database

### ⏱️ Focus Study Timer

The platform includes a focused study timer with:

* 25-minute session
* 45-minute session
* 60-minute session
* Start, pause, and reset controls
* Saved focus-session history
* Daily focus minutes
* Total focus minutes
* Session count

### 🧠 Smart Quiz

An interactive quiz system covering topics such as:

* Python
* HTML
* CSS
* SQL
* Artificial Intelligence
* Environmental Sustainability

Features include:

* Multiple-choice questions
* Instant answer feedback
* Automatic score calculation
* Percentage calculation
* Quiz result history
* Retry option

### 🤖 AI Study Assistant

A built-in smart study assistant that helps students with basic learning-related questions and suggestions.

It includes:

* Interactive chat interface
* Study-related suggestions
* Python learning help
* Database learning help
* Study planning prompts
* Exam preparation prompts

> The current assistant uses a rule-based backend implementation rather than an external large language model API.

### 📈 Progress Tracking

The progress page provides an overview of:

* Courses started
* Course progress
* Focus-study minutes
* Quiz performance
* Saved notes
* Recent learning activity
* Learning summary

### 🔔 Activity & Notifications

The backend records relevant student activities and can create notifications for events such as:

* New account creation
* Completed quiz
* Longer focus-study sessions

---

## 🎨 Design

Gyami uses a modern futuristic student-tech interface featuring:

* 🌌 Dark navy/black background
* ⚡ Electric blue accents
* 🔶 Bright orange highlights
* ✨ Glowing UI elements
* 🪟 Glass-style panels
* 📱 Responsive layouts
* 🎓 Student-focused dashboard design
* 📊 Progress visualization
* 🤖 AI-inspired interface elements

The design is intended to provide a clean and engaging learning environment without overwhelming the student.

---

## 🛠️ Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* FastAPI
* Uvicorn

### Database

* SQLite

### Other

* REST API architecture
* Local browser storage for logged-in user session
* SHA-256 password hashing

---

## 📁 Project Structure

```text
Gyami-Smart-Learning-Platform/
│
├── css/
│   └── style.css
│
├── index.html
├── signup.html
├── dashboard.html
├── courses.html
├── books.html
├── notes.html
├── focus.html
├── quiz.html
├── ai.html
├── progress.html
├── about.html
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/srenithyaad613-png/Gyami-Smart-Learning-Platform.git
```

### 2. Open the project folder

```bash
cd Gyami-Smart-Learning-Platform
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI server

```bash
python -m uvicorn main:app --reload
```

### 5. Open the application

Open your browser and visit:

```text
http://127.0.0.1:8000
```

---

## 🗄️ Database

Gyami uses **SQLite** for persistent storage.

The backend automatically creates the required database tables when the application starts.

The database stores information including:

* Users
* Courses
* Course progress
* Notes
* Assignments
* Focus sessions
* Quiz results
* Journal/activity information
* Notifications

The database file is generated locally when the application runs and is intentionally not included in the GitHub repository.

---

## 🔐 Security

The application includes basic security practices such as:

* SHA-256 password hashing
* API-based authentication flow
* User-specific data retrieval
* Input handling on frontend forms
* Database-backed persistent storage

This project is intended as an educational/hackathon application and is not presented as a production-grade authentication system.

---

## 🎯 Project Objective

The goal of Gyami is to bring several everyday student-learning activities into one simple platform.

Instead of switching between separate tools for notes, courses, quizzes, focus sessions, and progress tracking, students can access these functions through one centralized learning dashboard.

---

## 🌱 Future Scope

Possible future improvements include:

* Integration with a real AI/LLM learning assistant
* Personalized AI study recommendations
* Advanced analytics and visual reports
* Gamification and achievement systems
* Study streak tracking
* Assignment deadlines and reminders
* Cloud database integration
* User profile customization
* More courses and learning resources
* Deployment as a publicly accessible web application

---

## 👩‍💻 Project

**Gyami Smart Learning Platform**

Built as a student-focused smart learning project combining web development, backend APIs, database management, and AI-inspired learning features.

---

## 📌 Note

Gyami is currently designed to run locally using FastAPI and SQLite. Uploading the source code to GitHub does not itself deploy the application as a live website.
