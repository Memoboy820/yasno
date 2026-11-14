from fastapi import APIRouter, UploadFile, HTTPException
from src.services.ai import ai_free_analyze_pdf, ai_paid_analyze_pdf
from src.constants import AI_FILE_ANALYSIS_ANALYSIS_PROMPT
import asyncio

router = APIRouter()

@router.post("/free_multiple_files_upload", description="Бесплатный анализ файлов из доступных форматов")
async def upload_files(uploaded_files: list[UploadFile]):
    files = []

    for uploaded_file in uploaded_files:
        try:
            file_bytes = await uploaded_file.read()
            
            files.append((uploaded_file.filename, file_bytes))

        finally:
            await uploaded_file.close()

    result = await ai_free_analyze_pdf(prompt=AI_FILE_ANALYSIS_ANALYSIS_PROMPT, files=files)
    
    if result is None:
        raise HTTPException(
            status_code=502,
            detail="[API upload_files]Не удалось получить ответ от ИИ"
        )
    
    return result





@router.post("/paid_multiple_files_upload", description="Платный анализ файлов из доступных форматов")
async def upload_files(uploaded_files: list[UploadFile]):
    files = []
    print("[API] Пришёл платный запрос", flush=True)
    print("[READ] Начинаем извлечение текста", flush=True)

    for uploaded_file in uploaded_files:
        try:
            file_bytes = await uploaded_file.read()
            
            files.append((uploaded_file.filename, file_bytes))

        finally:
            await uploaded_file.close()

    print("[AI] Текст готов, отправляем запрос провайдеру", flush=True)
    result = await ai_paid_analyze_pdf(prompt=AI_FILE_ANALYSIS_ANALYSIS_PROMPT, files=files)
    
    if result is None:
        raise HTTPException(
            status_code=502,
            detail="[API upload_files]Не удалось получить ответ от ИИ"
        )
    
    return result
    
    
