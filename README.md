# Chronos Atlas

## 🌍 Overview

Chronos Atlas is a timeline-focused API designed to provide historical data on figures, their contributions (Fields), and their influence relationships. The API is built using **Django**, **Django REST Framework (DRF)**, **Graphene-Django (GraphQL)**, and **PostgreSQL**.

The project is containerized using **Docker** and **Docker Compose** for a consistent production environment.

## 🚀 Status: Milestone 0.3 Complete

The core infrastructure is fully operational, and the database is populated with initial data.

| Milestone | Status | Description |
| :--- | :--- | :--- |
| **0.1** | ✅ Complete | Docker, Database, and API connectivity verified. |
| **0.2** | ✅ Complete | Core database schema (`Figure`, `Field`, etc.) created via migrations. |
| **0.3** | ✅ Complete | **Initial MVP Data Loaded.** The database is populated with figures and relationships using the `load_mvp_data` management command. |

**Next Focus: Milestone 1.0 - API Implementation** (Implementing the GraphQL schema to expose the loaded data).

## 💻 Local Development Setup (Production Environment)

### Prerequisites

* Docker
* Docker Compose

### 1. File Setup

Ensure the following files are in place:

* **`docker-compose.prod.yml`**: Defines the services and critical volume mounts.
* **`.env.prod`**: Contains production environment variables (e.g., database credentials).
* **`data/historical_figures_normalized.csv`**: The data file needed for the initial load.

### 2. Startup

Build and start the services defined in the production compose file. This will spin up the `api` (Django) and `db` (PostgreSQL) containers.

```bash
docker compose -f docker-compose.prod.yml up -d
```

### 3\. Database Initialization & Data Load

The following steps set up the database schema and load the initial MVP dataset.

| Step | Command | Description |
| :--- | :--- | :--- |
| **a. Run Migrations** | `docker compose -f docker-compose.prod.yml run --rm api python manage.py migrate --settings=ChronosAtlas.settings_prod` | Creates all necessary tables (`Figure`, `Field`, `Influence`, etc.). |
| **b. Load Data** | `docker compose -f docker-compose.prod.yml run --rm api python manage.py load_mvp_data --settings=ChronosAtlas.settings_prod` | Populates the database with the initial 8 figures and their relationships. |

-----

## 🛑 Important Configuration Notes

### Database Credentials

Database credentials are read from `.env.prod`. They must match the configuration within `docker-compose.prod.yml`.

| Variable | Value |
| :--- | :--- |
| `DB_NAME` | `chronosatlas` |
| `DB_USER` | `chronosuser` |
| `DB_PASSWORD` | `chronospassword` |
| `DB_HOST` | `db` (The service name) |

### Volume Mounts

The following critical volume mounts ensure the application and data files are available inside the container:

  * `.:/app`: Maps the project root to the container's working directory.
  * `./data:/app/data`: Maps the local `./data` folder to the expected `/app/data` path for data loading scripts.

## 🧩 Environment Structure

### Django Settings
- `settings_base.py`: Shared settings for all environments.
- `settings_dev.py`: Development overrides (DEBUG=True, SQLite).
- `settings_prod.py`: Production overrides (DEBUG=False, PostgreSQL).
- `settings_default.py`: Default/local settings.

### Docker Compose Files
- `docker-compose.yml`: Default/local environment (uses `settings_default.py`).
- `docker-compose.dev.yml`: Development environment (uses `settings_dev.py`).
- `docker-compose.prod.yml`: Production environment (uses `settings_prod.py`).

### Environment Variable Files
- `.env`: Local/dev environment variables.
- `.env.prod`: Production environment variables.

### Usage
- Make sure to use the correct Docker Compose file and `.env` file for your environment.
- The legacy `settings.py` has been removed for clarity.

## 🧪 API Usage & Frontend Simulator

### GraphQL Endpoint
- URL: `http://localhost:8000/graphql/`
- Test queries and mutations using the built-in GraphiQL IDE or the included `frontend_simulator.html`.

### REST API Endpoints
- Figures: `http://localhost:8000/api/figures/`
- Timeline Events: `http://localhost:8000/api/timeline/`
- Influences: `http://localhost:8000/api/influences/`

### Frontend Simulator
Open `frontend_simulator.html` in your browser to test both GraphQL and REST endpoints interactively. It provides:
- GraphQL query editor and response viewer
- REST API selector and response viewer

### Sample Data
Sample fixtures are provided and loaded automatically:
- Figures: `figures/fixtures/sample_figures.json`
- Timeline Events: `timeline/fixtures/sample_timeline.json`

## ✅ Problems Solved This Session
- Modularized Django settings for dev/prod/default
- Fixed Docker Compose and environment variable issues
- Ensured static files are served in production (WhiteNoise)
- REST API endpoints return JSON, not templates
- GraphQL IDE and API endpoints are accessible
- Added sample data and frontend simulator for easy testing

## 📝 Next Steps & TODOs
- Expand GraphQL schema and mutations for full CRUD
- Add more sample data and fixtures
- Implement authentication and permissions
- Modernize admin UI (optional)
- Add automated tests for models and APIs
- Document API schema and usage in detail

## 📚 For Next Development Session
- Review this README and the frontend simulator
- Test all endpoints and sample data
- Continue with GraphQL/REST API feature development
- Refine admin and frontend as needed
