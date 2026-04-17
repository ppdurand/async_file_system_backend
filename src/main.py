from fastapi import FastAPI
from src.presentation.routes.file_routes import router as file_router

app = FastAPI()

app.include_router(file_router)