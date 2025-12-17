# Welcome to IntelliGrades app!

As a part of our Software Engineering class, we are building **IntelliGrades**, a Learning Management System (LMS) prototype that helps educators and students manage courses, assignments, and grades in a efficient way.

## Project Overview

IntelliGrades is a Flask-based web application designed to improve educational workflows. Working on the following features as right now:
- User authentication (sign-in/sign-up)
- Course and assignment management
- Grade tracking and reporting
- A user-friendly interface built with Bootstrap

## Tech Stack

- **Backend**: Flask 3.0+
- **Database**: SQLAlchemy 2.0+ with SQLite
- **Forms**: WTForms 3.1+ and Flask-WTF
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5.3, HTML/CSS
- **Python**: 3.11+

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <https://github.com/jona70x/lms-project.git>
   cd lms-proj
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # For macOS
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional: It is a good practice to delete the db. Run the scripts to populate the db and you will be ready to go. 

```bash
   # Remove old database and recreate
   rm -f app/app.db
   ```

```bash
   # Populate db with test users
   python -m app.scripts.populate_db
   ```

```bash
   # courses and more test users
   python -m app.scripts.populate_courses
   ```

```bash
   # Start the app
   python run.py
   ```


### Running the Application

1. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate  # For macOS
   ```

2. **Run the Flask app**:
   ```bash
   python run.py
   ```

## Features
- Authentication & User Management: Provides secure user registration with role selection, email validation, hashed passwords, login/logout functionality, and role-based access to protected routes.

- Course Management: Enables creation, viewing, updating, and deletion of courses with capacity limits, unique code enforcement, enrollment availability toggles, and owner/admin permissions.

- Student Enrollment: Allows students to browse, enroll in, and drop courses while preventing duplicates and enforcing capacity and enrollment rules.

- Course Dashboard: Displays a tabbed dashboard with assignments, grades, submissions, people, and announcements, along with quick course info and role-specific actions.

- Assignment Management:Lets instructors create, update, and delete assignments while students view their relevant tasks, with details pages and contextual course selection.

- Grading System: Instructor in view submissions, grade, and updating scores, while students track assignment status and grades.

- Announcements: Provides instructors with tools to post, update, and delete course announcements visible to enrolled users.

- Academic Tools:Includes a GPA calculator that loads enrolled courses, supports letter-grade input, and computes weighted GPA in real time.

- Dashboard & Notifications: Offers personalized dashboards with role-specific course views.

- UI/UX Features: Features a responsive Bootstrap interface with form validation, flash messages, confirmation dialogs, and role-based visibility for UI elements.

- Security Features: URL redirects, password rules, session management, and permission checks in all db operations. Also a 404 catch all routes. 

## App Preview
Home Page
<img width="2996" height="1502" alt="image" src="https://github.com/user-attachments/assets/44e0a49d-309a-41c3-9547-c02a063eed59" />

Registration
<img width="3014" height="1790" alt="image" src="https://github.com/user-attachments/assets/0824f323-8263-4740-a116-a130f6cd408a" />

Course Dashboard as Professor
<img width="3014" height="1790" alt="image" src="https://github.com/user-attachments/assets/6e13e26a-b91f-4f38-88e0-67480a861588" />

New Assignment 
<img width="3014" height="1790" alt="image" src="https://github.com/user-attachments/assets/9db5bbd9-773c-4abd-9a09-7f0c6ff419bb" />

Repeated Course Title
<img width="3014" height="1790" alt="image" src="https://github.com/user-attachments/assets/fa3d6e6a-b11b-4125-a92b-a72374df632c" />

Student Submissions -- Professor View

<img width="3014" height="1790" alt="image" src="https://github.com/user-attachments/assets/d103eefa-2ef1-4efc-b6b3-99d0b27f4df3" />

New Announcement 

<img width="3014" height="1790" alt="image" src="https://github.com/user-attachments/assets/cca27618-c499-4d2e-b35d-b48c48534892" />

All courses and assignments view as student
<img width="3014" height="1790" alt="image" src="https://github.com/user-attachments/assets/666a17bf-35ea-47df-885e-25171e7536de" />

All enrolled students in course 
<img width="1514" height="901" alt="image" src="https://github.com/user-attachments/assets/ff6151e9-dba1-425b-a171-3dc9d36ece9b" />

Grades as student 
<img width="3014" height="1790" alt="image" src="https://github.com/user-attachments/assets/4ad48607-3493-4e89-bd07-93762e3a7945" />

Assignments as student
<img width="3014" height="1790" alt="image" src="https://github.com/user-attachments/assets/feb7ca5c-8e41-478f-b59e-8709f59c724c" />

Gpa calculator
<img width="3014" height="1790" alt="image" src="https://github.com/user-attachments/assets/a50de12a-91e1-4c4a-be6c-0a18ca29499a" />



## Meet the Team

- Sofware Engineer: Jonathan Carpio
- Project Manager: Rahaf Mohammed
- Tester/Developer: Vern Toor

## UI Sketches

<img width="1154" height="723" alt="Screenshot 2025-11-16 at 10 37 02 PM" src="https://github.com/user-attachments/assets/f7b2eac1-a8c9-45c4-8a94-200d33f6f7a8" />
<img width="1155" height="720" alt="Screenshot 2025-11-16 at 10 36 16 PM" src="https://github.com/user-attachments/assets/be4f62e3-5778-4422-9cd5-70ea2161371a" />
<img width="476" height="776" alt="Screenshot 2025-11-16 at 10 54 30 PM" src="https://github.com/user-attachments/assets/42cc1d83-a5bf-4466-a8fb-e14000427b5e" />
<img width="599" height="776" alt="Screenshot 2025-11-16 at 10 54 49 PM" src="https://github.com/user-attachments/assets/de925e2c-8d52-49ea-8475-343646fa4d65" />
