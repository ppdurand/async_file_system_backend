class DeleteFileUseCase:
    def __init__(self, repository):
        self.repository = repository
    
    async def execute(self, id):
        try:
            record = await self.repository.delete_file(id)
            return record
        except Exception as e:
            raise e
        
        