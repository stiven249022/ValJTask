from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -----------------------------------------------------------------------------
# 1. LA URL DE CONEXIÓN
# Formato: mysql+driver://usuario:password@servidor:puerto/nombre_bd
# Esto es la dirección exacta donde vive tu base de datos.
# -----------------------------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/fastapi_tareas"

# -----------------------------------------------------------------------------
# 2. EL ENGINE (El Enchufe / La Tubería Principal) 🔌
# - create_engine: Crea la conexión física con MySQL.
# - Es el responsable de mantener el canal abierto. Si MySQL se apaga, 
#   este objeto es el que lanzará el error de conexión.
# -----------------------------------------------------------------------------
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# -----------------------------------------------------------------------------
# 3. SESSIONMAKER (La Fábrica de Cheques / Transacciones) ✍️
# - No usamos el 'engine' directamente para cada pequeña cosa.
# - Usamos esta fábrica para crear una "SessionLocal" por cada petición.
# - autocommit=False: Para que no guarde nada hasta que estemos seguros (firmar el cheque).
# - bind=engine: Le dice que use la tubería que creamos arriba.
# -----------------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -----------------------------------------------------------------------------
# 4. BASE (El ADN / El Molde Maestro) 🧬
# - declarative_base: Crea una clase especial.
# - Más adelante, cuando creemos la tabla 'Tareas', la haremos heredar de esta Base.
# - Esto le permite a Python saber que esa clase NO es código normal,
#   sino una TABLA de base de datos que debe crearse en MySQL.
# -----------------------------------------------------------------------------
Base = declarative_base()  # ... (aquí ya tienes tu engine, SessionLocal, etc.)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()