# Task API

A **FastAPI CRUD API** for managing a to-do list, backed by **PostgreSQL** and fully containerized with **Docker Compose**.

This project extends the previous CRUD implementation by replacing the temporary storage layer with a real PostgreSQL repository. The application and database run together as a single Docker Compose stack, while PostgreSQL data is persisted through a Docker volume.



## Features

* FastAPI backend
* Full CRUD operations
* PostgreSQL database
* PostgreSQL repository layer
* Service/repository architecture
* Input validation
* Correct HTTP status codes
* JSON responses
* Health-check endpoint
* Interactive Swagger UI
* Dockerized application
* Docker Compose stack
* Persistent PostgreSQL volume
* Environment-based database configuration
* Git/GitHub version control

## Architecture

The application follows a layered architecture:

```text
HTTP Request
     ↓
FastAPI Routes
     ↓
Task Service
     ↓
Task Repository Interface
     ↓
PostgreSQL Repository
     ↓
PostgreSQL
```

The routes and service layer do not contain PostgreSQL-specific code.

The PostgreSQL implementation is isolated inside:

```text
app/repositories/postgres_task_repository.py
```

This demonstrates the main architectural goal of the assignment: **switching the storage implementation without changing the service or route logic.**

## Project Structure

```text
CraudAPI/

├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── postgres_task_repository.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── tasks.py
│   │
│   └── services/
│       ├── __init__.py
│       └── task_service.py
│
├── sql/
│   └── init.sql
│
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── swagger.png
```

## Requirements

For the Dockerized setup:

* Docker
* Docker Compose

For local development without Docker:

* Python 3.10+
* pip
* Git

## Environment Variables

The application uses environment variables for the PostgreSQL connection.

Create a `.env` file in the project root:

```env
POSTGRES_DB=taskdb
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=taskpassword
DATABASE_URL=postgresql://taskuser:taskpassword@db:5432/taskdb
```

A `.env.example` file is committed to the repository so that the required variables are documented without exposing the actual environment file.

The real `.env` file is ignored by Git.

## Running the Application

The entire stack can be started with one command.

From the project root:

```powershell
docker compose up --build
```

Docker Compose starts:

```text
FastAPI application
        +
PostgreSQL database
```

The application will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

API health check:

```text
http://localhost:8000/health
```

## Docker Compose

The application and PostgreSQL database are defined in `docker-compose.yml`.

The PostgreSQL service uses the official PostgreSQL image and stores its data in a named Docker volume:

```yaml
volumes:
  postgres_data:
```

The database is also given a health check so that the FastAPI application waits for PostgreSQL to become ready before starting.

The database initialization script is mounted from:

```text
sql/init.sql
```

into PostgreSQL's initialization directory.

## Database Initialization

The file:

```text
sql/init.sql
```

creates the `tasks` table:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);
```

It also inserts the initial example tasks when they do not already exist.

The table contains:

| Column  | Type    | Description       |
| ------- | ------- | ----------------- |
| `id`    | SERIAL  | Primary key       |
| `title` | TEXT    | Task title        |
| `done`  | BOOLEAN | Completion status |

## API Endpoints

| Method | Endpoint      | Description         | Success |
| ------ | ------------- | ------------------- | ------: |
| GET    | `/`           | Get API information |     200 |
| GET    | `/health`     | Check API health    |     200 |
| GET    | `/tasks`      | Get all tasks       |     200 |
| GET    | `/tasks/{id}` | Get one task        |     200 |
| POST   | `/tasks`      | Create a task       |     201 |
| PUT    | `/tasks/{id}` | Update a task       |     200 |
| DELETE | `/tasks/{id}` | Delete a task       |     204 |

## Task Structure

Each task contains:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "done": false
}
```

When creating a task, only the title is required:

```json
{
  "title": "Buy milk"
}
```

The database automatically assigns the task ID and defaults `done` to `false`.

## CRUD Examples

### Get all tasks

```powershell
curl.exe -i http://localhost:8000/tasks
```

Example response:

