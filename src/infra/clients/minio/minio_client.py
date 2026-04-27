import os
from minio import Minio
endpoint = os.getenv("MINIO_ENDPOINT")

minio_client = Minio(
    endpoint=endpoint,
    access_key=os.getenv("MINIO_ROOT_USER"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
    secure=False
)
