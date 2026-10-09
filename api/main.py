from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import models
from api.database import engine
from api.routers import usuarios, inventario, ventas

# Esta línea le dice a SQLAlchemy que cree todas las tablas en SQLite
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SAD API (ERP)", 
    description="API RESTful para el Sistema de Administración de Datos", 
    version="1.0.0"
)

# Configurar CORS (Permite que React se comunique con esta API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # URL de Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(usuarios.router)
app.include_router(inventario.router)
app.include_router(ventas.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del ERP SAD"}

@app.get("/status")
def status():
    return {"status": "El backend está funcionando correctamente"}
