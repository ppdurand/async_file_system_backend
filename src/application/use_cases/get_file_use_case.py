class GetFileUseCase:
    def __init__(self, file_repository):
        self.file_repository = file_repository
    
    async def execute(self, file_id: str):
        try:
            record = await self.file_repository.get_file(file_id)
            return record
        except Exception as e:
            print("ERROUSECASE =>", e)
            raise e
        
        
    