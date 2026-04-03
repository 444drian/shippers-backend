from fastapi import UploadFile
from io import BytesIO
from app.processors.pdf_processor import PDFProcessor
from app.processors.pedimento_processor import PedimentoProcessor

class FileService:

    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.pedimento_processor = PedimentoProcessor()

    async def process_files(self, files: list[UploadFile]):
        all_pedimentos = []

        for file in files:
            content = await file.read()

            print("\n--- 📄 Procesando PDF ---")
            print("Nombre:", file.filename)

            text = self.pdf_processor.extract_text(content)
            lines = self.pdf_processor.normalize_text(text)
            result = self.pedimento_processor.process(lines)

            # print("📊 Total líneas:", len(lines))
            # print("🔎 Primera línea:", lines[0] if lines else "VACÍO")

            # 🔥 Extraer y acumular
            pedimentos = result.get("pedimentos", [])
            all_pedimentos.extend(pedimentos)

        print(all_pedimentos)


        return {
            "success": True,
            "data": {
                "pedimentos": all_pedimentos
            },
            "error": None
        }  

    


        


    