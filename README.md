## Running the Project with Docker

This project provides a full-stack environment using Docker and Docker Compose, with a Python backend, a TypeScript/Next.js frontend, and a Postgres database. The setup is tailored for this codebase and leverages project-specific Dockerfiles and configuration.

### Project-Specific Requirements

- **Backend**: Python 3.13 (from `python:3.13-slim`), dependencies managed via `uv` and `pyproject.toml`.
- **Frontend**: Node.js 22.13.1 (from `node:22.13.1-slim`), dependencies from `package.json`/`package-lock.json`.
- **Database**: Postgres (official `postgres:latest` image).

### Required Environment Variables

- **Backend**:
  - `PORT` (default: 8000)
  - Optionally, use a `.env` file in `./backend` for additional configuration (uncomment `env_file` in compose if used).
- **Frontend**:
  - `PORT` (default: 3000)
  - Optionally, use a `.env` file in `./frontend` for additional configuration (uncomment `env_file` in compose if used).
- **Database** (set in `docker-compose.yml`):
  - `POSTGRES_DB=todo_db`
  - `POSTGRES_USER=todo_user`
  - `POSTGRES_PASSWORD=todo_pass`

### Exposed Ports

- **Backend**: [http://localhost:8000](http://localhost:8000)
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Postgres**: [localhost:5432](localhost:5432)

### Build and Run Instructions

1. **Clone the repository and ensure Docker and Docker Compose are installed.**
2. *(Optional)* Create `.env` files in `./backend` and/or `./frontend` if you need to override defaults or provide secrets.
3. **Build and start all services:**

   ```sh
   docker compose up --build
   ```

   This will build the backend, frontend, and database containers as defined in the project-specific Dockerfiles and `docker-compose.yml`.

4. **Access the services:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - Postgres: `localhost:5432` (credentials as above)

### Special Configuration Notes

- **Healthchecks** are defined for both backend and database containers for robust startup and monitoring.
- **Persistent Database Storage**: To persist Postgres data between runs, uncomment the `volumes` section for `postgres-db` in `docker-compose.yml`.
- **Network**: All services are connected via the `app-network` Docker bridge network.
- **Non-root Users**: Both backend and frontend containers run as non-root users for improved security.
- **Backend dependencies** are installed using `uv` for fast, reproducible builds.
- **Frontend** builds Next.js and prunes dev dependencies for a lean production image.

---

*For more details on service-specific configuration, see the `README.md` files in `./backend` and `./frontend`.*
