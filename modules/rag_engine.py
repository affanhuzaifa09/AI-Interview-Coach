# modules/rag_engine.py
# This is the core RAG pipeline.
# It handles: loading PDFs, chunking, embedding, storing in FAISS, and retrieval.

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from utils.embeddings import get_embedding_model

load_dotenv()

# --------------------------------------------------------
# STEP 1: LOAD AND PROCESS PDF
# --------------------------------------------------------

def load_and_chunk_pdf(pdf_path: str) -> list:
    """
    Loads a PDF and splits it into chunks.

    Args:
        pdf_path: Path to the PDF file on disk

    Returns:
        List of document chunks
    """

    # Load PDF using LangChain's PyPDFLoader
    # This loads each page as a separate document
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split documents into smaller chunks
    # chunk_size: maximum characters per chunk
    # chunk_overlap: how many characters overlap between chunks
    # (overlap helps preserve context at chunk boundaries)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


# --------------------------------------------------------
# STEP 2: CREATE VECTOR STORE
# --------------------------------------------------------

def create_vectorstore(chunks: list) -> FAISS:
    """
    Creates a FAISS vector store from document chunks.

    Args:
        chunks: List of document chunks from load_and_chunk_pdf

    Returns:
        FAISS vector store with all chunks embedded
    """

    # Get our embedding model
    embeddings = get_embedding_model()

    # Create FAISS vector store
    # This converts every chunk to an embedding and stores it
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vectorstore


def save_vectorstore(vectorstore: FAISS, path: str = "vectorstore/index"):
    """Saves the FAISS index to disk for reuse."""
    vectorstore.save_local(path)


def load_vectorstore(path: str = "vectorstore/index") -> FAISS:
    """Loads a previously saved FAISS index from disk."""
    embeddings = get_embedding_model()
    vectorstore = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore


# --------------------------------------------------------
# STEP 3: RETRIEVE RELEVANT CHUNKS
# --------------------------------------------------------

def retrieve_context(vectorstore: FAISS, query: str, k: int = 3) -> str:
    """
    Finds the most relevant chunks for a given query.

    Args:
        vectorstore: The FAISS vector store
        query: The user's question
        k: Number of chunks to retrieve (default 3)

    Returns:
        Combined text of the top k most relevant chunks
    """

    # similarity_search finds the k most similar chunks to the query
    relevant_docs = vectorstore.similarity_search(query, k=k)

    # Combine all retrieved chunks into one context string
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    return context


# --------------------------------------------------------
# STEP 4: GENERATE ANSWER USING LLM + CONTEXT
# --------------------------------------------------------

# RAG prompt - instructs LLM to answer based on provided context
rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful study assistant and technical interviewer.

Use the following context from the study material to answer the question.
If the answer is not in the context, say "I couldn't find this in the uploaded material."

Context from study material:
--------------------------
{context}
--------------------------

Question: {question}

Provide a clear, detailed answer based on the context above.
Also generate 2 relevant interview questions based on this topic.

Answer:
"""
)


def answer_question(vectorstore: FAISS, question: str) -> dict:
    """
    Full RAG pipeline: retrieve context + generate answer.

    Args:
        vectorstore: The FAISS vector store
        question: User's question

    Returns:
        Dictionary with context and answer
    """

    # Step 1: Retrieve relevant context
    context = retrieve_context(vectorstore, question)

    # Step 2: Initialize LLM
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Step 3: Build and run chain
    chain = rag_prompt | llm | StrOutputParser()

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return {
        "answer": response,
        "context": context
    }


# --------------------------------------------------------
# HELPER: PROCESS UPLOADED PDF (saves to disk first)
# --------------------------------------------------------

def process_uploaded_pdf(uploaded_file) -> FAISS:
    """
    Takes a Streamlit uploaded file, saves it temporarily,
    processes it and returns a FAISS vector store.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        FAISS vector store ready for querying
    """

    # Save uploaded file temporarily to disk
    # PyPDFLoader needs a file path, not a file object
    temp_path = f"data/notes/{uploaded_file.name}"

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load and chunk the PDF
    chunks = load_and_chunk_pdf(temp_path)

    # Create vector store
    vectorstore = create_vectorstore(chunks)

    return vectorstore, len(chunks)