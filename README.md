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

4. **Optional: It is a good practice to delete the db and populate it again so testing can be done succesfully.

```bash
   # Remove old database and recreate
   rm -f app/app.db
   ```
    
```bash
   # Run populate_db to create tables and test user
python -m app.scripts.populate_db
   ```

```bash
   # Run populate_courses to add course data
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

### Current Features
- User authentication with proper database schema and form validation with WTForms.
- Users can login and logout from their accounts.
- Create, read, delete, and updte operations for courses and assingments.
- Users can enroll and drop courses.
- Rerouting and error validation for most of the routes.
- Protected routes implemented. 

## Screenshots
Home Page
<img width="1167" height="889" alt="image" src="https://github.com/user-attachments/assets/f7fd549a-d939-4f47-828c-a24556035e81" />

Registration
<img width="1190" height="584" alt="image" src="https://github.com/user-attachments/assets/881cc226-a782-4781-a90e-40ab5daaf560" />

After successfull registration redirects to sign in page
<img width="1185" height="645" alt="image" src="https://github.com/user-attachments/assets/bacf973a-a708-4425-9ef1-56ab1d0e2fb5" />

Home Page with protected links displaying the user email 
<img width="1416" height="802" alt="image" src="https://github.com/user-attachments/assets/d315df77-64e7-48df-9e5f-e7dec350c272" />

Creating a new Course
<img width="1426" height="928" alt="image" src="https://github.com/user-attachments/assets/12e38009-5cc5-4248-8532-6f263bc8289a" />

All courses page with new course displaying
<img width="1509" height="995" alt="image" src="https://github.com/user-attachments/assets/5594b2e3-0a2f-448c-a62e-2d8fee6dc7b4" />

Newly created course details
<img width="1512" height="636" alt="image" src="https://github.com/user-attachments/assets/7a1cf5c8-c272-4b01-9dbe-3762051e6e75" />

All courses and assignments
<img width="1286" height="986" alt="image" src="https://github.com/user-attachments/assets/0ef88d05-838e-41b5-bc61-5ec88fe53cd1" />

## Meet the Team

- Sofware Engineer: Jonathan Carpio
- Project Manager: Rahaf Mohammed
- Tester/Developer: Vern Toor

## App Preview

**index.html**

<img width="990" height="954" alt="Screenshot 2025-11-15 at 11 15 01 PM" src="https://github.com/user-attachments/assets/c60deb43-742e-41a6-a460-2e550622fcd1" />

**login.html rendered on /auth/login route with flashed messages**

<img width="990" height="954" alt="Screenshot 2025-11-15 at 11 15 07 PM" src="https://github.com/user-attachments/assets/b74a2c8d-a27c-4c83-9b9a-9a4ed72af4eb" />

## UI Sketches

<img width="1154" height="723" alt="Screenshot 2025-11-16 at 10 37 02 PM" src="https://github.com/user-attachments/assets/f7b2eac1-a8c9-45c4-8a94-200d33f6f7a8" />
<img width="1155" height="720" alt="Screenshot 2025-11-16 at 10 36 16 PM" src="https://github.com/user-attachments/assets/be4f62e3-5778-4422-9cd5-70ea2161371a" />
<img width="476" height="776" alt="Screenshot 2025-11-16 at 10 54 30 PM" src="https://github.com/user-attachments/assets/42cc1d83-a5bf-4466-a8fb-e14000427b5e" />
<img width="599" height="776" alt="Screenshot 2025-11-16 at 10 54 49 PM" src="https://github.com/user-attachments/assets/de925e2c-8d52-49ea-8475-343646fa4d65" />
