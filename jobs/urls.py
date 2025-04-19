from django.urls import path
from .views import JobListCreateView, JobDetailView, JobResultView

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/<int:pk>/result/', JobResultView.as_view(), name='job-result'),
]
