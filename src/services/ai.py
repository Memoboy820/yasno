from src.constants import models, ai_client, ds_client, AI_FILE_ANALYSIS_ANALYSIS_PROMPT, AI_FILE_ANALYSIS_ANALYSIS_STARTING_PROMPT
from google.genai import types
from .funcs import pdf_to_text
import json

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



async def ai_analyze_pdf(prompt: str, files: list[tuple[str, bytes]]) -> dict | list | None:
    if not files:
        raise ValueError("Не переданы файлы")
    
    contents= [AI_FILE_ANALYSIS_ANALYSIS_STARTING_PROMPT]

    for filename, filebytes in files:
        contents.append(f"Следующий документ: {filename}")

        contents.append(
            types.Part.from_bytes(
                data=filebytes,
                mime_type="application/pdf"
            )
        )
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
                    raise ValueError("[ai_analyze_pdf] Ожидался JSON объект или список")
            
                return ai_text_list
        except Exception as e:
            print(f"[ai_analyze_pdf] {model} не дала пригодный ответ: {e}")
    return None





async def ai_ds_analyze_pdf(prompt: str, files: list[tuple[str, bytes]]) -> dict | list | None:
    if not files:
        raise ValueError("Не переданы файлы")

    contents = [{
        "type": "input_text",
        "text": AI_FILE_ANALYSIS_ANALYSIS_STARTING_PROMPT + f"\n{prompt}" + "\nВерни результат в виде JSON",
    }]

    try:
        for filename, file_bytes in files:
            contents.append(filename, pdf_to_text(file=file_bytes))
    except Exception as e:
        raise ValueError(f"Не удалось прочитать файл {filename}: {e}") from e
    

    #try:   
    #    ds_models = await get_openai_models()
    #except Exception as e:
    #    raise ValueError(f"Не удалось получить доступные модели ИИ: {e}") from e


    #for model in ds_models:
    try:
        response = await ds_client.responses.create(
            model="deepseek-v4.1-flash",
            input=[{"role": "user", "content": contents}],
            text={"format": {"type": "json_object"}}
            )       
        
        if response.output_text:
            ai_text_list = json.loads(response.output_text)

            if not isinstance(ai_text_list, (dict, list)):
                raise ValueError("[ai_analyze_pdf] Ожидался JSON объект или список")
        
            return ai_text_list


    except Exception as e:
        print(f"[DS] не дала пригодный ответ: {e}")
    return None

