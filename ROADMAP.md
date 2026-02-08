# Colosseum Core Roadmap

This document outlines the planned features and improvements for the Identity Provider service.

## 🏁 Phase 1: Foundation (Completed)
- [x] Initial FastAPI project structure.
- [x] Google OAuth 2.0 integration via Authlib.
- [x] JWT issuance and validation.
- [x] PostgreSQL database integration (Async).
- [x] User Profile "upsert" logic.
- [x] Basic test suite.

## 🛠 Phase 2: Security & Operations (In Progress)
- [ ] **RBAC (Role Based Access Control)**: Define granular roles (Admin, Moderator, Player).
- [ ] **Token Refresh**: Implement refresh token logic for longer-lived sessions.
- [ ] **API Rate Limiting**: Prevent abuse of the auth endpoints.
- [ ] **Enhanced Logging**: Structured logging for auth events (audit trail).

## 🚀 Phase 3: Extended Features (Planned)
- [ ] **Profile Customization**: Allow users to set custom display names separate from Google.
- [ ] **Multi-provider Support**: Add support for GitHub or Discord login.
- [ ] **Internal SDK**: Create a Python/JS client library for other services to easily verify Colosseum JWTs.
- [ ] **Admin Dashboard**: Basic UI to manage users and roles.
