from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from api.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, nullable=True)

class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    nombre_producto = Column(String, index=True)
    cantidad_disponible = Column(Integer, default=0)
    precio_unitario = Column(Float)
    
    # Relación: Un producto puede tener muchas ventas
    ventas = relationship("Venta", back_populates="producto")

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_venta = Column(DateTime, default=datetime.utcnow)
    
    # Clave Foránea: Relaciona la venta directamente con un producto del inventario
    producto_id = Column(Integer, ForeignKey("inventario.id"))
    producto = relationship("Inventario", back_populates="ventas")
    
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    total_venta = Column(Float)
    
    # (Nota: En un ERP real, Cliente y Vendedor también serían tablas separadas relacionadas)
    vendedor = Column(String)
    cliente_nombre = Column(String)
    cliente_contacto = Column(String)
    cliente_telefono = Column(String)
    cliente_email = Column(String)

class Finanza(Base):
    __tablename__ = "finanzas"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    tipo = Column(String) # Ejemplo: "Ingreso", "Egreso"
    monto = Column(Float)
    fecha = Column(DateTime, default=datetime.utcnow)
    responsable = Column(String)
