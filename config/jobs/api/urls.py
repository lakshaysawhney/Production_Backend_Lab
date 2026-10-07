from django.urls import path

from jobs.api.views import (
    JobDetailAPIView,
    JobListCreateAPIView,
)


urlpatterns = [
    path(
        "",
        JobListCreateAPIView.as_view(),
        name="job-list-create",
    ),

    path(
        "<uuid:job_id>/",
        JobDetailAPIView.as_view(),
        name="job-detail",
    ),
]