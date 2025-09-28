# 📚 ChronosAtlas API

A Django/Graphene-based GraphQL API for managing historical figures and timeline events, deployed using Docker and Docker Compose.

## 🚀 Current Project Status (Production Ready)

The application is currently **stable and fully deployed** in a Dockerized environment using the `docker-compose.prod.yml` file.

  * **Core Feature:** CRUD operations are fully functional for the **`TimelineEvent`** model and the **`Figure`** model via the GraphQL endpoint.
  * **Deployment:** The application successfully handles PostgreSQL database connection, runs migrations upon startup, collects static files, and serves the API via Gunicorn on port **8080**.

## ⚙️ Core Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend** | Python 3.11, Django 4.x | Web framework |
| **GraphQL** | Graphene-Django | Schema and API exposure |
| **Database** | PostgreSQL | Data persistence |
| **Containerization** | Docker, Docker Compose | Development and Production deployment |
| **Web Server** | Gunicorn | Production WSGI server |

## 🛠️ Deployment and Usage

### Prerequisites

  * Docker and Docker Compose installed on your host machine.
  * The project directory (`ChronosAtlas`) containing the `Dockerfile`, `docker-compose.prod.yml`, and application code.

### 1\. Launch the Stack (Build, Migrate, and Run)

This command builds the final image, pulls the PostgreSQL image, and starts both services in detached mode. The custom `entrypoint.sh` will ensure all migrations are applied.

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

### 2\. Verify Health

Wait about 15 seconds for the database and application to fully initialize, then check the running containers:

```bash
docker ps
```

You should see both `chronos_api` and `chronos_db` running.

### 3\. Test the GraphQL Endpoint

The API is available at `http://localhost:8080/graphql/`. Use a cURL command (or a tool like Insomnia/Postman) to perform a test mutation:

```bash
curl -X POST http://localhost:8080/graphql/ \
     -H 'Content-Type: application/json' \
     --data-raw '{
         "query": "mutation createEvent($input: TimelineEventInput!) { createTimelineEvent(input: $input) { timelineEvent { id title year category description } } }",
         "variables": {
             "input": {
                 "title": "Battle of Thermopylae",
                 "year": -480,
                 "category": "Military Conflict",
                 "description": "A battle in the Greco-Persian Wars where a small force of Greeks held a pass against a much larger Persian army."
             }
         }
     }'
```

### 4\. Shut Down

To stop and remove containers, networks, and ephemeral volumes:

```bash
docker compose -f docker-compose.prod.yml down
```

-----

## ⚠️ Known Issues and Resolved Debugging

This section highlights crucial configuration steps that were required to achieve the current stable state.

### Resolved Issues

| Issue | Resolution |
| :--- | :--- |
| **Database Connection Failure** | Verified and ensured the `DATABASE_URL` format was correct (`postgres://user:pass@host:port/name`). |
| **Table Not Found Error** | The initial fix required manually overriding the container's entrypoint to successfully generate and commit missing local migration files (`0001_initial.py` for `figures` and `timeline`). |
| **`ImproperlyConfigured`** | Ensured the `DATABASE_URL` environment variable was correctly passed to the temporary container when running one-off commands like `makemigrations`. |
| **Gunicorn Connection Reset** | Resolved a crash likely caused by the database issues, confirming that the application now starts and services requests without error. |

-----

## 🗓️ Future Plans and Roadmap

1.  **Authentication and Authorization:** Implement Django's built-in user system and integrate it with GraphQL using Graphene.
2.  **Media Storage:** Set up Amazon S3 or a similar cloud storage solution for user-uploaded figure images, using Django Storages.
3.  **Client Application:** Develop a frontend client (e.g., React or Vue) to consume the GraphQL API.
4.  **Testing Suite:** Implement unit and integration tests for all models and resolvers.

-----

## 💻 Code Changes Included in This Update

  * New migration files: `figures/migrations/0001_initial.py` and `timeline/migrations/0001_initial.py`.
  * Any necessary changes to the `Dockerfile`, `docker-compose.prod.yml`, or `entrypoint.sh` related to the debugging process (e.g., ensuring `migrate` runs correctly).
