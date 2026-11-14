from fastapi import APIRouter, UploadFile, HTTPException
from src.services.ai import ai_analyze_pdf, ai_ds_analyze_pdf
from src.constants import AI_FILE_ANALYSIS_ANALYSIS_PROMPT
import asyncio

router = APIRouter()

@router.post("/paid_multiple_files_upload", description="Бесплатный анализ файлов формата PDF")
async def upload_files(uploaded_files: list[UploadFile]):
    files = []

    for uploaded_file in uploaded_files:
        try:
            file_bytes = await uploaded_file.read()

            if not file_bytes.startswith(b"%PDF-"):
                raise HTTPException(
                    status_code=400,
                    detail=f"Файл {uploaded_file.filename} должен быть PDF"
                )
            
            files.append((uploaded_file.filename, file_bytes))

        finally:
            await uploaded_file.close()

    result = await ai_analyze_pdf(prompt=AI_FILE_ANALYSIS_ANALYSIS_PROMPT, files=files)
    
    if result is None:
        raise HTTPException(
            status_code=502,
            detail="[API upload_files]Не удалось получить ответ от ИИ"
        )
    
    return result


@router.post("/free_multiple_files_upload", description="Платный анализ файлов формата PDF")
async def upload_files(uploaded_files: list[UploadFile]):
    files = []

    for uploaded_file in uploaded_files:
        try:
            file_bytes = await uploaded_file.read()

            if not file_bytes.startswith(b"%PDF-"):
                raise HTTPException(
                    status_code=400,
                    detail=f"Файл {uploaded_file.filename} должен быть PDF"
                )
            
            files.append((uploaded_file.filename, file_bytes))

        finally:
            await uploaded_file.close()

    result = await ai_ds_analyze_pdf(prompt=AI_FILE_ANALYSIS_ANALYSIS_PROMPT, files=files)
    
    if result is None:
        raise HTTPException(
            status_code=502,
            detail="[API upload_files]Не удалось получить ответ от ИИ"
        )
    
    return result
    
    
