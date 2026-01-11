# Smart City Information and Issue Reporting System

A Django-based web application that helps citizens discover city services, report civic issues, and track their resolution status.  
This project is developed as part of **Python Full Stack Development – SDP (2025–26)**.

---

## 📌 Problem Statement

Citizens often struggle to find accurate information about city services and report civic issues.  
This platform provides details about public services and allows users to report problems such as road damage or water issues.  
Authorities can track and update issue status. Django manages reports and user interactions.

---

## 🎯 Core Features

- **City Service Directory**
  - Browse and search city services by category
  - View detailed information about each service

- **Issue Reporting**
  - Users can report civic issues with title, category, description, and location
  - Issues are linked to relevant departments

- **Status Tracking**
  - Track issue status (Open, In Progress, Resolved, Rejected)
  - Real-time updates by admin authorities

- **Authentication System**
  - User Sign Up & Sign In
  - Role-based access control (Admin / User)

- **Admin Dashboard**
  - Manage service categories
  - Manage issue categories
  - View and update reported issues
  - Approve, reject, or resolve issues

---

## 👥 User Roles

### 🔹 Admin
- Updates city service information
- Creates and deletes service categories
- Creates and deletes issue categories
- Reviews and updates issue status

### 🔹 User
- Registers and logs in to the platform
- Browses city services
- Reports civic issues
- Tracks issue status

> ⚠️ Only **Admin** and **User** roles are implemented, strictly following the problem statement.

---

## 🛠️ Tech Stack

| Layer        | Technology |
|-------------|------------|
| Backend     | Django 4.2.27 |
| Frontend    | Django Templates, HTML, CSS |
| Database    | SQLite (default Django database) |
| Styling     | Custom Dark Theme (CSS) |
| Version Control | Git & GitHub |

> SQLite is used as it is Django’s default database and fully satisfies the project requirements.

---

## 📂 Project Structure

