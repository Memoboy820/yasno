from src.constants import ds_client
from io import BytesIO
from pypdf import PdfReader

def pdf_to_text(file: bytes)-> str:
    reader = PdfReader(BytesIO(file))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text

def make_document_content(filename: str, text: str) -> dict:
    return {
        "type": "input_text",
        "text": f"Документ: {filename}\n\n{text}",
    }