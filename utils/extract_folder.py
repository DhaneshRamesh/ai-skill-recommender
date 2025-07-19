import os
import pymupdf4llm
from pathlib import Path

def process_pdfs_in_folder(pdf_folder_path):
    """
    Processes all PDF files in the specified folder,
    extracts Markdown content, and prints it with separators.

    Args:
        pdf_folder_path (str): Full path to the folder containing PDFs
    """
    try:
        pdf_folder = Path(pdf_folder_path)
        
        if not pdf_folder.exists():
            print(f"❌ Error: Folder not found at '{pdf_folder_path}'")
            return
        
        pdf_files = list(pdf_folder.glob("*.pdf"))
        
        if not pdf_files:
            print(f"⚠️ No PDF files found in '{pdf_folder}'")
            return
        
        for pdf_file in pdf_files:
            print(f"\n📄 Processing: {pdf_file.name}")
            print("-" * 50)

            try:
                # Extract Markdown text from the PDF
                md_text = pymupdf4llm.to_markdown(str(pdf_file))
                print(md_text)

            except Exception as e:
                print(f"❌ Error processing {pdf_file.name}: {str(e)}")

            print("-" * 50)
            print("\n")

    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

# --- Main entry ---
if __name__ == "__main__":
    # Modify this path or accept from input()
    pdf_folder_path = r"./Resumes"
    process_pdfs_in_folder(pdf_folder_path)
