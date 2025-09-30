# Chronos Atlas: Detailed Documentation

This document provides detailed technical information about the project's environment, configuration, and API usage.

## 🧩 Environment Structure

The project is configured to support multiple environments through a modular structure.

### Django Settings
- **`settings_base.py`**: Contains settings common to all environments.
- **`settings_dev.py`**: Overrides for local development (`DEBUG=True`, hot-reloading).
- **`settings_prod.py`**: Overrides for production (`DEBUG=False`, Gunicorn, security settings).
- **`settings_default.py`**: A fallback or local configuration.

### Docker Compose Files
- **`docker-compose.dev.yml`**: For the local development environment. Uses Django's development server for hot-reloading.
- **`docker-compose.prod.yml`**: For the production environment. Uses Gunicorn for a robust, multi-worker setup.
- **`docker-compose.yml`**: A default configuration, typically used for local setup.

### Environment Variable Files
- **`.env`**: Contains local/development environment variables.
- **`.env.prod`**: Contains production environment variables.

---

## 🛑 Production Environment Notes

### Database Credentials

In the production environment (`docker-compose.prod.yml`), database credentials are read from the `.env.prod` file. They must match the configuration within the compose file.

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

---

## 🧪 API Usage & Frontend Simulator

### GraphQL Endpoint
- **URL (Dev):** `http://localhost:8081/graphql/`
- **URL (Prod):** `http://localhost:8080/graphql/`
- **Testing:** Use the built-in GraphiQL IDE or the included `frontend/frontend_simulator.html`.

### REST API Endpoints
- **Figures:** `/api/figures/`
- **Timeline Events:** `/api/timeline/`
- **Influences:** `/api/influences/`

### Frontend Simulator
Open `frontend/frontend_simulator.html` in your browser to test both GraphQL and REST endpoints interactively. It provides:
- GraphQL query editor and response viewer
- REST API selector and response viewer