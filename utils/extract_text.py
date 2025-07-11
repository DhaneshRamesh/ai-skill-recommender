import pdfplumber
from docx import Document

def extract_text_from_pdf(file_obj):
    with pdfplumber.open(file_obj) as pdf:
        return ' '.join([page.extract_text() for page in pdf.pages if page.extract_text()])

def extract_text_from_docx(file_obj):
    doc = Document(file_obj)
    return '\n'.join([para.text for para in doc.paragraphs])
