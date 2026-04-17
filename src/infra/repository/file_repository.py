import os
import uuid
import hashlib
from src.infra.models.file import File

class FileRepository:
    def __init__(self, db):
        self.db = db
        self.upload_dir = "uploads"

    def upload_file(self, filename, content) -> File:
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