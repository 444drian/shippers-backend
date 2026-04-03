from pydantic import BaseModel
from typing import List, Optional


class Partida(BaseModel):
    num_partida: int
    fraccion: str
    origen: str
    descripcion: str
    cantidad: float
    peso: float
    valor_pesos: float
    valor_dolares: float

class ContenidoPedimento(BaseModel):
    tipo_cambio: float
    peso_bruto: float
    valor_dolares: float
    valor_calculado: float
    num_partidas: int
    partidas: List[Partida]


class Pedimento(BaseModel):
    nume_ped: str
    contenido: List[ContenidoPedimento]


class PedimentoData(BaseModel):
    pedimentos: List[Pedimento]


class ApiResponse(BaseModel):
    success: bool
    data: PedimentoData
    error: Optional[str] = None