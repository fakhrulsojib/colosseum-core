# Colosseum Core - Architecture & Technical Specs

The `colosseum-core` service acts as the central **Identity Provider** and **Authentication Gateway** for the Colosseum platform. It handles user authentication via Google OAuth, session management, and user data persistence.

## 1. Role & Responsibility
- **Central Identity Authority**: Manages User Identity (Profiles, Avatars, Roles).
- **Authentication**: Handles Google OAuth 2.0 flow.
- **Token Issuer**: Mints JWTs (JSON Web Tokens) for system-wide access.
- **Service Directory**: Serves as the "Phonebook" for other services (resolving UUIDs to Names).

**Independence:** This service owns the **User Database**. Other services (like Pool) *never* access the User DB directly; they rely on the JWT signed by this service or API calls via protected endpoints.

---

## 2. Technology Stack
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** PostgreSQL (Async via `asyncpg`)
- **ORM:** SQLAlchemy 2.0+ (Unified Mapping)
- **Migrations:** Alembic
- **Auth:** `authlib` (OAuth registry), `python-jose` (JWT handling)

---

## 3. Database Schema

### Table: `users`
| Column | Type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default gen_random_uuid() | The Global User ID |
| `email` | String | Unique, Not Null | Primary contact email |
| `google_sub` | String | Unique, Indexed | The Google Account ID |
| `full_name` | String | | Display Name |
| `avatar_url` | String | | URL to Google Profile Pic |
| `is_active` | Boolean | Default True | Access control flag |
| `is_superuser` | Boolean | Default False | Administrative privileges |
| `created_at` | DateTime | Default Now | |

---

## 4. Authentication Flow (The "Auth Dance")

### Scenario: User Login
1.  **Initiation**: Frontend directs user to `GET /api/v1/auth/login`.
2.  **Redirect**: Backend uses `authlib` to construct the Google OAuth URL and redirects the user.
3.  **Google Interaction**: User logs in on Google and grants permissions.
4.  **Callback**: Google redirects to `GET /api/v1/auth/callback?code=...`.
5.  **Token Exchange**: 
    - Exchange code for Google Access Token.
    - Fetch user details (Email, Name, Avatar) from Google UserInfo API.
6.  **Upsert**: Check DB for user by email. Update profile if existing, create if new.
7.  **Mint JWT**: `security.py` signs a Colosseum JWT (`sub: user_uuid`, `exp: 7d`).
8.  **Handoff**: Redirect user to Frontend (e.g., `http://localhost:3000/auth/success?token=<JWT>`).

### Scenario: Protected API Access
1.  **Request**: Frontend sends header `Authorization: Bearer <JWT>`.
2.  **Dependency**: `get_current_user` in `deps.py` validates the signature.
3.  **Validation**: Extracts `sub`, checks DB for active status.
4.  **Completion**: Endpoint receives a valid `User` model, serialized via Pydantic.

---

## 5. Module Responsibilities

- **`app/main.py`**: App initialization and middleware (Session/CORS).
- **`app/core/config.py`**: Pydantic-Settings management for environment variables.
- **`app/core/security.py`**: JWT signing/verification logic.
- **`app/db/`**: Async engine configuration and session factories.
- **`app/schemas/`**: Pydantic models for request validation and response serialization.
- **`app/api/v1/`**: Endpoint definitions for Auth and User management.
- **`app/services/google.py`**: Authlib OAuth registry configuration.
