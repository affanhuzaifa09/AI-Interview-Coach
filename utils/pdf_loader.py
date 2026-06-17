# utils/pdf_loader.py
# This utility file handles PDF reading and text extraction.
# It is used by both the Resume Analyzer and RAG Knowledge Base modules.

from pypdf import PdfReader
import streamlit as st


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extracts all text from an uploaded PDF file.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        Full text content of the PDF as a single string
    """

    try:
        # Create a PDF reader object from the uploaded file
        reader = PdfReader(uploaded_file)

        full_text = ""

        # Loop through every page and extract text
        for page_number, page in enumerate(reader.pages):
            page_text = page.extract_text()

            if page_text:
                full_text += f"\n--- Page {page_number + 1} ---\n"
                full_text += page_text

        if not full_text.strip():
            return "Could not extract text from this PDF. It may be scanned or image-based."

        return full_text.strip()

    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def get_pdf_info(uploaded_file) -> dict:
    """
    Returns basic information about the PDF.

    Returns:
        Dictionary with page count and file name
    """

    try:
        reader = PdfReader(uploaded_file)
        return {
            "pages": len(reader.pages),
            "filename": uploaded_file.name
        }
    except Exception:
        return {"pages": 0, "filename": "Unknown"}