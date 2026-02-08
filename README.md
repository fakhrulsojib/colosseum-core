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
│   ├── api/                  # API endpoints and dependencies.
│   ├── db/                   # Database connection and sessions.
│   ├── models/               # SQLAlchemy ORM models.
│   ├── core/                 # Configuration and security logic.
│   ├── schemas/              # Pydantic data models.
│   └── services/             # External service integrations (Google).
└── alembic/                  # Database migrations.
```

## ⚡ Quick Start

This service is part of the larger Colosseum ecosystem. To get it running quickly:

1.  **Clone the Infrastructure Repo**: This project relies on the central gateway and database managed by `colosseum-infra`.
2.  **Set up Environment**:
    -   Copy `.env.example` to `.env`.
    -   Fill in your `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`.
3.  **Run via Infra**:
    ```bash
    # From the colosseum-infra directory
    make dev
    ```

## 🚀 Features

-   **Google OAuth 2.0**: Secure third-party authentication.
-   **JWT Management**: Issues secure tokens for system-wide state.
-   **Identity Storage**: Maintains the primary User database.
-   **REST API**: High-performance FastAPI endpoints.

## 🛠 Tech Stack

Detailed architecture and technical specifications can be found in [ARCHITECTURE.md](./ARCHITECTURE.md).

-   **Framework**: FastAPI (Python 3.11+)
-   **Database**: PostgreSQL (Async)
-   **Auth**: Authlib, Python-Jose
-   **Migrations**: Alembic

## 📦 Local Development

### Testing
To run tests inside the container:
```bash
# In colosseum-infra directory
docker-compose exec core-service pytest
```
