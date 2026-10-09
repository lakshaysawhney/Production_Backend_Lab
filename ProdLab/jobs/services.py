from jobs.models import Job

def create_job(*, name: str, payload: dict) -> Job:
    return Job.objects.create(
        name=name,
        payload=payload,
    )