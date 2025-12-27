from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. MODELO DE DATOS
# Definimos qué forma tiene una "Tarea"
class Tarea(BaseModel):
    titulo: str
    descripcion: str
    completada: bool = False # Por defecto no está terminada

# 2. BASE DE DATOS SIMULADA
# Una lista vacía en la memoria
db_tareas = []

# 3. RUTA PARA VER LAS TAREAS (READ)
@app.get("/tareas")
def obtener_todas_las_tareas():
    return db_tareas

# 4. RUTA PARA CREAR TAREAS (CREATE)
@app.post("/tareas")
def crear_tarea(nueva_tarea: Tarea):
    # Agregamos la tarea que llega a nuestra lista
    db_tareas.append(nueva_tarea)
    return {"mensaje": "Tarea creada con éxito", "tarea": nueva_tarea}

# Prueba de memoria del servidor

# 5. RUTA PARA ACTUALIZAR (UPDATE)
# Usamos el método PUT
# {task_id} será el número de la tarea en la lista (0, 1, 2...)
@app.put("/tareas/{task_id}")
def actualizar_tarea(task_id: int, tarea_actualizada: Tarea):
    # Verificamos si el ID existe en la lista
    if task_id < 0 or task_id >= len(db_tareas):
        return {"error": "Tarea no encontrada, revisa el ID"}
    
    # Reemplazamos la tarea vieja por la nueva
    db_tareas[task_id] = tarea_actualizada
    return {"mensaje": "Tarea actualizada", "tarea_nueva": db_tareas[task_id]}

# 6. RUTA PARA BORRAR (DELETE)
@app.delete("/tareas/{task_id}")
def eliminar_tarea(task_id: int):
    # Validación (Perfecta, tal como la escribiste)
    if task_id < 0 or task_id >= len(db_tareas):
        return {"error": "Tarea no encontrada, revisa el ID"}
    
    # Acción: Sacamos el elemento de la lista
    # Nota: pop() devuelve el elemento que acaba de borrar, lo guardamos para mostrarlo
    tarea_eliminada = db_tareas.pop(task_id)
    
    # Respuesta
    return {"mensaje": "Eliminada con éxito", "tarea": tarea_eliminada}