---

## 🏁 Final MVP Review & PR Template

### Final Summary

Chronos Atlas MVP is complete:
- All core APIs, models, and automation are implemented and tested.
- Documentation is up to date for onboarding, deployment, and troubleshooting.
- Sample data and GiST indexes are loaded and verified.
- CI, pre-commit, and PR automation are enforced.
- All MVP checklist items are complete in `PROJECT_EXECUTION_PLAN.md`.

### PR Preparation Checklist

- [x] All code passes tests and linting (pre-commit, CI).
- [x] All documentation is up to date and clear.
- [x] All environment and deployment instructions are accurate.
- [x] No secrets or sensitive data are committed.
- [x] All MVP checklist items are complete in `PROJECT_EXECUTION_PLAN.md`.
- [x] Branch is up to date with `dev-stage` and ready for PR.

### PR Body Template

```
## Chronos Atlas MVP Delivery

### What’s included
- All core APIs (GraphQL, REST), models, and management commands
- Docker Compose (dev/prod), environment parity, and automation
- Pre-commit, CI, and PR workflow
- Complete documentation (README, detailed docs, onboarding, troubleshooting)
- Sample data and GiST index verification

### How to test
1. Clone repo and run `pip install pre-commit && pre-commit install`
2. Start dev: `docker compose -f docker-compose.dev.yml up --build -d`
3. Run tests: `make test`
4. Try API endpoints: `/graphql/`, `/api/figures/`, `/api/timeline/`
5. Review docs in `README.md` and `docs/README_DETAILED.md`

### Checklist
- [ ] All tests pass
- [ ] All docs up to date
- [ ] No secrets committed
- [ ] Ready for review/merge
```

# Chronos Atlas: Detailed Documentation

> **MVP Status:** This project is at MVP (Minimum Viable Product) stage. All core APIs, data models, and automation are production-ready. See [PROJECT_EXECUTION_PLAN.md](PROJECT_EXECUTION_PLAN.md) for roadmap.

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


## 🧪 API Usage & Examples

### GraphQL Endpoint
- URL: `http://localhost:8081/graphql/`
- Test queries and mutations using the built-in GraphiQL IDE.

#### Example Query
```graphql
query {
	allFigures {
		edges {
			node {
				id
				name
				slug
			}
		}
	}
}
```

#### Example Mutation
```graphql
mutation {
	createFigure(input: {
		name: "Ada Lovelace"
		slug: "ada-lovelace"
		wikidataId: "Q7259"
		normalizedBirthYear: 1815
		normalizedDeathYear: 1852
		summary: "Pioneer of computing."
	}) {
		figure {
			id
			name
		}
	}
}
```

### REST API Endpoints
- Figures: `http://localhost:8081/api/figures/`
- Timeline Events: `http://localhost:8081/api/timeline/`

#### Example (GET)
```bash
curl http://localhost:8081/api/figures/
```

#### Example (POST)
```bash
curl -X POST http://localhost:8081/api/figures/ \
	-H 'Content-Type: application/json' \
	-d '{"name": "Ada Lovelace", "slug": "ada-lovelace", ...}'
```

---

## 🛠️ Troubleshooting & Tips

- **Docker Compose fails to start:** Ensure ports 8081/5432 are free and Docker is running.
- **Migrations fail:** Try `docker compose down -v` to reset volumes, then re-run migrations.
- **Tests fail on CI:** Run `make test` locally and check `.pre-commit-config.yaml` for linting issues.
- **API returns 500:** Check logs with `docker compose logs api`.

---

## 🔄 PR, CI, and Code Quality Workflow

- All code must pass pre-commit hooks and CI before merge.
- PRs require review and must be up-to-date with `dev-stage` or `main`.
- See `.github/pull_request_template.md` for PR checklist.

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

---

## 🚢 Deployment, Environment Variables & Secrets Handling

### Deployment Overview

- **Development:**
	- Use `docker compose -f docker-compose.dev.yml up --build -d`.
	- Exposes API on [http://localhost:8081](http://localhost:8081).
	- Uses `.env` for environment variables.
- **Production:**
	- Use `docker compose -f docker-compose.prod.yml up --build -d`.
	- Exposes API on [http://localhost:8080](http://localhost:8080).
	- Uses `.env.prod` for environment variables.
	- Runs with `DEBUG=False` and production settings.

### Environment Variable Files

- `.env`: Used for local/dev. Contains Django secret key, DB credentials, allowed hosts, CORS, etc.
- `.env.prod`: Used for production. Contains secure Django secret key, production DB credentials, and settings overrides.

**Never commit real secrets or production keys to version control.**

#### Example `.env` (development)
```env
SECRET_KEY=your-dev-secret-key
POSTGRES_DB=chronosatlas
POSTGRES_USER=chronosuser
POSTGRES_PASSWORD=chronospassword
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

#### Example `.env.prod` (production)
```env
DJANGO_SECRET_KEY=your-very-long-production-secret
DJANGO_SETTINGS_MODULE=ChronosAtlas.settings_prod
DJANGO_ENV=production
DB_NAME=chronosatlas
DB_USER=chronosuser
DB_PASSWORD=chronospassword
DB_HOST=db
DB_PORT=5432
```

### Secrets Handling

- **Never** hardcode secrets in code or Dockerfiles.
- Use environment variables for all secrets (Django secret key, DB password, etc.).
- Use `.env` and `.env.prod` for local and production secrets, respectively.
- For cloud deployment, use your platform’s secret manager or environment variable injection.

### Additional Security Tips
- Always set `DEBUG=False` in production.
- Restrict `ALLOWED_HOSTS` to your real domain(s) in production.
- Rotate secrets regularly and never share them in public channels.

---

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
