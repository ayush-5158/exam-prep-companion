import environ

from langchain_google_genai import ChatGoogleGenerativeAI

from corpus.services.retrieval import retrieve_chunks, build_context


env = environ.Env()
env.read_env()


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0,
        google_api_key=env("GEMINI_API_KEY"),
    )


def answer_question(question):
    # 1. Retrieve relevant chunks from Pinecone
    retrieved_chunks = retrieve_chunks(
        question,
        top_k=5,
    )

    # 2. Build context from retrieved chunks
    context = build_context(retrieved_chunks)

    # 3. Create prompt
    prompt = f"""
You are a UPSC preparation assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided material."

Context:
{context}

Question:
{question}
"""

    # 4. Send context + question to Gemini
    llm = get_llm()

    response = llm.invoke(prompt)

    # 5. Get clean text response
    answer = response.text()

    # 6. Prepare clean source information
    sources = []

    for chunk in retrieved_chunks:
        sources.append({
            "document_id": chunk["document_id"],
            "chunk_index": chunk["chunk_index"],
            "score": chunk["score"],
        })

    # 7. Return API-friendly response
    return {
        "answer": answer,
        "sources": sources,
    }