# app/services/s_bay_service.py
from fastapi import UploadFile
from app.services.ocr.ocr_service import OCRService
from app.schemas.file_schema import ApiResponse


class SBayService:

    def __init__(self):
        self.ocr_service = OCRService()

    async def process_files(self, files: list[UploadFile]):

   
        results = []
        for file in files:
            try:
                content = await file.read()

                text = self.ocr_service.extract_text_from_pdf(content)
                print(f"Texto extraído de {file.filename}:\n{text}\n{'-'*40}")

                results.append({
                    "file_name": file.filename,
                    "text": text
                })

            except Exception as e:
                print(f"ERROR PROCESANDO {file.filename}: {e}")  # 👈 AGREGA ESTO
                results.append({
                    "file_name": file.filename,
                    "error": str(e)
                })

        return ApiResponse(
            success=True,
            message="Procesamiento OCR completado",
            data={"files": results}
        )