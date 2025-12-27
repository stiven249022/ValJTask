from sqlalchemy.orm import Session
from models import Usuario, Tarea # Importamos los modelos
import schemas
from hashing import Hash
import models
def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    # El repo se encarga del hashing y la creación
    hashed_pass = Hash.bcrypt(usuario.password)
    nuevo_usuario = Usuario(
        email=usuario.email,
        hashed_password=hashed_pass,
        rol="estudiante" # 🎭 Valor por defecto
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def buscar_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

# Esta la usaremos luego para la lógica de tareas
def obtener_mis_tareas(db: Session, usuario_id: int):
    return db.query(Tarea).filter(Tarea.owner_id == usuario_id).all()
def cambiar_rol(db: Session, user_id: int, nuevo_rol: str):
    usuario_query = db.query(models.Usuario).filter(models.Usuario.id == user_id)
    usuario = usuario_query.first()
    
    if not usuario:
        return None # El cocinero avisa que no encontró el ingrediente
        
    usuario_query.update({"rol": nuevo_rol})
    db.commit()
    db.refresh(usuario)
    return usuario