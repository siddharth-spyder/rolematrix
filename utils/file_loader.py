"""
File loader utility to extract text from PDF and DOCX files.
"""
import pdfplumber
from docx import Document
from typing import Optional


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file using pdfplumber.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""
    return text.strip()


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file using python-docx.
    
    Args:
        file_path: Path to the DOCX file
        
    Returns:
        Extracted text as a string
    """
    text = ""
    try:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error extracting DOCX text: {e}")
        return ""
    return text.strip()


def extract_text_from_file(file_path: str, file_extension: str) -> Optional[str]:
    """
    Extract text from a file based on its extension.
    
    Args:
        file_path: Path to the file
        file_extension: File extension (pdf or docx)
        
    Returns:
        Extracted text as a string or None if unsupported format
    """
    file_extension = file_extension.lower()
    
    if file_extension == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_extension in ["docx", "doc"]:
        return extract_text_from_docx(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return None
