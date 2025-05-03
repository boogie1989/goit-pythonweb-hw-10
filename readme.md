# Contacts API

A REST API for managing contacts, built with FastAPI and SQLAlchemy.

## Project Structure

The project follows a modular architecture:

```
app/
├── api/                  # API endpoints
│   ├── endpoints/        # Route handlers
│   │   └── contacts.py   # Contacts endpoints
│   └── router.py         # Main API router
├── core/                 # Core configuration
│   ├── config.py         # App settings
│   └── database.py       # Database connection
├── crud/                 # Database operations
│   └── contact.py        # Contact CRUD operations
├── models/               # SQLAlchemy models
│   └── contact.py        # Contact model
└── schemas/              # Pydantic schemas
    └── contact.py        # Contact validation schemas
main.py                   # Application entry point
alembic/                  # Database migrations
```

## Requirements

- Python 3.11+
- PostgreSQL
- Docker

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:boogie1989/goit-pythonweb-hw-08.git
   cd goit-pythonweb-hw-08
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run PostgreSQL in Docker:

   ```bash
   docker-compose up --build
   ```

4. Apply migrations:
   ```bash
   alembic upgrade head
   ```

## Running the API

Start the server:

```bash
uvicorn main:app --reload
```

API is available at: `http://127.0.0.1:8000`

Documentation: `http://127.0.0.1:8000/docs`

## Features

- **POST** `/api/v1/contacts/` — Create a contact
- **GET** `/api/v1/contacts/` — List all contacts
- **GET** `/api/v1/contacts/{id}` — Get a contact by ID
- **PUT** `/api/v1/contacts/{id}` — Update a contact
- **DELETE** `/api/v1/contacts/{id}` — Delete a contact
- **GET** `/api/v1/contacts/search/?query=...` — Search by first name, last name, or email
- **GET** `/api/v1/contacts/birthdays/` — Get contacts with birthdays in the next 7 days
