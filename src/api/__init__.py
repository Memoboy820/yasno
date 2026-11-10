from fastapi import APIRouter
from .ai import router as current_router 

main_router = APIRouter()

main_router.include_router(current_router)