from rest_framework import serializers
from .models import Job, JobResult

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'name', 'description', 'scheduled_time', 'status']

class JobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResult
        fields = ['job', 'output', 'error_message', 'completed_at']
