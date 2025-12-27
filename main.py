from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles # <--- No olvides importar esto
from routers import usuarios, tareas
import models
from database import engine
from fastapi.responses import FileResponse
# 1. Crear las tablas (si no existen)
models.Base.metadata.create_all(bind=engine)

# 2. CREAR LA APP (Esto debe ir ANTES de usar 'app')
app = FastAPI()

# 3. MONTAR LA CARPETA STATIC (Ahora sí, porque 'app' ya existe)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 4. Incluir los routers
app.include_router(usuarios.router)
app.include_router(tareas.router) 

# Ruta de prueba para verificar que el servidor vive
@app.get("/")
def home():
    return FileResponse("static/index.html")