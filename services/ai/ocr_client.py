# services/ai/ocr_client.py

import os
import io
from google.cloud import documentai
from PyPDF2 import PdfReader

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION")
PROCESSOR_ID = os.getenv("DOC_OCR_PROCESSOR_ID")

client = documentai.DocumentProcessorServiceClient()


def has_digital_text(content: bytes, mime_type: str) -> bool:
    """
    Check if a PDF has extractable digital text.
    Returns True if text can be extracted directly, False if OCR is needed.
    """
    if mime_type != "application/pdf":
        return False
    
    try:
        pdf = PdfReader(io.BytesIO(content))
        # Check first few pages for text
        for page_num in range(min(3, len(pdf.pages))):
            text = pdf.pages[page_num].extract_text()
            if text and len(text.strip()) > 50:  # Has meaningful text
                return True
        return False
    except Exception:
        return False


def extract_text_from_pdf(content: bytes) -> str:
    """Extract text directly from a PDF with digital text."""
    try:
        pdf = PdfReader(io.BytesIO(content))
        text_parts = []
        for page in pdf.pages:
            text_parts.append(page.extract_text())
        return "\n\n".join(text_parts)
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""


def extract_text_with_ocr(content: bytes, mime_type: str) -> str:
    """Use Document AI OCR to extract text from scanned documents or images."""
    name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    request = {
        "name": name,
        "raw_document": {"content": content, "mime_type": mime_type}
    }

    result = client.process_document(request=request)
    return result.document.text or ""


def extract_text(content: bytes, mime_type: str) -> str:
    """
    Smart text extraction:
    - For PDFs with digital text: extract directly (fast, free)
    - For scanned PDFs or images: use Document AI OCR
    """
    # Check if PDF has digital text
    if mime_type == "application/pdf" and has_digital_text(content, mime_type):
        print("📄 Extracting text from digital PDF...")
        return extract_text_from_pdf(content)
    
    # Check if OCR is properly configured
    if not PROJECT_ID or not PROCESSOR_ID:
        print("⚠️ OCR not configured - cannot process scanned documents")
        return "ERROR: This document appears to be scanned or is an image. OCR is not configured. Please upload a PDF with digital text, or configure Document AI OCR processor in Google Cloud Console."
    
    # Use OCR for scanned documents or images
    print("🔍 Running OCR on scanned document/image...")
    try:
        return extract_text_with_ocr(content, mime_type)
    except Exception as e:
        print(f"❌ OCR failed: {e}")
        return f"ERROR: OCR processing failed. This document may be scanned or an image. Please upload a PDF with digital text. (Technical error: {str(e)[:100]})"
