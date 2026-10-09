from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from api.database import get_db
from api.models import Inventario, Venta, Finanza
from api.schemas import VentaCreate, VentaResponse

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)

@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def registrar_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el producto existe
    producto = db.query(Inventario).filter(Inventario.id == venta.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # 2. Verificar disponibilidad de stock
    if producto.cantidad_disponible < venta.cantidad:
        raise HTTPException(status_code=400, detail=f"Stock insuficiente. Disponible: {producto.cantidad_disponible}")
    
    # 3. Calcular totales
    total_venta = venta.cantidad * producto.precio_unitario

    # 4. Registrar la Venta
    nueva_venta = Venta(
        producto_id=venta.producto_id,
        cantidad=venta.cantidad,
        precio_unitario=producto.precio_unitario,
        total_venta=total_venta,
        vendedor=venta.vendedor,
        cliente_nombre=venta.cliente_nombre,
        cliente_contacto=venta.cliente_contacto,
        cliente_telefono=venta.cliente_telefono,
        cliente_email=venta.cliente_email
    )
    db.add(nueva_venta)

    # 5. Descontar del inventario
    producto.cantidad_disponible -= venta.cantidad

    # 6. Registrar en Finanzas
    nuevo_ingreso = Finanza(
        descripcion=f"Ingreso por venta de {producto.nombre_producto} (Venta ID: autogenerado)",
        tipo="Ingreso",
        monto=total_venta,
        responsable=venta.vendedor
    )
    db.add(nuevo_ingreso)

    # Confirmar todas las operaciones (Transacción ACID automática en SQLAlchemy)
    db.commit()
    db.refresh(nueva_venta)
    
    # Actualizar la descripción de la finanza con el ID real de la venta
    nuevo_ingreso.descripcion = f"Ingreso por venta de {producto.nombre_producto} (Venta ID: {nueva_venta.id})"
    db.commit()

    return nueva_venta

@router.get("/", response_model=List[VentaResponse])
def listar_ventas(db: Session = Depends(get_db)):
    return db.query(Venta).all()
