# Exam Management System

An online Exam Management System built with Django and MySQL, designed to streamline exam processes for both teachers and students. The system provides separate dashboards and functionalities for teachers and students, enabling easy management of exams, questions, and results.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Features

### Teacher Features
- **Login and Registration**: Secure login and registration system for teachers.
- **Dashboard**: Overview of exams created and management options.
- **Exam Creation**: Allows teachers to create exams with a configurable number of questions.
- **Add and Edit Questions**: Teachers can add, edit, or delete questions associated with each exam.
- **Results Management**: View students' results and calculate scores as percentages.
- **Attempted Exams**: Automatically moves exams to “Attempted Exams” once completed by students.

### Student Features
- **Login and Registration**: Secure login and registration for students.
- **Dashboard**: Access available exams and past results.
- **Take Exam**: A feature to take exams with options to skip, mark for review, and submit answers.
- **Countdown Timer**: Visual timer that turns red in the last minute and auto-submits the exam at zero.
- **View Results**: Display of scores as a percentage and correct answers out of the total.

## Technologies Used
- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Environment**: Django on local development server

## Setup and Installation

### Prerequisites
- Python 3.x
- MySQL database
- Git
- (Optional) Virtual Environment for Python

### Installation Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/akashkumarnitc/exam_management_system.git
   cd exam_management_system
2. **Install dependencies
   ```bash
   pip install -r requirements.txt
3. **Configure database
   ```bash
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
    }

  4. **Run Migrations
     ```bash
     python manage.py migrate
  5. **Create a superuser
     ```bash
     python manage.py createsuperuser
  6. **Start Development Server
     ```bash
     python manage.py runserver
  7. **Access the Application
     ```open
     https://127.0.0.1:8000

## Project structure
```bash
   exam_management/
│
├── exam_management/          # Project settings and configuration
├── exams/                    # Exam app for managing exams and questions
├── users/                    # User app for handling authentication and profiles
├── templates/                # HTML templates
│   ├── registration/         # Templates for login, logout, and registration
│   ├── ...                   # Other templates (e.g., home, dashboard, exam, results)
│
├── static/                   # Static files (CSS, JavaScript)
├── media/                    # Media files (if any)
└── README.md
