# Voice2Invoice FastAPI Project (Modular Architecture)

This project is a FastAPI backend for a Voice2Invoice service, structured using a modular architecture. It includes features for authentication, company-based user management with Row-Level Security (RLS) in PostgreSQL, and distinct modules for different business domains.

## Features
- FastAPI backend
- **Modular Architecture**: Code is organized into distinct functional domains (`auth`, `voice`, `whatsapp`, `xero`, `embeddings`).
- **Database**: SQLAlchemy ORM with PostgreSQL. Designed for Company-based Row-Level Security (RLS).
- SQLAlchemy ORM, Alembic migrations
- **Authentication**: Auth module with Google social login (using Authlib) and JWT.
- **User Management**: User/Company association and role-based permissions (admin, user).

## Project Structure
```
app/
├── modules/
│   ├── auth/
│   ├── voice/
│   ├── whatsapp/
│   ├── xero/
│   └── embeddings/
├── core/
│   ├── database.py
│   ├── security.py
│   └── dependencies.py
├── models/
│   └── db.py
└── main.py
```

## Setup
1. Copy `.env.example` to `.env` and fill in your database and Google credentials.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize and run Alembic migrations:
   ```bash
   alembic init alembic
   # Edit alembic.ini to point to your DB URL and tell it where to find your models.
   alembic upgrade head
   ```
4. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## RLS with PostgreSQL
This project is intended to be used with Row-Level Security in PostgreSQL to enforce data isolation between different companies. You will need to set up RLS policies on your database tables (e.g., `invoices`) based on the user's `company_id`.
