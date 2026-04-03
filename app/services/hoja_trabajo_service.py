from fastapi import UploadFile
from app.processors.excel_processor import ExcelProcessor
from app.processors.hoja_trabajo_processor import HojaTrabajoProcessor


class HojaTrabajoService:

    def __init__(self):
        self.excel_processor = ExcelProcessor()
        self.processor = HojaTrabajoProcessor()

    async def process_files(self, files: list[UploadFile]):

        all_pedimentos = []

        for file in files:
            content = await file.read()

            print("\n--- 📄 Procesando Excel ---")
            print("Nombre:", file.filename)

            # 🔥 1. Leer Excel
            df = self.excel_processor.read_excel(content)

            # 🔥 2. Procesar
            result = self.processor.process(df)

            # 🔥 3. Acumular
            pedimentos = result.get("pedimentos", [])
            all_pedimentos.extend(pedimentos)

        print("📦 Resultado final:", all_pedimentos)

        return {
            "success": True,
            "data": {
                "pedimentos": all_pedimentos
            },
            "error": None
        }