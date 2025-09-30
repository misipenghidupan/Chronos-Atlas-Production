# Chronos Atlas: Comprehensive Execution Plan & Project Rules

This document is the central, living checklist and rulebook for building Chronos Atlas to MVP and beyond. Update as you progress.

---

## 1. Guiding Principles

- **Single Source of Truth:** Each config (e.g., DB settings, indexes) defined in only one place.
- **Environment Parity:** Dev mirrors prod (Docker, PostgreSQL, unified settings).
- **Clarity & Maintainability:** Code, docs, and structure must be clean, consistent, and easy for any developer.
- **Modern Docker Usage:** Always use `docker compose` (never `docker-compose`).
- **README Policy:** Keep all READMEs in sync and up to date, with clear audience and purpose.

---

## 2. Roadmap & To-Do List (MVP & Beyond)

### ✅ Foundation & Refactor (Complete)
- [x] Fix management command and restore GiST indexes.
- [x] Unify environment config (PostgreSQL, dj_database_url, settings).
- [x] Remove hardcoded settings, consolidate documentation.

### ⬜️ Pre-MVP: Core Functionality & Quality
- [ ] **Automated Test Suite:**
    - [ ] Fix failing GraphQL tests (ensure endpoint, schema, and test setup are correct).
    - [ ] Achieve 100% pass rate for all core model, API, and integration tests.
- [ ] **API Consistency:**
    - [ ] Review and document all REST and GraphQL endpoints.
    - [ ] Ensure all endpoints are covered by tests and docs.
- [ ] **Data Model Review:**
    - [ ] Audit models for normalization, constraints, and index coverage.
    - [ ] Add/adjust migrations as needed for MVP data requirements.
- [ ] **Fixtures & Sample Data:**
    - [ ] Ensure all fixtures load cleanly and cover MVP use cases.
- [ ] **Admin & Management:**
    - [ ] Review Django admin for usability and security.
    - [ ] Ensure all management commands are documented and tested.

### ⬜️ MVP Delivery
- [ ] **Frontend Simulator:**
    - [ ] Finalize and document usage of `frontend_simulator.html` for API testing.
- [ ] **Documentation:**
    - [ ] Update all READMEs and detailed docs for MVP state.
    - [ ] Add API usage examples and troubleshooting tips.
- [ ] **Deployment:**
    - [ ] Test production Docker Compose setup (`docker-compose.prod.yml`).
    - [ ] Document deployment, environment variables, and secrets handling.
- [ ] **Performance & Index Verification:**
    - [ ] Load larger sample data and verify GiST index usage in query plans.

### ⬜️ Post-MVP: Polish & Scale
- [ ] **ETL & Data Ingestion:**
    - [ ] Implement and document ETL pipeline (Wikidata, etc.).
- [ ] **Caching & Background Tasks:**
    - [ ] Integrate Redis and Celery for caching and ETL jobs.
- [ ] **Monitoring & Observability:**
    - [ ] Add logging, error tracking, and basic monitoring.
- [ ] **Security Review:**
    - [ ] Audit for secrets, permissions, and best practices.
- [ ] **Cloud/Production Launch:**
    - [ ] Prepare for cloud deployment (Docker registry, cloud DB, etc.).

---

## 3. Session Log

*Update this section as you complete major tasks or milestones.*
