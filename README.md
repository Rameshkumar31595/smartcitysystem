# Smart City Information and Issue Reporting System

A Django-based web application developed as part of **Python Full Stack Development – SDP (2025–26)**.  
This system helps citizens access city services, report civic issues, and track their resolution status efficiently.

---

## Problem Description

Citizens often struggle to find accurate information about city services and report civic issues.  
This platform provides details about public services and allows users to report problems such as road damage, water leakage, or public infrastructure failures. Authorities can track and update issue status. Django manages reports and user interactions.

---

## Core Features

- City service directory
- Issue reporting
- Status tracking
- Role-based access control
- Admin management dashboard
- Authentication (Sign Up / Sign In)

---

## Roles

### Admin
- Updates city service information
- Creates, edits, and deletes service categories
- Creates, edits, and deletes issue categories
- Reviews reported issues
- Updates issue status (Open, In Progress, Resolved, Rejected)

### User
- Registers and logs in
- Browses city services
- Reports civic issues
- Tracks issue status

> Only **Admin** and **User** roles are implemented, strictly following the problem statement.

---

## Technology Stack

- **Backend:** Django 4.2.27
- **Frontend:** Django Templates, HTML, CSS
- **Database:** SQLite (Django default)
- **Styling:** Custom dark theme
- **Version Control:** Git & GitHub

SQLite is used as Django automatically provides it, removing the need for manual database configuration while fully satisfying project requirements.

---

## Project Structure

smartcitysystem/
├── smartcityportal/
│   ├── accounts/        # Authentication & user management
│   ├── services/        # City services and categories
│   ├── issues/          # Issue reporting and tracking
│   ├── templates/       # HTML templates
│   ├── static/          # CSS and static files
│   ├── manage.py
│   └── smartcityportal/ # Project settings
├── .gitignore
├── README.md
└── requirements.txt

---

## Database

- Uses **SQLite**, Django’s default database
- Automatically configured
- Uses Django ORM
- No manual SQL or database setup required

---

## Authentication & Access Flow

- Landing page is public
- Sign Up / Sign In required for accessing services, reporting issues, and dashboards
- Logged-in users are redirected to dashboard instead of landing page
- Admin users see admin dashboard
- Users see user dashboard
- Logout returns the user to the landing page

---

## Setup Instructions

### Step 1: Clone Repository
git clone https://github.com/Rameshkumar31595/smartcitysystem.git  
cd smartcitysystem

### Step 2: Create Virtual Environment
python -m venv .venv

### Step 3: Activate Virtual Environment
Windows:
.venv\Scripts\activate

Linux / macOS:
source .venv/bin/activate

### Step 4: Install Dependencies
pip install django

### Step 5: Apply Migrations
python manage.py makemigrations  
python manage.py migrate

### Step 6: Create Admin User
python manage.py createsuperuser

### Step 7: Seed Demo Data (Optional)
python manage.py seed_demo_data

### Step 8: Run Server
python manage.py runserver

Open browser and visit:
http://127.0.0.1:8000/

---

## Implemented Pages

- Landing Page
- User Dashboard
- Admin Dashboard
- City Services List
- City Service Detail
- Issue Reporting Form
- Issue List & Detail
- Admin Category Management Pages
- Authentication Pages (Login / Signup)

---

## Academic Compliance Note

- The project strictly follows the given SDP problem statement
- No additional roles beyond Admin and User
- PostgreSQL is not required as SQLite satisfies project requirements
- Django framework manages backend logic, database interactions, and user authentication

---

## Project Status

✔ Backend implemented  
✔ Frontend implemented  
✔ Authentication completed  
✔ Admin & User roles implemented  
✔ Database integrated  
✔ Version controlled with GitHub  

---

## Author

Rameshkumar kandula 
Python Full Stack Development – SDP  
2025–26

---

## License

This project is developed for academic purposes only.
