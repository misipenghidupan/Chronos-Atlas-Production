# Docker & Git Tips for Chronos Atlas

This guide covers essential Docker, Git, and Makefile commands for developing, testing, and maintaining Chronos Atlas. It also includes troubleshooting tips, workflow best practices, and advanced usage.

---

## 🚀 Quick Start Workflow

1. **Start all services:**
   ```sh
   make up
   # or
   docker compose -f docker-compose.dev.yml up --build -d
   ```
2. **Run migrations:**
   ```sh
   make migrate
   # or
   docker compose -f docker-compose.dev.yml exec api python manage.py migrate
   ```
3. **Run tests:**
   ```sh
   make test
   # or
   docker compose -f docker-compose.dev.yml exec api python manage.py test
   ```
4. **Run pre-commit hooks:**
   ```sh
   docker compose -f docker-compose.dev.yml exec api pre-commit run --all-files
   ```
5. **Stop all services:**
   ```sh
   make down
   # or
   docker compose -f docker-compose.dev.yml down
   ```

---

## 🐳 Docker Compose Commands

- **Build and start services:**
  ```sh
  docker compose -f docker-compose.dev.yml up --build -d
  ```
- **Stop services:**
  ```sh
  docker compose -f docker-compose.dev.yml down
  ```
- **View logs:**
  ```sh
  docker compose -f docker-compose.dev.yml logs -f api
  ```
- **Run Django management commands:**
  ```sh
  docker compose -f docker-compose.dev.yml exec api python manage.py <command>
  # Examples:
  docker compose -f docker-compose.dev.yml exec api python manage.py migrate
  docker compose -f docker-compose.dev.yml exec api python manage.py test
  docker compose -f docker-compose.dev.yml exec api python manage.py shell
  ```
- **Run pre-commit hooks:**
  ```sh
  docker compose -f docker-compose.dev.yml exec api pre-commit run --all-files
  ```

---

## 🛠️ Makefile Shortcuts

The `Makefile` provides convenient shortcuts for common Docker Compose tasks:

- `make up` — Start all services (build if needed, run in background)
- `make down` — Stop all services
- `make test` — Run Django tests in the container
- `make logs` — View logs for the API service
- `make migrate` — Run Django migrations
- `make shell` — Open a Django shell in the container

---

## 🧑‍💻 Git Safe Directory in Docker

If you see errors like:

```
fatal: detected dubious ownership in repository at '/app'
```

This is because Docker runs as a different user than your host. The entrypoint script automatically runs:

```sh
git config --global --add safe.directory /app
```

so you do not need to do this manually.

---

## 🧩 Advanced Usage & Troubleshooting

- **Rebuild the Docker image after changing dependencies or Dockerfile:**
  ```sh
  docker compose -f docker-compose.dev.yml build
  ```
- **Restart services after a rebuild:**
  ```sh
  docker compose -f docker-compose.dev.yml up -d
  ```
- **Check if .git is mounted in the container:**
  ```sh
  docker compose -f docker-compose.dev.yml exec api ls -la /app/.git
  ```
- **Check git status inside the container:**
  ```sh
  docker compose -f docker-compose.dev.yml exec api git status
  ```
- **Run a custom Django management command:**
  ```sh
  docker compose -f docker-compose.dev.yml exec api python manage.py <yourcommand>
  ```
- **Run a bash shell inside the container:**
  ```sh
  docker compose -f docker-compose.dev.yml exec api bash
  ```

---

## 📝 Best Practices

- **Always run all development, debugging, tests, pre-commit hooks, and management commands inside Docker containers.**
- **Keep your Docker images up to date** by rebuilding after changes to dependencies or the Dockerfile.
- **Use Makefile shortcuts** for common tasks to save time and avoid mistakes.
- **Check the [Execution Plan](docs/PROJECT_EXECUTION_PLAN.md) and [Main README](README.md) for project rules and onboarding.**
- **If you encounter permission or git errors, check the Docker & Git Tips section first.**

---

For more, see the [Execution Plan](docs/PROJECT_EXECUTION_PLAN.md), [Main README](README.md), and other docs in the navigation.
