from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# ========================
# Esquemas para Usuarios
# ========================
class UsuarioBase(BaseModel):
    username: str

class UsuarioCreate(UsuarioBase):
    password: str
    role: Optional[str] = "empleado"

class UsuarioResponse(UsuarioBase):
    id: int
    role: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# ========================
# Esquemas para Inventario
# ========================
class InventarioBase(BaseModel):
    codigo: str
    nombre_producto: str
    cantidad_disponible: int
    precio_unitario: float

class InventarioCreate(InventarioBase):
    pass

class InventarioResponse(InventarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ========================
# Esquemas para Ventas
# ========================
class VentaBase(BaseModel):
    producto_id: int
    cantidad: int
    vendedor: str
    cliente_nombre: str
    cliente_contacto: str
    cliente_telefono: str
    cliente_email: str

class VentaCreate(VentaBase):
    pass

class VentaResponse(VentaBase):
    id: int
    fecha_venta: datetime
    precio_unitario: float
    total_venta: float
    producto: Optional[InventarioResponse] = None
    model_config = ConfigDict(from_attributes=True)

# ========================
# Esquemas para Finanzas
# ========================
class FinanzaResponse(BaseModel):
    id: int
    descripcion: str
    tipo: str
    monto: float
    fecha: datetime
    responsable: str
    model_config = ConfigDict(from_attributes=True)
