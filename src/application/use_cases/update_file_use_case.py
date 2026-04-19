from src.application.dto.file import UpdateFile

class UpdateFileUseCase:
    def __init__(self, repository):
        self.repository = repository
        
    async def execute(self, parameters: UpdateFile):
        try:
            record = await self.repository.update_file(file_id=parameters.id, filename=parameters.filename)
            
            return record
        except Exception as e:
            raise e