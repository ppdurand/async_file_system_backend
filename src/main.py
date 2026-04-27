from fastapi import FastAPI
from src.infra.database import Base, engine
from src.domain.models import File 
from src.presentation.routes.file_routes import router as file_router
from infra.clients.minio.minio_client import minio_client

app = FastAPI()

app.include_router(file_router)

Base.metadata.create_all(bind=engine)

BUCKET_NAME = 'arquivos'

@app.on_event("startup")
def init_minio():
    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)