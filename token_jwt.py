from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from fastapi import HTTPException

# 1. CONFIGURACIÓN SECRETA (Como la receta de la Coca-Cola)
# Cambia esta clave por algo muy largo y secreto luego
SECRET_KEY = "tu_llave_super_secreta_para_el_proyecto_tareas"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # La pulsera dura 30 minutos

def crear_token_acceso(data: dict):
    # Hacemos una copia de los datos (el ID del usuario)
    to_encode = data.copy()
    
    # Calculamos cuándo debe vencer la pulsera
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Agregamos la fecha de vencimiento a los datos
    to_encode.update({"exp": expire})
    
    # Firmamos el Token con nuestra llave secreta
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verificar_token(token: str):
    try:
        # Intentamos abrir la pulsera con nuestra llave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return user_id # Retornamos el ID del usuario que venía dentro
    except JWTError:
        raise HTTPException(status_code=401, detail="No se pudo validar la identidad")