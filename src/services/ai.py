from src.constants import models, ai_client
from google.genai import types
from src.constants import AI_FILE_ANALYSIS_ANALYSIS_PROMPT, AI_FILE_ANALYSIS_ANALYSIS_STARTING_PROMPT
import json


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