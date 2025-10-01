
# Chronos Atlas

![MVP Status](https://img.shields.io/badge/status-MVP-green)


## 🌍 Overview

Chronos Atlas is a high-performance API designed to serve historical data for interactive timeline visualizations. It provides rich, contextual information about historical figures, their work, and their influence on the world.

The project is fully containerized using **Docker** and **Docker Compose**, ensuring a consistent and reproducible environment for both development and production.

## ✨ Key Features

*   **Dual API Support:** Offers both a flexible **GraphQL** API for complex, nested queries and standard **REST** endpoints for straightforward data retrieval.
*   **Optimized for Performance:** Utilizes a PostgreSQL database with a data model specifically designed for efficient time-series analysis.
*   **Containerized & Reproducible:** Docker-based setup guarantees environment parity and simplifies deployment.
*   **Clean & Modular Architecture:** Features a clear separation of settings, a modular application structure, and a focus on maintainability.

## 🛠️ Technology Stack

| Layer         | Technology            |
| :------------ | :-------------------- |
| **Backend**   | Python, Django        |
| **Database**  | PostgreSQL with GiST  |
| **GraphQL API** | Graphene-Django       |
| **REST API**    | Django REST Framework |
| **Deployment**  | Docker, Gunicorn      |


## 🚀 Quickstart

### Development
```bash
docker compose -f docker-compose.dev.yml up --build -d
```
Then visit [http://localhost:8081/graphql/](http://localhost:8081/graphql/) for GraphQL or `/api/figures/` for REST.

### Production
```bash
docker compose -f docker-compose.prod.yml up --build -d
```
API will be available at [http://localhost:8080](http://localhost:8080).

---

## 🔐 Deployment, Environment Variables & Secrets

- All secrets (Django secret key, DB password, etc.) are managed via `.env` (dev) and `.env.prod` (prod).
- Never commit real secrets to version control.
- See [Detailed Documentation](docs/README_DETAILED.md#deployment-environment-variables--secrets-handling) for full details and security tips.

---

For full setup, see [Detailed Documentation](docs/README_DETAILED.md).

## 🤝 Contributing

- Run `pip install pre-commit && pre-commit install` after cloning.
- All code is auto-formatted and linted before commit.
- PRs require passing CI and review before merge.
- See `.github/pull_request_template.md` for PR guidelines.

## 🧪 CI/CD

All pushes and PRs are tested automatically via GitHub Actions (`.github/workflows/ci.yml`).

---

For detailed instructions on setup, API usage, troubleshooting, and the final MVP review & PR template, see the **[Detailed Documentation](docs/README_DETAILED.md)**.