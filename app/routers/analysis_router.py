from fastapi import APIRouter, Request
import json
from app.services.analysis_service import AnalysisService

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

service = AnalysisService()

@router.post("/analizar")
async def analizar(request: Request):

    payload = await request.json()

    # print("\n🚀 PAYLOAD RECIBIDO\n")
    # print(json.dumps(payload, indent=2, ensure_ascii=False))

    resultado = service.procesar(payload)

    print("\n✅ RESULTADO GENERADO\n")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    return {
        "success": True,
        "data": resultado
    }