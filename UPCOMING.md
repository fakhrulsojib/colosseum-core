# Upcoming Features - Core Service (Identity Provider)

## 1. Project Overview
**Service Name:** `colosseum-core`
**Role:** The Central Identity Authority.
**Responsibility:**
- Manages User Identity (Profiles, Avatars, Roles).
- Handles Google OAuth 2.0 Authentication.
- Mints JWTs (JSON Web Tokens) for system-wide access.
- Serves as the "Phonebook" for other services (resolving UUIDs to Names).
**Independence:** This service owns the **User Database**. Other services (like Pool) *never* access the User DB directly; they rely on the JWT signed by this service or API calls to this service.

---

## 2. Technology Stack
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** PostgreSQL 15 (Async)
- **ORM:** SQLAlchemy 2.0+ (AsyncIO)
- **Migrations:** Alembic
- **Auth Library:** `authlib` (for Google OAuth), `python-jose` (for JWT generation)
- **Environment:** Docker & Docker Compose

---

## 3. Architecture & Directory Structure
The project follows a standard Domain-Driven structure.

```text
/colosseum-core
├── Dockerfile              # Multi-stage python build
├── docker-compose.yml      # Local dev setup (DB + App)
├── requirements.txt        # fastapi, uvicorn, sqlalchemy, asyncpg, alembic, python-jose, authlib, httpx, pydantic-settings
├── alembic.ini             # Migration config
├── /app
│   ├── main.py             # Entry point, Middleware, CORS
│   ├── /core
│   │   ├── config.py       # Settings (CLIENT_ID, SECRET_KEY, DB_URL)
│   │   └── security.py     # Logic to Sign & Create JWTs
│   ├── /db
│   │   ├── session.py      # Async Engine & SessionMaker
│   │   └── base.py         # Import all models here
│   ├── /models
│   │   └── user.py         # SQLAlchemy Model: User
│   ├── /schemas
│   │   ├── user.py         # Pydantic: UserRead, UserCreate
│   │   └── token.py        # Pydantic: TokenSchema
│   ├── /api
│   │   └── /v1
│   │       ├── auth.py     # /login, /callback (Google Flow)
│   │       └── users.py    # /me, /batch (Profile Management)
│   └── /services
│       └── google.py       # Helper to configure Authlib OAuth registry

```

---

## 4. Database Schema (PostgreSQL)

*Note: These tables exist in the `public` schema.*

### Table: `users`

| Column | Type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default gen_random_uuid() | The Global User ID |
| `email` | String | Unique, Not Null | e.g., "john@company.com" |
| `google_sub` | String | Unique, Indexed | The Google Account ID |
| `full_name` | String |  | Display Name |
| `avatar_url` | String |  | URL to Google Profile Pic |
| `is_active` | Boolean | Default True | Can login? |
| `is_superuser` | Boolean | Default False | Admin access? |
| `created_at` | DateTime | Default Now |  |

---

## 5. Authentication Flow (The Critical Path)

1. **Initiation:**
* Frontend sends user to `GET /api/v1/auth/login`.
* Backend uses `authlib` to generate a Google Authorization URL.
* User is redirected to Google.


2. **Callback:**
* Google redirects user back to `GET /api/v1/auth/callback?code=...`.
* Backend exchanges `code` for an `access_token` from Google.
* Backend calls Google UserInfo API to get Email/Name/Avatar.


3. **Upsert (Update/Insert):**
* Backend checks DB: Does a user with this `email` exist?
* **If No:** Create new User row.
* **If Yes:** Update `avatar_url` and `full_name` (keep them fresh).


4. **Token Minting:**
* Backend creates a **JWT**.
* **Header:** `alg: HS256`
* **Payload:** `sub: <user_uuid>`, `exp: <7 days>`, `admin: <bool>`
* **Signature:** Signed using `SECRET_KEY` (The same key shared with Pool Service).


5. **Handoff:**
* Backend redirects the browser to the Frontend URL (e.g., `https://app.colosseum.com/auth/success?token=<JWT>`).
* *Note:* In production, strict cookies are better, but for this hybrid architecture, a redirect query param is easier to implement first.



---

## 6. API Endpoints Specification

### `GET /api/v1/auth/login`

* **Action:** Redirects to Google.

### `GET /api/v1/auth/callback`

* **Action:** Handles OAuth dance. Redirects to Frontend with JWT.

### `GET /api/v1/users/me`

* **Headers:** `Authorization: Bearer <JWT>`
* **Response:** `{ "id": "uuid", "email": "...", "full_name": "...", "avatar_url": "..." }`
* **Logic:** Decodes JWT, fetches fresh data from DB.

### `POST /api/v1/users/batch`

* **Role:** Internal/Public use. Used by Game Services (Pool) to resolve IDs on the leaderboard.
* **Body:** `{"user_ids": ["uuid-1", "uuid-2"]}`
* **Response:** List of User objects.
* **Logic:** `SELECT * FROM users WHERE id IN (...)`

---

## 7. Step-by-Step Implementation Guide for LLM

*Use these prompts to generate code iteratively.*

**Step 1: Infrastructure**

> "Generate the Dockerfile, docker-compose.yml, and requirements.txt for a FastAPI project. Include `authlib` and `itsdangerous` for session management. Configure `pydantic-settings`."

**Step 2: Database & Models**

> "Create `app/core/config.py` loading `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `DATABASE_URL`. Then create the SQLAlchemy Async model for `User` with a UUID primary key."

**Step 3: Security & JWT**

> "Create `app/core/security.py`. Add a function `create_access_token(subject: str)` that encodes a JWT using HS256 and the SECRET_KEY from config."

**Step 4: Google OAuth Logic**

> "Set up `app/services/google.py` using Authlib's `oauth.register`. Then create the `GET /login` and `GET /callback` endpoints in `app/api/v1/auth.py`. The callback should upsert the user into the DB and redirect to a dummy frontend URL with the JWT."

**Step 5: User Routes**

> "Create `app/api/v1/users.py`. Add `GET /me` (dependency injected current user) and `POST /batch` (fetch multiple users by ID)."