# LLM Implementation Prompts

Use these prompts to generate code iteratively or understand the implementation steps.

## Step 1: Infrastructure

> "Generate the Dockerfile, docker-compose.yml, and requirements.txt for a FastAPI project. Include `authlib` and `itsdangerous` for session management. Configure `pydantic-settings`."

## Step 2: Database & Models

> "Create `app/core/config.py` loading `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `DATABASE_URL`. Then create the SQLAlchemy Async model for `User` with a UUID primary key."

## Step 3: Security & JWT

> "Create `app/core/security.py`. Add a function `create_access_token(subject: str)` that encodes a JWT using HS256 and the SECRET_KEY from config."

## Step 4: Google OAuth Logic

> "Set up `app/services/google.py` using Authlib's `oauth.register`. Then create the `GET /login` and `GET /callback` endpoints in `app/api/v1/auth.py`. The callback should upsert the user into the DB and redirect to a dummy frontend URL with the JWT."

## Step 5: User Routes

> "Create `app/api/v1/users.py`. Add `GET /me` (dependency injected current user) and `POST /batch` (fetch multiple users by ID)."
