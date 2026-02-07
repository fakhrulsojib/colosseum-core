# Colosseum Core Service

The Identity Provider and Auth gateway for Colosseum.

This microservice handles user authentication exclusively via Google OAuth 2.0 and manages the source of truth for user profiles.

## 🏗 Structure

```text
colosseum-core/
├── Dockerfile                # Instructions to build the Python container.
├── requirements.txt          # Dependencies (FastAPI, Authlib, SQLAlchemy).
├── app/
│   ├── main.py               # The entry point.
│   ├── api/
│   │   └── auth.py           # Handles "Login with Google" and JWT creation.
│   ├── db/
│   │   └── models.py         # The 'Users' table definition.
│   └── core/
│       └── security.py       # Logic to sign and encrypt JWTs.
└── migrations/               # SQL scripts for database schema.
```

## 🚀 Features

- **Google OAuth 2.0**: Secure third-party authentication.
- **JWT Management**: Issues secure tokens for local session state.
- **Identity Storage**: Maintains the primary User database.

## 🛠 Tech Stack

- **Framework**: FastAPI (Python)
- **Auth**: Authlib
- **Database Logic**: SQLAlchemy (Async)
- **Database**: PostgreSQL

## 📦 Local Development (via Docker)

This service is intended to be run as part of the Colosseum stack via `colosseum-infra`.

```bash
# To build the image manually
docker build -t colosseum-core .
```
