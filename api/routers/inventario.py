from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api.database import get_db
from api.models import Inventario
from api.schemas import InventarioCreate, InventarioResponse

router = APIRouter(
    prefix="/inventario",
    tags=["Inventario"]
)

@router.post("/", response_model=InventarioResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: InventarioCreate, db: Session = Depends(get_db)):
    db_producto = db.query(Inventario).filter(
        (Inventario.codigo == producto.codigo) | 
        (Inventario.nombre_producto == producto.nombre_producto)
    ).first()
    
    if db_producto:
        raise HTTPException(status_code=400, detail="El código o nombre del producto ya existe")
    
    nuevo_producto = Inventario(**producto.model_dump())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

@router.get("/", response_model=List[InventarioResponse])
def listar_inventario(db: Session = Depends(get_db)):
    return db.query(Inventario).all()

@router.get("/{producto_id}", response_model=InventarioResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Inventario).filter(Inventario.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{producto_id}", response_model=InventarioResponse)
def actualizar_producto(producto_id: int, producto_update: InventarioCreate, db: Session = Depends(get_db)):
    producto = db.query(Inventario).filter(Inventario.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    for key, value in producto_update.model_dump().items():
        setattr(producto, key, value)
    
    db.commit()
    db.refresh(producto)
    return producto

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Inventario).filter(Inventario.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(producto)
    db.commit()
    return None

