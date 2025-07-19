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
        # Convert bytes to markdown
        md_text = pymupdf4llm.to_markdown(io.BytesIO(file_bytes))

        # Optional: strip markdown to plain text
        plain_text = md_text.replace("#", "").replace("*", "").strip()

        return plain_text

    except Exception as e:
        print(f"❌ Error extracting text from PDF: {e}")
        return ""
