from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import hashlib

from api.database import get_db
from api.models import Usuario
from api.schemas import UsuarioCreate, UsuarioResponse

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(user: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    db_user = db.query(Usuario).filter(Usuario.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    
    # Crear el nuevo usuario
    hashed_pwd = hash_password(user.password)
    nuevo_usuario = Usuario(username=user.username, password=hashed_pwd, role=user.role)
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post("/login")
def login(user: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.username == user.username).first()
    if not db_user or db_user.password != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    return {"message": "Login exitoso", "role": db_user.role, "user_id": db_user.id}

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()
