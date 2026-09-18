from django.urls import path
from .views import SubjectListView,SubjectDetailView,SourceDocumentListView


urlpatterns = [
    path("subjects/", SubjectListView.as_view(), name="subject-list"),
    path("subjects/<int:pk>/" , SubjectDetailView.as_view(), name="subject-detail"),
    path("documents/", SourceDocumentListView.as_view(), name="document-list"),
]