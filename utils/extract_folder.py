import os
import pymupdf4llm
from pathlib import Path

def process_pdfs_in_folder(pdf_folder_path):
    try:
        pdf_folder = Path(pdf_folder_path)
        
        print(f"[DEBUG] Checking folder at: {pdf_folder_path}")
        if not pdf_folder.exists():
            print(f"❌ Error: Folder not found at '{pdf_folder_path}'")
            return
        
        pdf_files = list(pdf_folder.glob("*.pdf"))
        print(f"[DEBUG] Number of PDF files found: {len(pdf_files)}")
        
        if not pdf_files:
            print(f"⚠️ No PDF files found in '{pdf_folder}'")
            return
        
        for pdf_file in pdf_files:
            print(f"\n[DEBUG] Processing file: {pdf_file.name}")
            print("-" * 50)

            try:
                md_text = pymupdf4llm.to_markdown(str(pdf_file))
                print(f"[DEBUG] Extracted markdown preview (first 500 chars):\n{md_text[:500]}")

            except Exception as e:
                print(f"❌ Error processing {pdf_file.name}: {str(e)}")

            print("-" * 50)
            print("\n")

    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    pdf_folder_path = r"./Resumes"
    process_pdfs_in_folder(pdf_folder_path)
