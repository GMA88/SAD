from fastapi import FastAPI
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
