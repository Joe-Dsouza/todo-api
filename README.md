# Task API

A simple in-memory CRUD API for managing a to-do list, built with FastAPI.

## How to run

\`\`\`bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install fastapi uvicorn
uvicorn main:app --reload --port 8000
\`\`\`

Then visit `http://localhost:8000` or `http://localhost:8000/docs` for interactive Swagger UI.

## Endpoints

| Method | Path            | Description                     |
|--------|-----------------|----------------------------------|
| GET    | /               | API info                         |
| GET    | /health         | Health check                     |
| GET    | /tasks          | List all tasks                   |
| GET    | /tasks/{id}     | Get one task by id               |
| POST   | /tasks          | Create a new task                |
| PUT    | /tasks/{id}     | Update a task's title/done status|
| DELETE | /tasks/{id}     | Delete a task                    |

## Example request

\`\`\`
curl.exe -i http://localhost:8000/tasks

HTTP/1.1 200 OK
date: Thu, 10 Sep 2026 05:52:32 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":1,"title":"Buy milk","done":false}
\`\`\`

## Swagger UI

![Swagger UI](swagger-screenshot.png)

## Note on data persistence

This API stores tasks in memory only — all data is lost when the server restarts. This is intentional for this stage of the project; a real database is introduced in the following assignment.