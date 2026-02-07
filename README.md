# Colosseum Core Service

The Identity Provider and Auth gateway for Colosseum.

This microservice handles user authentication via Google OAuth 2.0 and manages the source of truth for user profiles.

## 🏗 Structure

```text
colosseum-core/
├── Dockerfile                # Instructions to build the Python container.
├── requirements.txt          # Dependencies (FastAPI, Authlib, SQLAlchemy).
├── app/
│   ├── main.py               # The entry point.
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py       # Handles "Login with Google" and JWT creation.
│   │   │   └── users.py      # User profile endpoints.
│   │   └── deps.py           # Dependency injection (Current User, DB Session).
│   ├── db/
│   │   └── session.py        # Database connection logic.
│   ├── models/
│   │   └── user.py           # The 'Users' table definition.
│   └── core/
│       ├── config.py         # Settings and Environment Variables.
│       └── security.py       # Logic to sign and encrypt JWTs.
└── alembic/                  # Database migrations.
```

## 🚀 Features

- **Google OAuth 2.0**: Secure third-party authentication.
- **JWT Management**: Issues secure tokens for local session state.
- **Identity Storage**: Maintains the primary User database.
- **REST API**: Provides endpoints for user data and batch retrieval.

## 🛠 Tech Stack

- **Framework**: FastAPI (Python)
- **Auth**: Authlib, Python-Jose
- **Database Logic**: SQLAlchemy 2.0 (Async)
- **Database**: PostgreSQL
- **Migrations**: Alembic
- **Testing**: Pytest, Pytest-Asyncio

## 📦 Local Development (via Docker)

This service is intended to be run as part of the Colosseum stack via `colosseum-infra`.

To run tests:
```bash
# In colosseum-infra directory
docker-compose exec core-service pytest
```
