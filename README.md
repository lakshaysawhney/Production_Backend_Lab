# Production Backend Lab

Going from “I can build a backend” to “I can ship code in production”.

This repo is my hands-on backend engineering lab for understanding what it takes to move beyond working APIs and build systems that are reliable, secure, observable, performant, testable and safe to operate.

The application itself is intentionally simple so that the focus stays on production engineering rather than product complexity.

## Current Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- pytest
- Docker

More production components will be added progressively as the project evolves.

## Current Architecture

Target production request path:

```text
Client
→ NGINX
→ Gunicorn
→ WSGI
→ Django Middleware
→ DRF
→ Service Layer
→ Django ORM
→ PostgreSQL
```

Currently, Django is still being run locally using its development server.

NGINX, Gunicorn and the production deployment setup will be added later.

## Current Features

- PostgreSQL-backed Job model
- Job create/list/retrieve APIs
- Explicit input validation using DRF serializers
- Separate input and output serializers
- Service layer for job creation
- Request-ID middleware
- Automated API/integration tests
- Environment-based configuration

## Project Structure

```text
Production_Backend_Lab/
├── README.md
├── notes/
├── docker-compose.yml
├── requirements-dev.txt
│
└── ProdLab/
    ├── manage.py
    ├── pytest.ini
    ├── config/
    ├── core/
    └── jobs/
```

## Run Locally

Start PostgreSQL from the repository root:

```bash
docker compose up -d db
```

Move into the Django project:

```bash
cd ProdLab
```

Apply migrations:

```bash
python manage.py migrate
```

Start Django:

```bash
python manage.py runserver
```

Run tests:

```bash
pytest -v
```

## Learning Notes

Short notes and experiments from the production-engineering work are kept in [`notes/`](notes/).
