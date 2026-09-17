from django.db import models

class Subject(models.Model):

    name = models.CharField(max_length=100,unique=True)

class SourceDocument(models.Model):

    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name="documents",)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="corpus/")
    created_at = models.DateTimeField(auto_now_add=True)

class Chunk(models.Model):

    document = models.ForeignKey(SourceDocument,on_delete=models.CASCADE,related_name="chunks",)
    content = models.TextField()
    chunk_index = models.PositiveIntegerField()