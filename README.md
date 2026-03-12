# Voice2Invoice FastAPI Project

## Features
- FastAPI backend
- Auth module with Google social login (Authlib)
- User/Company association
- Role-based permissions (admin, user)
- SQLAlchemy ORM, Alembic migrations

## Setup
1. Copy `.env.example` to `.env` and fill in your Google credentials.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run Alembic migrations:
   ```bash
   alembic upgrade head
   ```
4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

## Auth
- `/auth/login/google` — Google OAuth2 login
- `/auth/auth/google/callback` — Google OAuth2 callback

## Roles
- Admin: manage company, users, invoices
- User: create/view invoices
