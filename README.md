# Chronos Atlas

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

## 🚀 Getting Started

For detailed instructions on setting up the development environment, running the application, and using the APIs, please refer to the **[Detailed Documentation](docs/README_DETAILED.md)**.