# User Balance Management API

A production-quality REST API built with FastAPI following Domain-Driven Design (DDD) principles.

## Features

- Create users with unique emails and initial balance
- List all users
- Transfer money between users with validation
- Clean DDD architecture
- Comprehensive error handling
- Type hints throughout
- Unit tests

## Architecture

```
app/
├── domain/          # Business logic and entities
├── application/     # Use cases and business workflows
├── infrastructure/  # Data persistence (in-memory)
└── interfaces/      # API routes and schemas
```

## Installation

```bash
# Install dependencies
uv sync
```

## Running the Application

```bash
# Development server
uv run fastapi dev app/main.py

# Production server
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Create User
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "balance": 100.0}'
```

### Get Users
```bash
curl "http://localhost:8000/users"
```

### Transfer Money
```bash
curl -X POST "http://localhost:8000/transfer" \
  -H "Content-Type: application/json" \
  -d '{"from_user_id": 1, "to_user_id": 2, "amount": 25.0}'
```

## Testing

```bash
uv run pytest test_api.py -v
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc