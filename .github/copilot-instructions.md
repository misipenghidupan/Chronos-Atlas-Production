## Docker Command Usage Rule

- **Always use `docker compose` (with a space, not a dash) for all Docker-related commands.**
  - Do NOT use `docker-compose` (deprecated). Use `docker compose up`, `docker compose exec`, `docker compose build`, etc.
  - This applies to all documentation, scripts, and automation.
# Copilot Instructions for Chronos Atlas

## Project Overview
Chronos Atlas is a containerized Django/PostgreSQL project for serving historical data via GraphQL and REST APIs. It is optimized for time-series analysis and interactive timeline visualizations. The architecture is modular, with clear separation between core app domains (figures, timeline), settings, and environment configuration.

## Key Architectural Patterns
- **Dual API Layer:** Both GraphQL (Graphene-Django) and REST (DRF) are supported. Endpoints are defined in `schema.py` (GraphQL) and `api.py` (REST) within each app.
- **Data Model:** PostgreSQL with GiST indexes for efficient time-based queries. See `models.py` and migration files in each app for schema details.
- **Settings Management:** Environment-specific settings are split across `settings_base.py`, `settings_dev.py`, `settings_prod.py`, and `settings_default.py`.
- **Containerization:** All development and production workflows use Docker Compose. Multi-stage Dockerfile builds are used for optimized images.

## Developer Workflows
- **Start Dev Environment:**
  ```bash
  docker compose -f docker-compose.dev.yml up --build -d
  ```
- **Run Migrations & Load Data:**
  ```bash
  docker exec chronosatlas_api_dev python manage.py migrate
  docker exec chronosatlas_api_dev python manage.py loaddata figures/fixtures/sample_figures.json
  docker exec chronosatlas_api_dev python manage.py loaddata timeline/fixtures/sample_timeline.json
  ```
- **Check Logs:**
  ```bash
  docker compose -f docker-compose.dev.yml logs -f
  # Or for just the API:
  docker compose -f docker-compose.dev.yml logs -f api
  ```
- **Test APIs:**
  - GraphQL: [http://localhost:8081/graphql/](http://localhost:8081/graphql/)
  - REST: [http://localhost:8081/api/figures/], [http://localhost:8081/api/timeline/]
  - Frontend Simulator: Open `frontend/frontend_simulator.html` in a browser

## Project-Specific Conventions
- **App Structure:** Each domain (e.g., `figures`, `timeline`) is a Django app with its own models, schema, API, filters, and tests.
- **Fixtures:** Sample data is loaded from JSON files in each app's `fixtures/` directory.
- **Management Commands:** Custom commands (e.g., `verify_indexes.py`) are in `management/commands/` within each app.
- **Settings Import:** Always import from `settings_base.py` and override as needed per environment.
- **Entrypoint:** The `scripts/entrypoint.sh` script ensures DB readiness before starting the app.

## Integration & External Dependencies
- **Database:** PostgreSQL with advanced indexing (see `migrations/` for index setup).
- **Data Source:** Wikidata (SPARQL) is the intended source for large-scale data ingestion (future phases).
- **Caching/ETL:** Redis and Celery are planned for production (see docs for roadmap).

## References
- [Detailed Docs](../docs/README_DETAILED.md)
- [Architecture Blueprint](../docs/Chronos-Atlas/ARCHITECTURE_BLUEPRINT.md)
- [Data Flow & Scaling](../docs/Chronos-Atlas/DATA_FLOW_AND_SCALING.md)
- [Execution Roadmap](../docs/Chronos-Atlas/EXECUTION_ROADMAP.md)

**For AI agents:**
- Prefer using Docker Compose for all workflows.
- Follow the modular app structure and settings conventions.
- Reference fixtures and management commands for data and schema operations.
- When in doubt, check the detailed documentation and blueprints in `/docs/Chronos-Atlas/`.

---

## Project Rules & To-Do List (AI Agent Reference)

### Guiding Principles

## README Synchronization & Documentation Rules

- **Multiple README Policy:**
  - `ChronosAtlas/README.md` is the high-level, user-facing overview for the main API/service repository. It should be concise, focused on onboarding, and always link to detailed docs.
  - `docs/Chronos-Atlas/README.md` is the technical/blueprint README for the architecture, roadmap, and deep-dive documentation. It should provide context, rationale, and links to all technical blueprints.
  - Keep both READMEs in sync regarding project status, stack, and key links, but tailor content to their audience and purpose.
  - When updating one README, review the other for consistency and update hyperlinks, status tables, and stack descriptions as needed.
  - Always update or add hyperlinks in both READMEs if file locations or documentation structure changes.

**For AI agents:**
- When making changes to project structure, documentation, or status, check both READMEs and update as appropriate.
1. **Fix Management Command Error:** Ensure `figures/management/commands/verify_indexes.py` is implemented and working.
2. **Restore & Verify Indexes:** Confirm GiST indexes are active in PostgreSQL; resolve model/migration conflicts.
3. **Unify Environment Config:** Use PostgreSQL in all environments; settings via `dj_database_url`; `manage.py` must respect `DJANGO_SETTINGS_MODULE`.
4. **Consolidate Documentation:** Main `README.md` = high-level overview; `docs/README_DETAILED.md` = setup/tech details; remove obsolete docs.
5. **Final Verification:** Run all tests and review changes before commit.

*Update this list as tasks are completed or new issues are found. Log major changes for traceability.*
