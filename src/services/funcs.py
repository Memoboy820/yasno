from src.constants import ds_client

async def ai_files_create(filename, file_bytes) -> dict:
    uploaded = await ds_client.files.create(
        file=(filename, file_bytes),
        purpose="user_data",
    )

    return {"type": "input_file", "file_id": uploaded.id,}   