```json
[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "done": false
  },
  {
    "id": 2,
    "title": "Build CRUD API",
    "done": false
  }
]
```

### Get one task

```powershell
curl.exe -i http://localhost:8000/tasks/1
```

### Create a task

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/tasks" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"title":"Test PostgreSQL persistence"}'
```

The server returns:

```text
HTTP/1.1 201 Created
```

### Update a task

```powershell
curl.exe -i -X PUT http://localhost:8000/tasks/1 `
  -H "Content-Type: application/json" `
  -d '{"title":"Learn FastAPI properly","done":true}'
```

### Delete a task

```powershell
curl.exe -i -X DELETE http://localhost:8000/tasks/1
```

The server returns:

```text
HTTP/1.1 204 No Content
```

## Validation and Error Handling

The API validates incoming data and returns appropriate HTTP status codes.

| Situation            | Status |
| -------------------- | -----: |
| Successful GET       |    200 |
| Successful POST      |    201 |
| Successful PUT       |    200 |
| Successful DELETE    |    204 |
| Invalid request body |    400 |
| Task does not exist  |    404 |

For example, an empty title is rejected:

```powershell
curl.exe -i -X POST http://localhost:8000/tasks `
  -H "Content-Type: application/json" `
  -d '{"title":"   "}'
```

The API returns:

```text
HTTP/1.1 400 Bad Request
```

Trying to access a nonexistent task:

```powershell
curl.exe -i http://localhost:8000/tasks/99
```

returns:

```text
HTTP/1.1 404 Not Found
```

## Swagger UI

FastAPI automatically generates interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

Swagger UI can be used to test all CRUD endpoints through the **Try it out** functionality.





## PostgreSQL Repository

The project uses the `TaskRepository` interface to define the storage operations:

```text
app/repositories/base.py
```

The PostgreSQL implementation is:

```text
app/repositories/postgres_task_repository.py
```

The service depends on the repository interface rather than directly depending on PostgreSQL.

This means the application follows:

```text
Routes
  ↓
Service
  ↓
Repository Interface
  ↓
PostgreSQL Repository
```

The **service and routes were not changed to add PostgreSQL queries**. PostgreSQL-specific persistence is contained inside the repository implementation.

## Persistence Proof

Persistence was tested by creating a task and then restarting the application and database containers.

Example test:

```powershell
docker compose up --build
```

Create a task:

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/tasks" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"title":"A3 persistence test"}'
```

Verify that the task exists:

```powershell
curl.exe http://localhost:8000/tasks
```

Stop the stack:

```powershell
docker compose down
```

The Docker volume was intentionally preserved.

The stack was then started again:

```powershell
docker compose up --build
```

The task was requested again:

```powershell
curl.exe http://localhost:8000/tasks
```

The previously created task remained in the database after the container restart.

This proves that PostgreSQL data is persisted through the Docker volume rather than being stored only inside the application container.

> Do not use `docker compose down -v` during this test because the `-v` option removes the database volume and therefore deletes the persisted data.

## Data Persistence

The PostgreSQL data directory is backed by the named Docker volume:

```text
postgres_data
```

The volume exists independently of the PostgreSQL container.

Therefore:

```text
PostgreSQL container
       ↓
postgres_data volume
       ↓
Database data survives container restart
```

## Technologies

* Python
* FastAPI
* Uvicorn
* Pydantic
* PostgreSQL
* Psycopg
* Docker
* Docker Compose
* Git
* GitHub

## A3 Assignment Outcome

This implementation satisfies the main A3 requirements:

* PostgreSQL runs inside Docker.
* PostgreSQL uses a persistent Docker volume.
* The application and database start together with `docker compose up`.
* The database connection string is provided through `.env`.
* `.env` is gitignored.
* `.env.example` is committed.
* The database table is created through `sql/init.sql`.
* A PostgreSQL repository implements the existing repository interface.
* The service and routes remain independent of PostgreSQL.
* CRUD operations use the PostgreSQL database.
* Persistence was verified across application and container restart.

## Author

Ahmed Mohamed Nagib
