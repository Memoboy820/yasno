from fastapi import APIRouter
from .ai import router as ai_router
from .homepage import router as homepage_router 

main_router = APIRouter()

main_router.include_router(ai_router)
main_router.include_router(homepage_router)