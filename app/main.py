from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import file_router
from app.routers import analysis_router

app = FastAPI()

# 🔥 CONFIGURACIÓN CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # permitir todo (por ahora)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_router.router)
app.include_router(analysis_router.router)