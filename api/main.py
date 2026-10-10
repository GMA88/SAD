from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import models
from api.database import engine
from api.routers import usuarios, inventario, ventas, ai

# Esta línea le dice a SQLAlchemy que cree todas las tablas en SQLite
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SAD API (ERP)", 
    description="API RESTful para el Sistema de Administración de Datos", 
    version="1.0.0"
)

# Configurar CORS (Permite que React se comunique con esta API desde cualquier puerto local)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(usuarios.router)
app.include_router(inventario.router)
app.include_router(ventas.router)
app.include_router(ai.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del ERP SAD"}

@app.get("/status")
def status():
    return {"status": "El backend está funcionando correctamente"}

from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
import hashlib
from api.database import get_db

@app.post("/seed")
def seed_data(db: Session = Depends(get_db)):
    """Poblar la base de datos con datos realistas para demostración y analítica"""
    # 1. Crear usuarios demo si no existen
    if db.query(models.Usuario).count() == 0:
        demo_users = [
            ("admin", "admin123", "Administrador"),
            ("carlos_ventas", "pass123", "Vendedor"),
            ("lucia_gerente", "pass123", "Gerente")
        ]
        for username, pwd, role in demo_users:
            hpwd = hashlib.sha256(pwd.encode()).hexdigest()
            db.add(models.Usuario(username=username, password=hpwd, role=role))
        db.commit()

    # 2. Crear productos de prueba si no existen
    productos_base = [
        {"codigo": "PRD-001", "nombre_producto": "Laptop Profesional 16 Ultra", "cantidad_disponible": 14, "precio_unitario": 1250.0},
        {"codigo": "PRD-002", "nombre_producto": "Monitor Panorámico 27 4K", "cantidad_disponible": 4, "precio_unitario": 380.0},
        {"codigo": "PRD-003", "nombre_producto": "Teclado Mecánico RGB Pro", "cantidad_disponible": 28, "precio_unitario": 95.0},
        {"codigo": "PRD-004", "nombre_producto": "Mouse Ergonómico Inalámbrico", "cantidad_disponible": 3, "precio_unitario": 55.0},
        {"codigo": "PRD-005", "nombre_producto": "Silla Ergonómica Mesh Office", "cantidad_disponible": 8, "precio_unitario": 240.0},
        {"codigo": "PRD-006", "nombre_producto": "Auriculares Cancelación Ruido", "cantidad_disponible": 19, "precio_unitario": 150.0},
        {"codigo": "PRD-007", "nombre_producto": "Hub USB-C 8 en 1 Multipuerto", "cantidad_disponible": 2, "precio_unitario": 65.0}
    ]

    for p in productos_base:
        existente = db.query(models.Inventario).filter(models.Inventario.codigo == p["codigo"]).first()
        if not existente:
            db.add(models.Inventario(**p))
    db.commit()

    # 3. Crear ventas históricas distribuidas en los últimos 10 días
    if db.query(models.Venta).count() < 5:
        prods = db.query(models.Inventario).all()
        clientes = [
            ("Tech Solutions S.A.", "tech@example.com", "+52 55 1234 5678"),
            ("Corporativo Andino", "compras@andino.com", "+52 55 8765 4321"),
            ("Innovaciones Digitales", "contacto@innovacion.mx", "+52 33 2211 4455"),
            ("Desarrollos Alfa", "finanzas@alfa.com", "+52 81 9988 7766"),
            ("Consultoría Nova", "admin@nova.org", "+52 55 4433 2211")
        ]
        vendedores = ["Carlos Gómez", "Lucía Peña", "Mario Silva"]

        now = datetime.utcnow()
        for i in range(12):
            prod = random.choice(prods)
            cliente = random.choice(clientes)
            cant = random.randint(1, 3)
            total = cant * prod.precio_unitario
            # Fecha retroactiva
            dias_atras = random.randint(0, 9)
            horas_atras = random.randint(1, 23)
            fecha_venta = now - timedelta(days=dias_atras, hours=horas_atras)

            venta = models.Venta(
                producto_id=prod.id,
                cantidad=cant,
                precio_unitario=prod.precio_unitario,
                total_venta=total,
                vendedor=random.choice(vendedores),
                cliente_nombre=cliente[0],
                cliente_email=cliente[1],
                cliente_telefono=cliente[2],
                cliente_contacto=cliente[0],
                fecha_venta=fecha_venta
            )
            db.add(venta)

            finanza = models.Finanza(
                descripcion=f"Ingreso por venta demo de {prod.nombre_producto}",
                tipo="Ingreso",
                monto=total,
                fecha=fecha_venta,
                responsable="Sistema Demo"
            )
            db.add(finanza)
        db.commit()

    return {"message": "Datos de prueba cargados exitosamente"}

