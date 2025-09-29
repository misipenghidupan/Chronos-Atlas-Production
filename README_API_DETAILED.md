# Chronos Atlas Backend: Detailed API Documentation

## Overview
This backend provides both GraphQL and REST API endpoints for historical figures and timeline events. It is built with Django, Graphene-Django, Django REST Framework, and Docker Compose.

---

## 1. Running the Backend
- **Start with Docker Compose:**
  ```bash
  docker compose -f docker-compose.dev.yml up --build
  ```
- **Access the app:**
  - Django Admin: [http://localhost:8081/admin/](http://localhost:8081/admin/)
  - GraphQL API: [http://localhost:8081/graphql/](http://localhost:8081/graphql/)
  - REST API Root: [http://localhost:8081/api/](http://localhost:8081/api/)
  - Homepage: [http://localhost:8081/](http://localhost:8081/)

---

## 2. Data Models

### Figure
| Field                | Type    | Description                       |
|---------------------|---------|-----------------------------------|
| id                  | int     | Unique identifier                 |
| name                | string  | Name of the figure                |
| slug                | string  | URL-friendly unique identifier    |
| wikidata_id         | string  | Wikidata unique ID                |
| summary             | text    | Short description                 |
| birth_date          | date    | Birth date                        |
| death_date          | date    | Death date                        |
| normalized_birth_year | int   | Birth year (for timeline)         |
| normalized_death_year | int   | Death year (for timeline)         |
| instance_of_QIDs    | list    | List of Wikidata QIDs             |
| fields              | list    | Related fields (ManyToMany)       |

### Field
| Field | Type   | Description         |
|-------|--------|---------------------|
| id    | int    | Unique identifier   |
| name  | string | Field name (unique) |

### TimelineEvent
| Field      | Type    | Description         |
|------------|---------|---------------------|
| id         | int     | Unique identifier   |
| title      | string  | Event title        |
| year       | int     | Year of event      |
| category   | string  | Event category     |
| description| text    | Event description  |

### Influence
| Field      | Type    | Description         |
|------------|---------|---------------------|
| id         | int     | Unique identifier   |
| influencer | Figure  | Influencer figure   |
| influenced | Figure  | Influenced figure   |

---

## 3. GraphQL API
- **Endpoint:** `/graphql/`
- **Interactive IDE:** GraphiQL available at `/graphql/`

### Main Queries
#### List All Figures
```graphql
query {
  allFigures {
    id
    name
    slug
    wikidataId
    summary
    birthDate
    deathDate
    normalizedBirthYear
    normalizedDeathYear
    instanceOfQIDs
    fields {
      id
      name
    }
  }
}
```
#### List All Timeline Events
```graphql
query {
  allTimelineEvents {
    id
    title
    year
    category
    description
  }
}
```
#### List All Influences
```graphql
query {
  allInfluences {
    id
    influencer {
      id
      name
    }
    influenced {
      id
      name
    }
  }
}
```

### Main Mutations
#### Create a Figure
```graphql
mutation {
  createFigure(input: {
    name: "Marie Curie",
    slug: "marie-curie",
    wikidataId: "Q7186",
    summary: "Chemist and physicist",
    birthDate: "1867-11-07",
    deathDate: "1934-07-04",
    normalizedBirthYear: 1867,
    normalizedDeathYear: 1934,
    instanceOfQIDs: ["Q5"]
  }) {
    figure {
      id
      name
    }
  }
}
```
#### Create a Timeline Event
```graphql
mutation {
  createTimelineEvent(input: {
    title: "Moon Landing",
    year: 1969,
    category: "Space",
    description: "Apollo 11 landed on the moon."
  }) {
    timelineEvent {
      id
      title
    }
  }
}
```
#### Create an Influence
```graphql
mutation {
  createInfluence(input: {
    influencerId: 1,
    influencedId: 2
  }) {
    influence {
      id
      influencer {
        name
      }
      influenced {
        name
      }
    }
  }
}
```

---

## 4. REST API Endpoints

All endpoints are under `/api/` and follow standard REST conventions.

### Figures
- `GET /api/figures/` — List all figures
- `POST /api/figures/` — Create a new figure
- `GET /api/figures/<id>/` — Retrieve a figure by ID
- `PUT /api/figures/<id>/` — Update a figure
- `PATCH /api/figures/<id>/` — Partially update a figure
- `DELETE /api/figures/<id>/` — Delete a figure

#### Example Request
```http
GET /api/figures/
```
#### Example Response
```json
[
  {
    "id": 1,
    "name": "Albert Einstein",
    "slug": "albert-einstein",
    "wikidata_id": "Q937",
    "summary": "Physicist",
    "birth_date": "1879-03-14",
    "death_date": "1955-04-18",
    "normalized_birth_year": 1879,
    "normalized_death_year": 1955,
    "instance_of_QIDs": ["Q5"],
    "fields": [{"id": 1, "name": "Science"}]
  }
]
```

### Timeline Events
- `GET /api/timeline/` — List all timeline events
- `POST /api/timeline/` — Create a new timeline event
- `GET /api/timeline/<id>/` — Retrieve a timeline event by ID
- `PUT /api/timeline/<id>/` — Update a timeline event
- `PATCH /api/timeline/<id>/` — Partially update a timeline event
- `DELETE /api/timeline/<id>/` — Delete a timeline event

### Influences
- `GET /api/influences/` — List all influences
- `POST /api/influences/` — Create a new influence
- `GET /api/influences/<id>/` — Retrieve an influence by ID
- `PUT /api/influences/<id>/` — Update an influence
- `PATCH /api/influences/<id>/` — Partially update an influence
- `DELETE /api/influences/<id>/` — Delete an influence

---

## 5. Authentication
- The admin panel requires superuser login.
- API endpoints are open by default but can be secured with authentication (see Django REST Framework docs).

---

## 6. Error Handling
- Standard HTTP status codes are used:
  - `200 OK` for successful GET/PUT/PATCH/DELETE
  - `201 Created` for successful POST
  - `400 Bad Request` for invalid input
  - `404 Not Found` for missing resources
  - `500 Internal Server Error` for server issues
- Error responses are returned in JSON format.

---

## 7. Development Notes
- All models and schema are defined in the `figures`, `timeline`, and `ChronosAtlas` apps.
- For REST API, Django REST Framework is used for serialization and routing.
- For GraphQL, use GraphiQL to explore the schema and test queries/mutations.
- Example data and test cases are available in `figures/tests.py` and `timeline/tests.py`.

---

## 8. Contact
For questions or help, contact the backend maintainer or open an issue in the repository.
