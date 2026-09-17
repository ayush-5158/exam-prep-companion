from django.contrib import admin
from .models import Subject, SourceDocument, Chunk

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(SourceDocument)
class SourceDocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subject", "created_at")
    list_filter = ("subject",)
    search_fields = ("title",)
    ordering = ("-created_at",)

@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "chunk_index")
    list_filter = ("document",)
    search_fields = ("content",)
    ordering = ("document", "chunk_index")
