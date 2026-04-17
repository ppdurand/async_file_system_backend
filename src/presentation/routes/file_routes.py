from sqlalchemy.orm import Session
from src.infra.database import get_db
from fastapi import APIRouter, UploadFile, Depends
from src.infra.repository.file_repository import FileRepository
from src.application.use_cases.update_file_use_case import UploadFileUseCase
from src.application.dto.file import UploadFile as UploadFileParameter

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    content = await file.read()
    
    file_repository = FileRepository(db)
    use_case = UploadFileUseCase(file_repository)
    parameters = UploadFileParameter(filename=file.filename, content=content)
    
    response = use_case.execute(parameters)
    
    if response['success'] == False:
        return {"success": False, "message": response['message']}
    
    return {"success": True, "data": response['data']}
