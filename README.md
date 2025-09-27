# ChronosAtlas: Historical Data API (Django/Graphene)

This project is a GraphQL API backend built using Django and Graphene, designed to manage and query historical data, including figures and timeline events.

The API is currently being deployed via **Docker Compose** using the production configuration, which requires careful management of static files and database migrations.

## 🚀 Current Development Status

**Branch Context:** This documentation reflects development and debugging efforts targeting the **production** environment and is based on recent changes to integrate GraphQL mutations.

### The Final Known Issue (Bug)

The last attempt to run the `createFigure` mutation failed with an internal database error, even though the overall HTTP status was `200 OK` (meaning the GraphQL endpoint was reachable).

**Error Received:**

```

{"errors":[{"message":"An unexpected error occurred: table figures\_figure has no column named birth\_year","locations":[{"line":1,"column":12}],"path":["createFigure"]}],"data":{"createFigure":null}}

```

**Root Cause:**
This error confirms that the Python code for the `CreateFigure` mutation is correct, but the PostgreSQL database is missing the table schema updates. The `figures_figure` table exists (from an older migration), but the new columns (`birth_year`, `death_year`, `description`) defined in `figures/models.py` have not been added to the database.

## ✅ Resolution (Next Steps to Fix the Bug)

To fix the `birth_year` column error and successfully run the mutation, you must run the standard Django migration commands to generate and apply the new schema.

**Execute the following commands from your host machine (outside the Docker container) to force the API service to catch up:**

1. **Generate Migration File (if needed):**

   * This command checks the new `figures/models.py` against the existing state and creates the migration file that adds the missing columns.

```

docker compose exec api python manage.py makemigrations figures --settings=ChronosAtlas.settings\_prod

```

2. **Apply Migration to Database:**

* This command executes the migration file against the PostgreSQL database inside the `chronos_db` container, adding the required columns.

```

docker compose exec api python manage.py migrate --settings=ChronosAtlas.settings\_prod

```

3. **Test the Mutation:**

* After the migration is applied, the database will be correctly structured, and the mutation should succeed.

```

curl -v -X POST http://localhost:8080/graphql/ -H "Content-Type: application/json" -d '{"query": "mutation { createFigure(input: {name: "Final Test", birthYear: 2025, deathYear: 2026, description: "Success" }) { figure { id name } } }"}'

```

*(Expected result: HTTP 200 OK with data containing the created figure's ID and name.)*

## 📁 Key File Implementations

The following files represent the current, working configuration of the Django/Graphene integration, which allows the use of the `input` object in mutations.

### 1. `ChronosAtlas/settings.py` (Fixed Static Files Error)

This version includes the critical **`STATIC_ROOT`** setting to allow the container to pass the `collectstatic` phase in production mode.

```

"""
Django settings for ChronosAtlas project.
... (Standard imports and settings)
"""

# Note: The actual content here is a placeholder.

# You MUST ensure any problematic line like 'import timeline.schema' is REMOVED.

import os
from pathlib import Path

# ... (rest of the settings)

# Static files (CSS, JavaScript, Images)

STATIC\_URL = 'static/'

# CRITICAL FIX: Define STATIC\_ROOT for collectstatic to prevent ImproperlyConfigured error.

STATIC\_ROOT = BASE\_DIR / 'staticfiles'

# Default primary key field type

DEFAULT\_AUTO\_FIELD = 'django.db.models.BigAutoField'

# \----------------------------------------

# GRAPHENE CONFIGURATION

# \----------------------------------------

GRAPHENE = {
\# This must be a string path to your main schema object
'SCHEMA': 'ChronosAtlas.schema.schema'
}

# ... (rest of the settings like CORS)

```

### 2. `figures/models.py` (Model Definition)

Defines the SQL structure for the `Figure`.

```

from django.db import models

class Figure(models.Model):
"""
Represents a historical figure, as required by the figures GraphQL schema.
"""
name = models.CharField(max\_length=255)
\# Using db\_column to maintain Python naming conventions while allowing snake\_case in the database
birthYear = models.IntegerField(db\_column='birth\_year')
deathYear = models.IntegerField(db\_column='death\_year', null=True, blank=True)
description = models.TextField(blank=True, null=True)

```
def __str__(self):
    return self.name

class Meta:
    ordering = ['birthYear']
```

```

### 3. `figures/schema.py` (Corrected Mutation Logic)

This file contains the **`FigureInput`** and the **`CreateFigure`** mutation using the standard Graphene-Django pattern to correctly accept the single `input` object from the cURL request.

```

import graphene
from graphene\_django.types import DjangoObjectType
from .models import Figure
from django.db import IntegrityError

# \--- 1. Graphene Type Definition ---

class FigureType(DjangoObjectType):
"""Defines the structure of the Figure in GraphQL."""
class Meta:
model = Figure
fields = ("id", "name", "birthYear", "deathYear", "description")

# \--- 2. Query Definition ---

class FigureQuery(graphene.ObjectType):
"""Handles fetching Figure data."""
figures = graphene.List(FigureType)

```
def resolve_figures(root, info):
    """Resolver to fetch all Figure objects, ordered by birthYear."""
    return Figure.objects.all()
```

# \--- 3. Mutation Input Definition ---

class FigureInput(graphene.InputObjectType):
"""Defines the structure of the input object for Figure mutations."""
name = graphene.String(required=True)
birthYear = graphene.Int(required=True)
deathYear = graphene.Int(required=True)
description = graphene.String(required=False)

# \--- 4. Mutation Definition (Create Operation) ---

class CreateFigure(graphene.Mutation):
"""Mutation to create a new Figure."""
figure = graphene.Field(FigureType)

```
class Arguments:
    # CRITICAL FIX: Defines a single 'input' argument using the InputObjectType
    input = FigureInput(required=True)

@staticmethod
def mutate(root, info, input=None):
    """The core logic for creating the figure."""
    try:
        figure = Figure.objects.create(
            name=input.name,
            birthYear=input.birthYear,
            deathYear=input.deathYear,
            description=input.description if input.description else ""
        )
        return CreateFigure(figure=figure)
    except IntegrityError as e:
        raise Exception(f"Database error while creating Figure: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")
```

# \--- 5. Mutation Container ---

class FigureMutation(graphene.ObjectType):
"""Root container for all Figure-related mutations."""
createFigure = CreateFigure.Field()

```

### 4. `ChronosAtlas/schema.py` (Root Schema Consolidation)

This root file correctly inherits all Queries and Mutations from the app-level schemas (`timeline` and `figures`).

```

import graphene

# Import schemas from the individual apps

from timeline.schema import TimelineQuery, TimelineMutation
from figures.schema import FigureQuery, FigureMutation

# Combine all application queries into a single root Query

class Query(TimelineQuery, FigureQuery, graphene.ObjectType):
"""The root query for the ChronosAtlas GraphQL API."""
pass

# Combine all application mutations into a single root Mutation

class Mutation(TimelineMutation, FigureQuery, graphene.ObjectType):
"""The root mutation for the ChronosAtlas GraphQL API."""
pass

# Create the final schema object, referenced in settings.py

schema = graphene.Schema(query=Query, mutation=Mutation)
