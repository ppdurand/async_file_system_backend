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
            unique_name = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(self.upload_dir, unique_name)

            os.makedirs(self.upload_dir, exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(content)

            file_hash = hashlib.sha256(content).hexdigest()

            file_record = File(
                id=str(uuid.uuid4()),
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