from celery import shared_task
from django.utils import timezone
from .models import Job, JobResult


@shared_task
def process_job(job_id):
    from .models import Job, JobResult

    try:
        job = Job.objects.get(id=job_id)
        job.status = "in_progress"
        job.save()

        # Simulate processing
        result_output = f"Processed job: {job.name} at {timezone.now()}"

        # Update or create result
        JobResult.objects.update_or_create(
            job=job,
            defaults={
                "output": result_output,
                "completed_at": timezone.now(),
                "error_message": None,
            },
        )

        job.status = "completed"
        job.save()

    except Exception as e:
        job.status = "failed"
        job.save()

        # Save or update result with error
        JobResult.objects.update_or_create(
            job=job,
            defaults={
                "error_message": str(e),
                "completed_at": timezone.now(),
                "output": None,
            },
        )


@shared_task
def check_and_run_scheduled_jobs():
    from .models import Job

    now = timezone.now()
    pending_jobs = Job.objects.filter(status="pending", scheduled_time__lte=now)

    for job in pending_jobs:
        # Call the actual processing task
        process_job.delay(job.id)
