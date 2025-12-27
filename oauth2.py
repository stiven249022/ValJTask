from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import token_jwt
from sqlalchemy.orm import Session
import database
import models

# Esto le dice a FastAPI dónde obtener el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

# oauth2.py

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    # 1. Verificamos el token
    # Esta función te devuelve el ID del usuario como un texto (ej: "1")
    token_data = token_jwt.verificar_token(token) 
    
    if token_data is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    # 2. Buscamos al usuario en la BD
    # ❌ ANTES (Error): filter(models.Usuario.id == token_data.id)
    # ✅ AHORA (Correcto): Usamos token_data directamente y lo convertimos a entero
    usuario = db.query(models.Usuario).filter(models.Usuario.id == int(token_data)).first()
    
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
    return usuario