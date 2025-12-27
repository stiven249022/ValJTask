# 1. IMPORTAR LAS HERRAMIENTAS
# Agregamos 'BaseModel' para definir la estructura de los datos (el molde)
from fastapi import FastAPI
from pydantic import BaseModel, Field

# 2. CREAR LA APLICACIÓN
app = FastAPI()

# --- TUS RUTAS ANTERIORES (GET) ---

@app.get("/")
def read_root():
    return {"mensaje": "Hola Soy Juan"}

@app.get("/saludo/{nombre}")
def saludar_persona(nombre: str):
    return {"mensaje": f"Hola {nombre}, ¡bienvenido a la API!"}

@app.get("/suma")
def sumar_numeros(n1: int, n2: int):
    resultado = n1 + n2
    return {"operacion": "suma", "resultado": resultado}

# --- LO NUEVO: LA PARTE DEL LOGIN (POST) ---

# Paso A: Definir el "molde" de los datos
class LoginData(BaseModel):
    usuario: str
    password: str = Field(min_length=8)

# Paso B: Crear la ruta POST que usa ese molde
@app.post("/login")
def iniciar_sesion(datos: LoginData):
    return {
        "mensaje": f"Usuario {datos.usuario} logueado exitosamente",
        "nota": "Tu contraseña viajó oculta en el cuerpo de la petición (Body)"
    }