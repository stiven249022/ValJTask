from pydantic import BaseModel, field_validator # <--- Importamos el validador
from datetime import datetime
from typing import Optional
# 1. Esquema Base (Lo que tienen en común)
class TareaBase(BaseModel):
    titulo: str
    descripcion: str | None = None # Puede ser texto o vacío (None)
    completada: bool = False

# 2. Esquema para CREAR (Lo que pedimos al usuario)
# Hereda de TareaBase, así que pide titulo, descripción y completada.
class TareaCreate(BaseModel):
    titulo: str
    descripcion: str
    fecha_entrega: datetime # <--- Campo nuevo obligatorio

    # --- VALIDACIÓN PERSONALIZADA ---
    # Esto revisa automáticamente que la fecha no sea del pasado
    @field_validator('fecha_entrega')
    def validar_fecha_futura(cls, fecha):
        # Si la fecha que mandan es menor (<) a "ahora mismo"
        if fecha < datetime.now():
            raise ValueError('¡La fecha de entrega no puede estar en el pasado!')
        return fecha

# 2. Esquema para RESPONDER una tarea (Lo que devuelve la API)
class TareaResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    fecha_inicio: datetime # <--- Mostramos cuándo se creó
    fecha_entrega: Optional[datetime] # <--- Mostramos cuándo vence
    owner_id: int

    class Config:
        from_attributes = True
        
# --- ESQUEMAS DE USUARIO ---

class UsuarioBase(BaseModel):
    email: str 

class UsuarioCreate(UsuarioBase):
    password: str  # Solo pedimos la contraseña al crear

class UsuarioResponse(UsuarioBase):
    id: int
    is_active: bool
    # OJO: ¡NUNCA devolvemos la contraseña aquí! 

    class Config:
        from_attributes = True