from django.core.management.base import BaseCommand

from corpus.services.ingestion import ingest_document


class Command(BaseCommand):
    help = "Ingest a source document into the RAG pipeline"

    def add_arguments(self, parser):
        parser.add_argument(
            "document_id",
            type=int,
        )

    def handle(self, *args, **options):
        document_id = options["document_id"]

        result = ingest_document(document_id)

        self.stdout.write(
            self.style.SUCCESS(
                f"Document {document_id} ingested successfully. "
                f"Chunks: {result['chunks']}, "
                f"Vectors: {result['vectors']}"
            )
        )