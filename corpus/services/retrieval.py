import os

from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_mistralai import MistralAIEmbeddings


load_dotenv()


def retrieve_chunks(query, top_k=5):
    embeddings = MistralAIEmbeddings(
        model="mistral-embed"
    )

    query_vector = embeddings.embed_query(query)

    pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY")
    )

    index = pc.Index("exam-prep")

    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace="core",
    )

    retrieved_chunks = []

    for match in results["matches"]:
        retrieved_chunks.append({
            "text": match["metadata"]["text"],
            "score": match["score"],
            "document_id": match["metadata"]["document_id"],
            "chunk_index": match["metadata"]["chunk_index"],
        })

    return retrieved_chunks

def build_context(retrieved_chunks):
    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(chunk["text"])

    return "\n\n".join(context_parts)