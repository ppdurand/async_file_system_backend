from pydantic import BaseModel
from datetime import datetime

class UploadFile(BaseModel):
    filename: str
    content: bytes
    
    class Config:
        arbitrary_types_allowed = True


class FileResponse(BaseModel):
    id: str
    filename: str
    filepath: str
    file_size: int
    file_hash: str = None
    mime_type: str = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True  
        json_encoders = {
            datetime: lambda v: v.isoformat() 
        }

class FileDownload(BaseModel):
    content: bytes
    filename: str
    content_type: str
    file_size: int
    
    class Config:
        arbitrary_types_allowed = True