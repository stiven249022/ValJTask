from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from oauth2 import get_current_user
import models
# Importamos el repositorio y otros útiles
from repository import user_repo 
import schemas
import database
from hashing import Hash
import token_jwt
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- REGISTRO ---
@router.post("/", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Le pedimos al repo que busque el email
    usuario_existente = user_repo.buscar_por_email(db, usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # 2. Le pedimos al repo que cree el usuario (él ya sabe hashear la clave)
    return user_repo.crear_usuario(db, usuario)

# --- LOGIN ---
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Buscamos al usuario usando el repo
    usuario = user_repo.buscar_por_email(db, form_data.username)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # 2. Validamos la contraseña
    if not Hash.verify(form_data.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    # 3. Generamos el token
    access_token = token_jwt.crear_token_acceso(data={"sub": str(usuario.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.patch("/{user_id}/rol", response_model=schemas.UsuarioResponse)
def ascender_a_profesor(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user) # Obtenemos el usuario completo
):
    # 🛡️ VALIDACIÓN DE SEGURIDAD MÁXIMA:
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden cambiar roles")

    # Ejecutamos la acción en el repo
    usuario_actualizado = user_repo.cambiar_rol(db, user_id, nuevo_rol="profesor")
    
    if not usuario_actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    return usuario_actualizado