from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from src.api import main_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], # "*" - все можно
    allow_methods=["*"],
    allow_credentials=False, # учетные данные
    allow_headers=["*"]
)
#  uvicorn main:app --reload 
#  fastapi dev ЯСНО\scr\main.py

app.include_router(main_router)
