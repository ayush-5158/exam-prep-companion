from rest_framework import serializers
from .models import Subject,SourceDocument

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]

class SourceDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceDocument
        fields = ["id", "subject", "title", "file", "created_at"]