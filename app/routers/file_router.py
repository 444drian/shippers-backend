from fastapi import APIRouter, UploadFile, File, Form
from app.schemas.file_schema import ApiResponse
from app.services.file_orchestrator import FileOrchestrator

router = APIRouter(prefix="/files", tags=["Files"])

orchestrator = FileOrchestrator()

@router.post("/procesar", response_model=ApiResponse)
async def procesar_archivos(
    files: list[UploadFile] = File(...),
    file_type: str = Form(...)
):
    return await orchestrator.process(files, file_type)

