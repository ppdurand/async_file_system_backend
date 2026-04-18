class ListFilesUseCase:
    def __init__(self, file_repository):
        self.file_repository = file_repository

    async def execute(self):
        try:
            files = await self.file_repository.list_files()
            return files
        except Exception as e:
            raise e