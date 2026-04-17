from src.infra.database import Base
from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime
import uuid

class File(Base):
    __tablename__ = "files"
    
    id = Column(String(36), primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String, index=True)
    file_size = Column(Integer, nullable=True)
    file_hash = Column(String(64), nullable=True)
    status = Column(String(20), default="uploaded")
    created_at = Column(DateTime, default=datetime.utcnow)
