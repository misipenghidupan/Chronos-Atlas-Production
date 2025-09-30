# Chronos Atlas: Detailed Documentation

This document provides a comprehensive guide to the Chronos Atlas project, including setup, configuration, API usage, and development details.

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

### 3. Database Initialization & Data Load
The following steps set up the database schema and load the initial data.

| Step | Command | Description |
| :--- | :--- | :--- |
| **a. Run Migrations** | `docker exec chronosatlas_api_dev python manage.py migrate` | Creates all necessary tables (`Figure`, `Timeline`, etc.). |
| **b. Load Data** | `docker exec chronosatlas_api_dev python manage.py loaddata figures/fixtures/sample_figures.json` | Populates the database with sample figures. |
| | `docker exec chronosatlas_api_dev python manage.py loaddata timeline/fixtures/sample_timeline.json` | Populates the database with sample timeline events. |

---

## 🧩 Environment Structure

### Django Settings
- `settings_base.py`: Shared settings for all environments.
- `settings_dev.py`: Development overrides (DEBUG=True).
- `settings_prod.py`: Production overrides (DEBUG=False).
- `settings_default.py`: Default/local settings.

### Docker Compose Files
- `docker-compose.dev.yml`: Development environment.
- `docker-compose.prod.yml`: Production environment.

### Environment Variable Files
- `.env`: Local/dev environment variables.
- `.env.prod`: Production environment variables.

---

## 🧪 API Usage & Frontend Simulator

### GraphQL Endpoint
- URL: `http://localhost:8081/graphql/`
- Test queries and mutations using the built-in GraphiQL IDE.

### REST API Endpoints
- Figures: `http://localhost:8081/api/figures/`
- Timeline Events: `http://localhost:8081/api/timeline/`

### Frontend Simulator
Open `frontend/frontend_simulator.html` in your browser to test both GraphQL and REST endpoints interactively. It provides:
- GraphQL query editor and response viewer
- REST API selector and response viewer

---

## 🛠️ Development Details

### Multi-stage Dockerfile
We use a multi-stage `Dockerfile` to create optimized images. The `builder` stage installs dependencies and builds Python wheels, while the `final` stage creates a minimal runtime image, resulting in smaller image sizes and improved security.

### Entrypoint Script
The `scripts/entrypoint.sh` script is executed when the `api` container starts. It waits for the database to be ready and then runs the main container command.

### Checking Logs
Since the development server runs in detached (`-d`) mode, you can use the `docker compose logs` command to view its output.

**1. View all logs at once:**
To see a snapshot of logs from all services (`api` and `db`):
```bash
docker compose -f docker-compose.dev.yml logs
```

**2. Follow logs in real-time (most common):**
To stream logs live as they happen, use the `-f` or `--follow` flag. This is the best way to monitor your application.
```bash
docker compose -f docker-compose.dev.yml logs -f
```
*(Press `Ctrl+C` to stop streaming.)*

**3. View logs for a specific service:**
If you only need to see the logs from the Django `api` container:
```bash
docker compose -f docker-compose.dev.yml logs -f api
```
