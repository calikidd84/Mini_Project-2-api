# Mini_Project-2-api

Mini Portfolio Project 2 App: a FastAPI backend for a video games application API.

## Start the server

Run the API and PostgreSQL database with Docker Compose:

```bash
docker compose up --build
```

The backend starts on `http://localhost:8000`.

The Compose command builds the backend image, starts the PostgreSQL database, seeds the database, and launches the FastAPI server with Uvicorn.

## API documentation

After the server is running, open either documentation endpoint in your browser:

- `http://localhost:8000/docs` - Interactive Swagger UI documentation. Use this to browse endpoints, view request and response schemas, and test API calls directly from the browser.
- `http://localhost:8000/redoc` - ReDoc documentation. Use this for a clean, reference-style view of the API endpoints and schemas.
