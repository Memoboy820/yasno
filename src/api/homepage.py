from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

INDEX_PATH = (Path(__file__).resolve().parent.parent.parent / "templates" / "index.html")

@router.get("/")
async def homepage():
    return FileResponse(INDEX_PATH)