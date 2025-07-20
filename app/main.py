from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Crear la instancia de FastAPI
app = FastAPI(
    title="OpenFGA FastAPI LinkedIn Course",
    description="Curso de LinkedIn sobre autorización avanzada con OpenFGA",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint de prueba para verificar que la aplicación funciona"""
    return {
        "message": "¡Bienvenido al curso de OpenFGA con FastAPI!",
        "course": "LinkedIn - Autorización Avanzada con OpenFGA",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)