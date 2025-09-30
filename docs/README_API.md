# Chronos Atlas Backend API Documentation

## Overview
This backend provides both GraphQL and REST API endpoints for accessing historical figures and timeline events. It is built with Django, Graphene-Django, and Docker Compose for easy development and deployment.

---

## 1. Running the Backend

- **Start with Docker Compose:**
  ```bash
  docker compose -f docker-compose.dev.yml up --build
  ```
- **Access the app:**
  - Django Admin: [http://localhost:8081/admin/](http://localhost:8081/admin/)
  - GraphQL API: [http://localhost:8081/graphql/](http://localhost:8081/graphql/)
  - Homepage: [http://localhost:8081/](http://localhost:8081/)

---

## 2. Data Models

### Figure
- `name`: string
- `slug`: string (unique)
- `wikidata_id`: string (unique)
- `summary`: text
- `birth_date`: date
- `death_date`: date
- `normalized_birth_year`: integer
- `normalized_death_year`: integer
- `instance_of_QIDs`: JSON list
- `fields`: ManyToMany to Field

### Field
- `name`: string (unique)

### TimelineEvent
- `title`: string
- `year`: integer
- `category`: string
- `description`: text

### Influence
- `influencer`: ForeignKey to Figure
- `influenced`: ForeignKey to Figure

---

## 3. GraphQL API

- **Endpoint:** `/graphql/`
- **Interactive IDE:** GraphiQL available at `/graphql/`

### Example Queries

#### Get All Figures
```graphql
query {
  allFigures {
    id
    name
    birthDate
    fields {
      name
    }
  }
}
```

#### Get All Timeline Events
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

#### Get All Influences
```graphql
query {
  allInfluences {
    influencer {
      name
    }
    influenced {
      name
    }
  }
}
```

### Example Mutations

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

---

## 4. REST API Endpoints

The following basic REST endpoints are available:

- **Figures List & Detail:**
  - `GET /api/figures/` — List all figures
  - `GET /api/figures/<id>/` — Get figure by ID

- **Timeline Events List & Detail:**
  - `GET /api/timeline/` — List all timeline events
  - `GET /api/timeline/<id>/` — Get timeline event by ID

- **Influences List & Detail:**
  - `GET /api/influences/` — List all influences
  - `GET /api/influences/<id>/` — Get influence by ID

---

## 5. Authentication
- The admin panel requires superuser login.
- API endpoints can be extended to require authentication as needed.

---

## 6. Development Notes
- All models and schema are defined in the `figures`, `timeline`, and `ChronosAtlas` apps.
- For REST API, Django REST Framework is recommended for advanced features.
- For GraphQL, use GraphiQL to explore the schema and test queries/mutations.

---

## 7. Contact
For questions or help, contact the backend maintainer or open an issue in the repository.
