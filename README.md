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
- User authentication pages
- Responsive navbar with Bootstrap
- Form validation with WTForms

## Meet the Team

- Sofware Engineer: Jonathan Carpio
- Project Manager: Rahaf Mohammed
- Tester/Developer: Vern Toor

## App Preview

**index.html**
<img width="990" height="954" alt="Screenshot 2025-11-15 at 11 15 01 PM" src="https://github.com/user-attachments/assets/c60deb43-742e-41a6-a460-2e550622fcd1" />

**login.html rendered on /auth/login route with flashed messages**
<img width="990" height="954" alt="Screenshot 2025-11-15 at 11 15 07 PM" src="https://github.com/user-attachments/assets/b74a2c8d-a27c-4c83-9b9a-9a4ed72af4eb" />
