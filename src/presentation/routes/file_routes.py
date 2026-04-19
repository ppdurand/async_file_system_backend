from sqlalchemy.orm import Session
from src.infra.database import get_db
from fastapi import APIRouter, UploadFile, Depends, Body
from src.infra.repository.file_repository import FileRepository
from src.application.use_cases import UploadFileUseCase, ListFilesUseCase, GetFileUseCase, UpdateFileUseCase, DeleteFileUseCase
from src.application.dto.file import UploadFile as UploadFileParameter, UpdateFile as UpdateFileParameter

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    content = await file.read()
    
    file_repository = FileRepository(db)
    use_case = UploadFileUseCase(file_repository)
    parameters = UploadFileParameter(filename=file.filename, content=content)
    
    response = await use_case.execute(parameters)
    
    if response['success'] == False:
        return {"success": False, "message": response['message']}
    
    return {"success": True, "data": response['data']}

@router.get("/files")
async def list_files(db: Session = Depends(get_db)):
    file_repository = FileRepository(db)
    
    use_case = ListFilesUseCase(file_repository)
    
    response = await use_case.execute()
    return {"success": True, "data": response}

@router.get("/files/{file_id}")
async def get_file(file_id: str, db: Session = Depends(get_db)):
    repo = FileRepository(db)
    
    use_case = GetFileUseCase(repo)
    
    response = await use_case.execute(file_id)
    
    return response

@router.put("/files/{file_id}")
async def update_file(file_id, filename: str = Body(..., embed=True), db: Session = Depends(get_db)):
    repo = FileRepository(db)
    
    use_case = UpdateFileUseCase(repo)
    parameters = UpdateFileParameter(
        id=file_id, filename=filename
    )
    
    response = await use_case.execute(parameters)
    
    return response

@router.delete("/files/{file_id}")
async def delete_file(file_id: str, db: Session = Depends(get_db)):
    repo = FileRepository(db)
    
    use_case = DeleteFileUseCase(repo)
    response = await use_case.execute(file_id)
    
    if response is not True:
        return {"success": False, "error": response}
    
    return {"success": True, "message": "Arquivo apagado com sucesso!"}