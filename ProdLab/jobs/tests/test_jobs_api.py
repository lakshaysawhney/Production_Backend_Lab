import pytest
from rest_framework.test import APIClient

from jobs.models import Job

# creating api_client pytest fixture (fixture = reusable test setup)
@pytest.fixture
def api_client():
    return APIClient()

# Test 1 - Create Job
@pytest.mark.django_db # explicitly allows test to use Django's TEST db 
# (done to prevent arbitrary database access since DB tests are more expensive & have side effects than pure code tests)
def test_create_job(api_client):
    response = api_client.post(
        "/api/v1/jobs/",
        {
            "name": "generate-report",
            "payload": {
                "month": "2026-09",
            },
        },
        format="json",
    )

    assert response.status_code == 201

    assert response.data["name"] == "generate-report"
    assert response.data["status"] == "pending"

    assert Job.objects.count() == 1

# Test 2 - Invalid Input must not create anything
@pytest.mark.django_db
def test_rejects_short_job_name(api_client):
    response = api_client.post(
        "/api/v1/jobs/",
        {
            "name": "x",
            "payload": {},
        },
        format="json",
    )

    assert response.status_code == 400
    assert Job.objects.count() == 0

# Test 3 - retrieve existing job
@pytest.mark.django_db
def test_get_job(api_client):
    # ARRANGE
    job = Job.objects.create(
        name="generate-report",
        payload={},
    )
    # ACT
    response = api_client.get(
        f"/api/v1/jobs/{job.id}/"
    )
    # ASSERT
    assert response.status_code == 200
    assert response.data["id"] == str(job.id)

# Test 4 - unknown Job -> 404
@pytest.mark.django_db
def test_unknown_job_returns_404(api_client):
    response = api_client.get(
        "/api/v1/jobs/"
        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa/"
    )

    assert response.status_code == 404

# Test 5 - Middleware (Request ID)
@pytest.mark.django_db
def test_response_contains_request_id(api_client):
    response = api_client.get(
        "/api/v1/jobs/",
        HTTP_X_REQUEST_ID="test-request-123",
    )

    assert (
        response.headers["X-Request-ID"]
        == "test-request-123"
    )