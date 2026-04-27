import os
import io
import uuid
import hashlib
from src.domain.models import File
from src.application.dto.file import FileResponse, FileBasicInfo
from infra.clients.minio.minio_storage import MinioStorage

class FileRepository:
    def __init__(self, db, minio_storage: MinioStorage):
        self.db = db
        self.storage = minio_storage
        self.upload_dir = "uploads"

    def upload_file(self, filename, content) -> FileResponse:
        try:
            id = str(uuid.uuid4())
            unique_name = f"{id}_{filename}"
                
            self.storage.upload(
                bucket_name='arquivos', 
                object_name=unique_name, 
                data=io.BytesIO(content), 
                length=len(content)
            )

            file_hash = hashlib.sha256(content).hexdigest()

            file_record = File(
                id=id,
                filename=filename,
                filepath=unique_name,
                file_size=len(content),
                file_hash=file_hash,
                status="uploaded"
            )

            self.db.add(file_record)
            self.db.commit()
            self.db.refresh(file_record)
        except Exception as e:
            self.db.rollback()
            raise e

        return file_record
    
    async def list_files(self) -> list[FileBasicInfo]:
        try:
            query = self.db.query(
                File.id, File.filename, File.file_size, File.status
            ).all()
            
            return list(map(lambda x: FileBasicInfo(
                id=x.id,
                filename=x.filename,
                file_size=x.file_size,
                status=x.status
            ), query))
        except Exception as e:
            raise e
    
    async def get_file(self, file_id) -> FileResponse:
        try:
            query = self.db.query(
                File
            ).filter(File.id == file_id).first()

            if query is None:
                return None

            return FileResponse(
                id=query.id,
                filename=query.filename,
                filepath=query.filepath,
                file_size=query.file_size,
                file_hash=query.file_hash,
                status=query.status,
                created_at=query.created_at
            )
        except Exception as e:
            print("ERRO ->", e)
            raise e
        
    async def update_file(self, file_id, filename) -> FileResponse:
        try:
            query = self.db.query(File).filter(File.id == file_id).first()
            if not query:
                raise Exception("File not found")

            result = self.storage.get(
                bucket_name='arquivos',
                object_name=query.filepath
            )
            content = result.read()
            result.close()
            result.release_conn()

            new_filepath = f"{query.id}_{filename}"
            self.storage.upload(
                bucket_name='arquivos',
                object_name=new_filepath,
                data=io.BytesIO(content),
                length=len(content)
            )

            self.storage.delete(
                bucket_name='arquivos',
                object_name=query.filepath
            )
            
            query.filename = filename
            query.filepath = new_filepath
            self.db.commit()
            self.db.refresh(query)

            return FileResponse(
                id=query.id,
                filename=query.filename,
                filepath=query.filepath,
                file_size=query.file_size,
                file_hash=query.file_hash,
                status=query.status,
                created_at=query.created_at
            )
        except Exception as e:
            self.db.rollback()
            raise e
    
    async def delete_file(self, file_id) -> bool:
        try:
            query = self.db.query(
                File
            ).filter(File.id == file_id).first()
            
            if not query:
                raise Exception("File not found")
            
            self.storage.delete(
                bucket_name='arquivos', 
                object_name=query.filepath
            )
                
            self.db.delete(query)
            self.db.commit()
            
            return True
        except Exception as e:
            self.db.rollback()
            raise e
        
    async def download_file(self, file_id: str):
        try:
            query = self.db.query(File).filter(File.id == file_id).first()
            if query is None:
                return None

            result = self.storage.get(
                bucket_name='arquivos',
                object_name=query.filepath
            )
            content = result.read()
            result.close()
            result.release_conn()

            return {"filename": query.filename, "content": content}
        except Exception as e:
            raise e
