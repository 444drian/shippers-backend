from app.services.file_service import FileService
from app.services.hoja_trabajo_service import HojaTrabajoService
from app.services.s_bay_service import SBayService
from app.schemas.file_schema import ApiResponse

class FileOrchestrator:

    def __init__(self):
        self.pedimento_service = FileService()
        self.hoja_service = HojaTrabajoService()
        self.s_bay_service = SBayService()

    async def process(self, files, file_type):

        if file_type == "pedimento":
            return await self.pedimento_service.process_files(files)

        elif file_type == "hoja_trabajo":
            return await self.hoja_service.process_files(files)

        elif file_type == "s_bay":
            return await self.s_bay_service.process_files(files)
        else:
            raise Exception(f"Tipo no soportado: {file_type}")