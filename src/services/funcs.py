from src.constants import ds_client, mime_types
from io import BytesIO
from pypdf import PdfReader
from pathlib import Path
from markitdown import MarkItDown, UnsupportedFormatException


def bytes_to_text(filename: str, file: bytes)-> str:
    try:
        reader = MarkItDown().convert_stream(
            BytesIO(file), file_extension=Path(filename).suffix.lower()
            )
        
        text = reader.text_content
        return text
    except UnsupportedFormatException as e:
        raise ValueError(f"[MARKITDOWN] Неподдерживаемый тип файла: {e}") from e



def make_document_content(filename: str, text: str) -> dict:
    return {
        "type": "input_text",
        "text": f"Документ: {filename}\n\n{text}",
    }



def get_mime_type(filename: str) -> str: 
    extension = Path(filename).suffix.lower()
    mime_type = mime_types.get(extension)

    if mime_type is None:
        raise ValueError(f"Неподдерживаемый формат файла: {filename}")
    
    return mime_type

