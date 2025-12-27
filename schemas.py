from pydantic import BaseModel

# 1. Esquema Base (Lo que tienen en común)
class TareaBase(BaseModel):
    titulo: str
    descripcion: str | None = None # Puede ser texto o vacío (None)
    completada: bool = False

# 2. Esquema para CREAR (Lo que pedimos al usuario)
# Hereda de TareaBase, así que pide titulo, descripción y completada.
class TareaCreate(TareaBase):
    pass 

# 3. Esquema para RESPONDER (Lo que le mostramos al usuario)
class TareaResponse(TareaBase):
    id: int  # Le agregamos el ID, porque la base de datos ya lo generó
    owner_id: int

    class Config:
        # Esta línea es CLAVE. Le permite a Pydantic leer datos de
        # un modelo de Base de Datos (ORM) y no solo de diccionarios.
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