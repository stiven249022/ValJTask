from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from oauth2 import get_current_user # Importa el portero
# CORRECCIÓN: Una importación por línea
import models
import schemas
import database
from fastapi import status

router = APIRouter(
    prefix="/tareas",
    tags=["Tareas"]
)
# ... (el resto del código sigue igual)

# 2. LA DEPENDENCIA (El Bibliotecario)
# La copiamos aquí porque la necesitamos para las rutas
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- RUTAS (Fíjate que ahora usamos @router en vez de @app) ---

# GET /tareas
@router.get("/", response_model=List[schemas.TareaResponse])
def obtener_tareas(db: Session = Depends(get_db)):
    return db.query(models.Tarea).all()

# POST /tareas

# routers/tareas.py

@router.post("/", response_model=schemas.TareaResponse)
def crear_tarea(
    tarea: schemas.TareaCreate, 
    db: Session = Depends(get_db),
    # 1. CAMBIO DE NOMBRE: Ya no es solo un ID, es el usuario completo (Admin, Profe, etc.)
    current_user: models.Usuario = Depends(get_current_user) 
):
    nueva_tarea = models.Tarea(
        titulo=tarea.titulo,
        descripcion=tarea.descripcion,
        # 2. ACCESO AL DATO: Del objeto completo, sacamos solo el ID
        owner_id=current_user.id  
    )
    
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    
    return nueva_tarea

# PUT /tareas/{id}
@router.put("/{task_id}", response_model=schemas.TareaResponse)
def actualizar_tarea(task_id: int, tarea_actualizada: schemas.TareaCreate, db: Session = Depends(get_db)):
    tarea_db = db.query(models.Tarea).filter(models.Tarea.id == task_id).first()
    if not tarea_db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    tarea_db.titulo = tarea_actualizada.titulo
    tarea_db.descripcion = tarea_actualizada.descripcion
    tarea_db.completada = tarea_actualizada.completada
    db.commit()
    db.refresh(tarea_db)
    return tarea_db

# DELETE /tareas/{id}
@router.delete("/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(
    tarea_id: int, 
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    # 1. Buscar la tarea en la base de datos
    tarea_query = db.query(models.Tarea).filter(models.Tarea.id == tarea_id)
    tarea = tarea_query.first()

    # 2. Si no existe, error 404
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # 3. Validar que la tarea sea del usuario que tiene el Token
    if tarea.owner_id != int(current_user_id):
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar esta tarea")

    # 4. Proceder a borrar
    tarea_query.delete(synchronize_session=False)
    db.commit()
    
    return {"mensaje": "Tarea eliminada exitosamente"}
@router.get("/mis-tareas", response_model=list[schemas.TareaResponse])
def leer_mis_tareas(
    db: Session = Depends(get_db), 
    current_user_id: str = Depends(get_current_user) # El portero de nuevo
):
    # Usamos el ID que viene del Token para filtrar
    tareas = db.query(models.Tarea).filter(models.Tarea.owner_id == int(current_user_id)).all()
    return tareas
@router.patch("/{tarea_id}", response_model=schemas.TareaResponse)
def marcar_completada(
        tarea_id: int, 
        db: Session = Depends(get_db),
        current_user_id: str = Depends(get_current_user)
    ):
        # 1. Busca la tarea por su ID
        tarea_query = db.query(models.Tarea).filter(models.Tarea.id == tarea_id)
        tarea = tarea_query.first()

        # 2. Si no existe, lanza el error 404
        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        # 3. ¿Qué validación de seguridad pondrías aquí para que nadie más la marque?
        # (Escribe la lógica del dueño aquí)
        if tarea.owner_id != int(current_user_id):
            raise HTTPException(status_code=403, detail="No tienes permiso para borrar esta tarea")
        # 4. Actualiza el campo 'completada'
        tarea_query.update({"completada": not tarea.completada})# O podrías hacer: not tarea.completada
        db.commit()
        db.refresh(tarea)
        
        return tarea