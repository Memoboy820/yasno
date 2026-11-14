from src.constants import models, ai_client, ds_client, AI_FILE_ANALYSIS_ANALYSIS_PROMPT as AI_FILE_ANALYSIS_ANALYSIS_STARTING_PROMPT
from google.genai import types
from .funcs import bytes_to_text, make_document_content, get_mime_type
import json
from asyncio import to_thread


# ------------------------------------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ

async def get_openai_models() -> list[str]:
    try:
        available_models = await ds_client.models.list()
        ds_models = [model.id for model in available_models.data]   
        return ds_models
    except Exception as e:
        raise Exception(f"Не удалось получить доступные модели openai: {e}")



async def ai_files_create(filename: str, file_bytes: bytes) -> dict:
    uploaded = await ds_client.files.create(
        file=(filename, file_bytes),
        purpose="user_data",
    )

    return {"type": "input_file", "file_id": uploaded.id,}   



async def get_gemini_response(ai: str, prompt: str, contents: list[str | types.Part]):
    for model in models:
        try:
            response = await ai_client.aio.models.generate_content(
                model=model,
                config=types.GenerateContentConfig(system_instruction=prompt, response_mime_type="application/json"),
                contents=contents
            )
            if response.text:
                ai_text_list = json.loads(response.text)

                if not isinstance(ai_text_list, (dict, list)):
                    raise ValueError(f"[{ai}] Ожидался JSON объект или список")
            
                return ai_text_list
        except Exception as e:
            print(f"[{ai}] {model} не дала пригодный ответ: {e}")
    return None



async def get_openai_response(ai: str, contents: list[dict]):
    try:
        response = await ds_client.responses.create(
            model="gemma-4-26b-a4b-it",
            input=[{"role": "user", "content": contents}],
            text={"format": {"type": "json_object"}}
            )       
        
        if response.output_text:
            ai_text_list = json.loads(response.output_text)

            if not isinstance(ai_text_list, (dict, list)):
                raise ValueError(f"[{ai}] Ожидался JSON объект или список")
        
            return ai_text_list


    except Exception as e:
        print(f"[{ai}] не дала пригодный ответ: {e}")
    return None



# ------------------------------------------- ГЛАВНЫЕ ФУНКЦИИ


async def ai_free_analyze_pdf(prompt: str, files: list[tuple[str, bytes]]) -> dict | list | None:
    if not files:
        raise ValueError("Не переданы файлы")
    
    contents= [AI_FILE_ANALYSIS_ANALYSIS_STARTING_PROMPT]

    for filename, filebytes in files:
        try:
            part = types.Part.from_bytes(
                data=filebytes,
                mime_type=get_mime_type(filename=filename))

            contents.extend([
            f"Следующий документ: {filename}",
            part
        ])
            
        except Exception as e:
            print(f"[GEMINI] Не удалось обработать файл: {e}")


    if len(contents) > 1: # наличие файлов вообще
        ai_text_list = await get_gemini_response(ai="GEMINI", prompt=prompt, contents=contents)
        return ai_text_list
    return None





async def ai_paid_analyze_pdf(prompt: str, files: list[tuple[str, bytes]]) -> dict | list | None:
    if not files:
        raise ValueError("Не переданы файлы")

    contents = [{
        "type": "input_text",
        "text": AI_FILE_ANALYSIS_ANALYSIS_STARTING_PROMPT + f"\n{prompt}" + "\nВерни результат в виде JSON",
    }]

    try:
        for filename, file_bytes in files:
            text = await to_thread(bytes_to_text, filename=filename, file=file_bytes)
            contents.append(make_document_content(filename, text))
    except Exception as e:
        raise ValueError(f"[OPENAI] Не удалось прочитать файл {filename}: {e}") from e
    
    
    ai_text_list = await get_openai_response(ai="OPENAI", contents=contents)

    if ai_text_list is not None:
        return ai_text_list
    return None
