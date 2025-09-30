# Chronos Atlas

## 🌍 Overview

Chronos Atlas is a data-driven API designed to serve historical data for an interactive timeline visualization. It provides rich context on historical figures, their fields of work, and their intellectual influence, with a focus on high performance and scalability.

The project is containerized using **Docker** and **Docker Compose** for a consistent production environment.

## ✨ Key Features

*   **Dual API Support:** Provides both a flexible **GraphQL** API (via Graphene-Django) for complex queries and standard **REST** endpoints (via DRF) for simple data retrieval.
*   **Optimized Data Model:** Tracks figures, timeline events, and influence relationships with a schema optimized for time-series queries.
*   **Containerized Environment:** Uses Docker and Docker Compose for reproducible development and production setups.
*   **Modular Settings:** Cleanly separates configuration for development, production, and local environments.

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python, Django |
| **Database** | PostgreSQL |
| **GraphQL API** | Graphene-Django |
| **REST API** | Django REST Framework |
| **Deployment** | Docker, Gunicorn |

## 🚀 Getting Started (Development Environment)

This guide will get a local development instance of the project up and running.

### Prerequisites
* Docker
* Docker Compose

### 1. Environment Configuration
This project uses separate Docker Compose files for different environments. For local development, we will use `docker-compose.dev.yml`. This setup provides hot-reloading for code changes.

### 2. Build and Run the Services
From the project root, run the following command to build the images and start the `api` and `db` containers.
```bash
docker compose -f docker-compose.dev.yml up --build -d
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
