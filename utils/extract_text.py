import io
import pymupdf4llm
import fitz  # PyMuPDF
from typing import Optional
import logging
import tempfile
import os

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_bytes: bytes) -> Optional[str]:
    """
    Extracts clean text from PDF bytes using best available method.
    Handles both pymupdf4llm and PyMuPDF with proper file handling.
    
    Args:
        file_bytes: PDF content as bytes
        
    Returns:
        Extracted text or None on failure
    """
    temp_path = None
    try:
        # First try pymupdf4llm by writing to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name

        try:
            # pymupdf4llm works better with file paths
            md_text = pymupdf4llm.to_markdown(temp_path)
            plain_text = md_text.replace("#", "").replace("*", "").strip()
            if len(plain_text) > 100:  # Reasonable minimum
                return plain_text
        except Exception as e:
            logger.warning(f"pymupdf4llm failed: {e}")
            # Fallback to PyMuPDF
            try:
                doc = fitz.open(temp_path)
                text = "\n".join(page.get_text() for page in doc)
                return text.strip() if text else None
            except Exception as e:
                logger.error(f"PyMuPDF failed: {e}")
                return None
                
    except Exception as e:
        logger.exception("PDF extraction failed")
        return None
    finally:
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception as e:
                logger.warning(f"Could not delete temp file: {e}")