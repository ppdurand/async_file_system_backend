from src.application.dto.file import UploadFile

class UploadFileUseCase:
    def __init__(self, file_repository):
        self.file_repository = file_repository

    async def execute(self, parameters: UploadFile):
        try:
            record = self.file_repository.upload_file(
                filename=parameters.filename,
                content=parameters.content
            )
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }
            
        return { "success": True, "data": record }