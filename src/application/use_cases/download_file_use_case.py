class DownloadFileUseCase:
    def __init__(self, file_repository):
        self.file_repository = file_repository
    
    async def execute(self, file_id: str):
        return await self.file_repository.download_file(file_id)
        
    