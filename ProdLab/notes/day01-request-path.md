# Day 1 — Production Request Path

## Mental Model

A backend request does not simply go:

```text
Client → Django → Database
```

A more realistic production path is:

```text
Client
→ reverse proxy
→ application server
→ Django middleware
→ URL routing
→ DRF view
→ serializer
→ service
→ Django ORM
→ PostgreSQL
→ response back outward
```

For this project, the eventual production path will be:

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

Locally, Django is still using `runserver`.

## Important Boundaries

### Middleware

Used for concerns that apply across many requests rather than one business feature.

Examples:

- request IDs
- logging
- timing
- security-related processing
- session/authentication-related processing

Middleware can run logic before the request reaches the view and again when the response comes back.

### View

The HTTP/controller layer.

Main responsibilities:

- receive the HTTP request
- invoke input validation
- call application/business logic
- create the HTTP response

Views should not grow into large containers for all business logic.

### Serializer

The boundary between external API data and internal application data.

Incoming:

```text
untrusted request data
→ validation
→ validated_data
```

Outgoing:

```text
Django/model object
→ API representation
→ JSON response
```

The database model, API input contract and API output contract do not have to be identical.

### Service Layer

Represents an application/business operation.

Example:

```text
create_job(...)
```

The service currently performs only a simple database create, but this keeps business orchestration out of the HTTP layer and gives it somewhere to grow later.

### ORM / Model

The model defines persistent application data.

The ORM converts Python-level operations such as:

```python
Job.objects.create(...)
```

into database operations against PostgreSQL.

## What I Implemented

- PostgreSQL-backed `Job` model
- UUID primary keys
- job status enum
- Django migrations
- create/list/retrieve Job APIs
- separate create and output serializers
- serializer validation
- service layer for job creation
- request-ID middleware
- automated API/integration tests

## Request Flow for Creating a Job

```text
POST /api/v1/jobs/
        ↓
Request-ID Middleware
        ↓
URL routing
        ↓
JobListCreateAPIView.post()
        ↓
request.data
        ↓
JobCreateSerializer
        ↓
validated_data
        ↓
create_job()
        ↓
Job.objects.create()
        ↓
PostgreSQL INSERT
        ↓
Job model instance
        ↓
JobSerializer
        ↓
DRF Response (201)
        ↓
Request-ID Middleware adds X-Request-ID
        ↓
Client
```

## Things I Observed

### Invalid input

Invalid input is rejected by the serializer before business logic or database creation happens.

```text
bad request
→ validation fails
→ 400
→ no DB mutation
```

A `400` is an expected client error, not an application crash.

### Database outage

When PostgreSQL is unavailable, an otherwise-correct API can still fail.

This reinforced that the backend is dependent on external infrastructure and that production reliability is not only about writing correct application code.

### Middleware

Middleware can:

- inspect incoming requests
- attach context to them
- let the request continue
- inspect/modify outgoing responses
- stop a request before it reaches the view

### Request IDs

Each request can be given an identifier such as:

```text
5e346792-5af5-42ec-b77c-bbdb688ca770
```

This can later be attached to logs so that all events belonging to one request can be correlated.

## Testing Mental Model

Tests convert expectations into executable checks.

```text
Requirement
→ Acceptance Criterion
→ Automated Test
```

Example:

```text
Requirement:
Input validation

Acceptance criterion:
Invalid job request returns 400

Test:
test_rejects_short_job_name()
```

The current API tests cover:

- valid creation → `201`
- invalid creation → `400`
- retrieve existing job → `200`
- retrieve unknown job → `404`
- response contains `X-Request-ID`

These are integration-style API tests because they exercise several real layers together:

```text
URL
→ View
→ Serializer
→ Service
→ ORM
→ Test Database
```

## Intentional Gaps

The current system is deliberately incomplete.

Still to be added:

- authentication
- authorization / RBAC
- tenant isolation
- proper pagination
- transaction handling
- concurrency protection
- caching
- background jobs
- retries / idempotency
- structured logging
- metrics / tracing
- health checks
- load testing
- Gunicorn
- NGINX
- CI/CD
- production deployment

The list endpoint currently limits results to 100 as a temporary safeguard. Proper pagination will be implemented later.
