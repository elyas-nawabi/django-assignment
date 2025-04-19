from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from .models import Job, JobResult
from .serializers import JobSerializer, JobResultSerializer
from .tasks import process_job
from drf_spectacular.utils import extend_schema

class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

    @extend_schema(
        request=JobSerializer,
        responses=JobSerializer,
        description="Create a new job with a scheduled time. Automatically schedules the job with Celery."
    )
    def perform_create(self, serializer):
        scheduled_time = serializer.validated_data['scheduled_time']
        if scheduled_time < timezone.now():
            raise ValidationError("Scheduled time cannot be in the past.")

        job = serializer.save(user=self.request.user)

        # Schedule Celery task
        process_job.apply_async((job.id,), eta=scheduled_time)

class JobDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

class JobResultView(generics.RetrieveAPIView):
    serializer_class = JobResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobResult.objects.filter(job__user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.job.status != 'completed':
            raise ValidationError("Result is only available for completed jobs.")
        return obj