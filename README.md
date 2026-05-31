# 🚀 Job Application Tracker

[![Flask](https://img.shields.io/badge/Flask-3.0-blue)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-green)](https://sqlite.org/)
[![Python](https://img.shields.io/badge/Python-3.10-yellow)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-red)](LICENSE)

> **A multi-user job application tracking system built with Flask, raw SQL, and session-based authentication.**

---

## 📌 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Database Schema](#-database-schema)
- [User Stories](#-user-stories)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Links](#-links)

---

## ✨ Features

### ✅ Core Requirements (Course Mandatory)
| Feature | Description |
|---------|-------------|
| 🔐 **Authentication** | Register, login, logout with session & cookies |
| 👥 **Multi-user** | Each user sees only their own applications |
| ➕ **Create** | Add new job applications (company, position, status, salary, dates) |
| 📖 **Read** | View all applications with status filtering |
| ✏️ **Update** | Edit application details |
| 🗑️ **Delete** | Remove applications with confirmation |
| 🗄️ **Raw SQL** | No ORM, pure SQLite3 queries |
| 🧪 **Unit Tests** | Business logic tested with unittest |

### ⭐ Extra Features (My Additions)
- 📊 **Dashboard** – Success rate, total applications, status distribution
- 📈 **Statistics** – (offer + accepted) / total × 100
- 🔍 **Status Filter** – Filter by applied/reviewing/interview/offer/rejected/accepted
- 📝 **Notes Field** – Add interview notes, salary expectations, follow-up dates
- 🗓️ **Next Action Date** – Track when to follow up

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Flask 3.0 |
| **Database** | SQLite3 (Raw SQL queries) |
| **Frontend** | HTML5, CSS3, Jinja2 templates |
| **Session** | Flask-Session (filesystem) |
| **Testing** | Python unittest |
| **Version Control** | Git + GitHub Projects (Kanban) |

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- Git
- Terminal/Command Prompt

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kardelenil/job-application-tracker.git
   cd job-application-tracker
