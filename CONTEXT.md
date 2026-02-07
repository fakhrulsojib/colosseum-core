# Colosseum Core Service Documentation

The `colosseum-core` service acts as the central **Identity Provider** and **Authentication Gateway** for the Colosseum platform. It handles user authentication via Google OAuth, session management, and user data persistence.

## 1. Project Structure & Responsibilities

### **Entry Point**
*   **`app/main.py`**
    *   Initializes the `FastAPI` application.
    *   Configures middleware (SessionMiddleware for OAuth state management).
    *   Includes API routers from `app/api/v1`.
    *   Defines the root endpoint for health checks.

### **Configuration & Security (`app/core/`)**
*   **`app/core/config.py`**
    *   Manages application settings using `pydantic-settings`.
    *   Loads environment variables (DB URLs, Google Client Secrets, JWT Secrets) from `.env`.
    *   Provides computed properties for sync/async database connection strings.
*   **`app/core/security.py`**
    *   **JWT Handling**: Functions to create (`create_access_token`) and validate JSON Web Tokens.
    *   **Password Hashing**: Utilities for hashing/verifying passwords (using `passlib`), though primarily used for service-to-service or legacy auth flows.

### **Database Layer (`app/db/` & `app/models/`)**
*   **`app/db/session.py`**
    *   Configures the **Async Engine** (`asyncpg`) for PostgreSQL.
    *   Provides the `AsyncSessionLocal` factory and `get_db` dependency for database transactions.
*   **`app/db/base_class.py`**
    *   `Base`: The declarative base class for SQLAlchemy models.
    *   Automatically derives table names from class names (e.g., `User` -> `user`).
*   **`app/models/user.py`**
    *   **The Source of Truth** for User data.
    *   Defines the `users` table schema: `id` (UUID), `email`, `google_sub`, `full_name`, `avatar_url`, `is_active`, `is_superuser`.

### **Schemas / Data Transfer Objects (`app/schemas/`)**
*   **`app/schemas/user.py`**
    *   **Pydantic Models** that define API request/response structures.
    *   `UserCreate`: Validation for creating users.
    *   `User`: Public-facing user profile structure (hiding sensitive internal fields).
*   **`app/schemas/token.py`**
    *   Defines the JWT payload structure (`Token`, `TokenPayload`).

### **API Endpoints (`app/api/v1/`)**
*   **`app/api/v1/auth.py`**
    *   **GET /login**: Initiates the Google OAuth flow, redirecting the user to Google.
    *   **GET /callback**: Handles the redirect from Google.
        *   Exchanges authorization code for an access token.
        *   Retrieves user info (email, profile pic) from Google.
        *   **Upserts** the user in the database (Create if new, Update if existing).
        *   Issues a **JWT** (colosseum-specific access token) to the user.
        *   Redirects to the frontend with the token.
*   **`app/api/v1/users.py`**
    *   **GET /me**: Returns the currently authenticated user's profile.
    *   **POST /batch**: Internal helper to fetch multiple users by ID (e.g., for Leaderboards).

### **Dependencies (`app/api/deps.py`)**
*   **`SessionDep`**: Dependency that yields an async database session.
*   **`get_current_user`**:
    *   Extracts the Bearer token from the `Authorization` header.
    *   Decodes and validates the JWT using `SECRET_KEY`.
    *   Fetches the user from the DB.
    *   Raises `401 Unauthorized` or `403 Forbidden` if validation fails.

### **Services (`app/services/`)**
*   **`app/services/google.py`**
    *   Configures the `Authlib` OAuth registry for Google.
    *   Encapsulates Client ID/Secret and scope configuration (`openid email profile`).

---

## 2. Request Flows

### **Scenario A: User Login (The Auth Dance)**

1.  **Frontend** directs user to `GET /api/v1/auth/login`.
2.  **`auth.py`** uses `app.services.google` to construct the OAuth URL and **redirects** user to Google.
3.  **User** logs in on Google and grants permission.
4.  **Google** redirects user back to `GET /api/v1/auth/callback?code=...`.
5.  **`auth.py`** receives the `code`:
    *   Exchanges `code` for **Google Access Token**.
    *   Fetches user details (Email, Name, Avatar).
    *   **Upserts User** in PostgreSQL `users` table.
6.  **`security.py`** mints a **Colosseum JWT** signed with `SECRET_KEY`.
7.  **`auth.py`** redirects user to Frontend (e.g., `http://localhost:3000/auth/success?token=<JWT>`).

### **Scenario B: Accessing Protected Routes**

1.  **Frontend** sends request to `GET /api/v1/users/me` with header `Authorization: Bearer <JWT>`.
2.  **FastAPI** invokes `get_current_user` dependency in **`deps.py`**:
    *   Verifies signature of JWT.
    *   Extracts User ID (`sub`).
    *   Checks DB for existence and active status.
3.  **`users.py`** receives valid `User` object.
4.  Endpoint returns `User` object, serialized by **`app/schemas/user.py`** to JSON.

---

## 3. Infrastructure & Testing

*   **`alembic/`**: Database migration tool. Manages schema changes (version control for your DB).
*   **`docker-compose.yml`** (in `colosseum-infra`): Orchestrates the service along with PostgreSQL (`core-db`), Nginx Gateway, and other microservices.
*   **`tests/`**: Contains pytest suites.
    *   **`conftest.py`**: Sets up async test client and mocks.
    *   **`tests/api/v1/test_auth.py`**: Validates the OAuth flow by mocking Google's responses and the database session.
