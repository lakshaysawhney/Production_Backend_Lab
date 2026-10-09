import uuid

from django.db import models


class Job(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"

    id = models.UUIDField( # Universal Unique Indentifier
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(max_length=120)

    payload = models.JSONField(
        default=dict,
        blank=True,
    )

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True) # created when row is created in DB
    updated_at = models.DateTimeField(auto_now=True) # updated every time instance is saved/updated in DB

    def __str__(self):
        return f"{self.name} ({self.status})"