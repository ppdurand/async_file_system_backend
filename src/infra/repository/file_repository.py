import os
import uuid
import hashlib
from src.infra.models.file import File
from src.application.dto.file import FileResponse, FileBasicInfo

class FileRepository:
    def __init__(self, db):
        self.db = db
        self.upload_dir = "uploads"

    def upload_file(self, filename, content) -> FileResponse:
        try:
            id = str(uuid.uuid4())
            unique_name = f"{filename}_{id}"
            file_path = os.path.join(self.upload_dir, unique_name)

            os.makedirs(self.upload_dir, exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(content)

            file_hash = hashlib.sha256(content).hexdigest()

            file_record = File(
                id=id,
                filename=filename,
                filepath=file_path,
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
        
    async def update_file(self, file_id, filename) -> FileBasicInfo:
        try:
            query = self.db.query(File).filter(File.id == file_id).first()
            if not query:
                raise Exception("File not found")
            
            old_path = os.path.join("uploads", f"{query.filename}_{query.id}")
            new_path = os.path.join("uploads", f"{filename}_{query.id}")
            
            print(old_path, new_path)
            
            if not os.path.exists(old_path):
                raise Exception("File not found in filesystem")
            
            os.rename(old_path, new_path)
            
            query.filename = filename
            query.filepath = new_path
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
            
            print("CWD:", os.getcwd())
            print("PATH:", query.filepath)
            print("ABS:", os.path.abspath(query.filepath))
            print("EXISTS:", os.path.exists(query.filepath))
            os.remove(query.filepath)
                
            self.db.delete(query)
            self.db.commit()
            self.db.refresh(query)
            
        except Exception as e:
            self.db.rollback()
            raise e
