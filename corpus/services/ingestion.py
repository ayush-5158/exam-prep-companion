import os

import fitz
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings

from corpus.models import SourceDocument, Chunk

load_dotenv()


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    full_text = ""

    for page in doc:
        full_text += page.get_text() + "\n"

    doc.close()

    return full_text


def extract_document_text(document_id):
    document = SourceDocument.objects.get(id=document_id)

    pdf_path = document.file.path

    return extract_text_from_pdf(pdf_path)


def create_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    chunks = splitter.split_text(text)

    return chunks


def save_chunks(document_id, chunks):
    document = SourceDocument.objects.get(id=document_id)

    # Existing chunks delete karo
    Chunk.objects.filter(document=document).delete()

    chunk_objects = []

    for i, content in enumerate(chunks):
        chunk_objects.append(
            Chunk(
                document=document,
                content=content,
                chunk_index=i,
            )
        )

    Chunk.objects.bulk_create(chunk_objects)

    return len(chunk_objects)

def create_embeddings(chunks):
    embeddings = MistralAIEmbeddings(
        model="mistral-embed"
    )

    vectors = embeddings.embed_documents(chunks)

    return vectors


def store_vectors(document_id, chunks, vectors):
    pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY")
    )

    index = pc.Index("exam-prep")

    records = []

    for i, vector in enumerate(vectors):
        records.append({
            "id": f"document-{document_id}-chunk-{i}",
            "values": vector,
            "metadata": {
                "text": chunks[i],
                "document_id": document_id,
                "chunk_index": i,
                "source": "core",
            },
        })

    index.upsert(
        vectors=records,
        namespace="core",
    )

    return len(records)


def ingest_document(document_id):
    # 1. PDF se text extract
    text = extract_document_text(document_id)

    # 2. Text ko chunks me divide
    chunks = create_chunks(text)

    # 3. Chunks PostgreSQL me save
    chunk_count = save_chunks(
        document_id,
        chunks,
    )

    # 4. Chunks ke embeddings create
    vectors = create_embeddings(chunks)

    # 5. Vectors Pinecone me store
    vector_count = store_vectors(
        document_id,
        chunks,
        vectors,
    )

    return {
        "document_id": document_id,
        "chunks": chunk_count,
        "vectors": vector_count,
    }