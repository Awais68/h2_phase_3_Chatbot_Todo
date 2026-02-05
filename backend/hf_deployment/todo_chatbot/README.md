## Docker Setup

Run the Todo Evolution API and supporting services using Docker Compose for a consistent, containerized environment.

### Requirements
- **Docker** and **Docker Compose** installed
- No need for local Python or dependencies; all handled in containers
- Uses Python **3.13-slim** base image and the **uv** package manager for fast dependency management

### Environment Variables
Ensure a `.env` file exists in the project root with the following required variables:
- `DATABASE_URL`: PostgreSQL connection string (e.g., from Neon)
- `SECRET_KEY`: JWT secret key
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`: Used by the `postgres-db` service (defaults: `todo_db`, `todo_user`, `todo_pass`)

Refer to the [Environment Variables](#environment-variables) section for details.

### Build and Run

1. **Copy and configure your `.env` file**
   ```bash
   cp .env.example .env
   # Edit .env with your Neon DATABASE_URL and SECRET_KEY
   ```

2. **Start all services**
   ```bash
   docker compose up --build
   ```
   This will build and start:
   - `python-app`: Main FastAPI backend (exposes **port 8000**)
   - `python-src`: Alternate backend (also **port 8000**, for development/worker tasks)
   - `postgres-db`: PostgreSQL database (exposes **port 5432**)

3. **Access the API**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Special Configuration
- The Dockerfiles use the `uv` package manager for fast, reproducible Python environments.
- Healthchecks are enabled for all services (`/health` endpoint for API, `pg_isready` for PostgreSQL).
- All containers run as non-root users for improved security.
- The `python-src` service is available for development or worker tasks; customize as needed.
- To persist PostgreSQL data locally, uncomment the `volumes` section in `docker-compose.yml`.

### Ports
| Service      | Container Name | Host Port | Container Port |
|--------------|---------------|-----------|---------------|
| python-app   | python-app    | 8000      | 8000          |
| python-src   | python-src    | 8000      | 8000          |
| postgres-db  | postgres-db   | 5432      | 5432          |

---

For troubleshooting and advanced configuration, see the [Troubleshooting](#troubleshooting) and [Deployment](#deployment) sections below.