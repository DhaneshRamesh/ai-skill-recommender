import io
import pymupdf4llm

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts clean text from a PDF file in-memory using pymupdf4llm.
    Converts to markdown, then strips formatting to raw text.

    Args:
        file_bytes (bytes): PDF file content in bytes

    Returns:
        str: Extracted plain text
    """
    try:
        print("[DEBUG] Starting text extraction from PDF bytes")
        md_text = pymupdf4llm.to_markdown(io.BytesIO(file_bytes))
        print(f"[DEBUG] Extracted markdown preview (first 500 chars):\n{md_text[:500]}")

        # Optional: strip markdown to plain text
        plain_text = md_text.replace("#", "").replace("*", "").strip()
        print(f"[DEBUG] Plain text preview (first 20000 chars):\n{plain_text[:20000]}")

        return plain_text

    except Exception as e:
        print(f"❌ Error extracting text from PDF: {e}")
        return ""
