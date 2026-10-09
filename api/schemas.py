from pydantic import BaseModel
from typing import Optional

# Esquemas para Usuarios
class UsuarioBase(BaseModel):
    username: str

class UsuarioCreate(UsuarioBase):
    password: str
    role: Optional[str] = "empleado"

class UsuarioResponse(UsuarioBase):
    id: int
    role: Optional[str] = None

    class Config:
        from_attributes = True

# Puedes agregar más esquemas para Inventario y Ventas aquí después
