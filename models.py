from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    rol = Column(String(50), default="estudiante")

    # RELACIÓN: Un usuario tiene muchas tareas
    # OJO AQUÍ: back_populates apunta a "owner" (que está en la clase Tarea)
    tareas = relationship("Tarea", back_populates="owner") 

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), index=True)
    descripcion = Column(String(255))
    
    # Nuevos campos de fecha
    fecha_inicio = Column(DateTime, default=datetime.now)
    fecha_entrega = Column(DateTime, nullable=True)

    # Clave foránea
    owner_id = Column(Integer, ForeignKey("usuarios.id"))

    # RELACIÓN: Una tarea pertenece a un usuario
    # OJO AQUÍ: La variable se llama "owner" y back_populates apunta a "tareas"
    owner = relationship("Usuario", back_populates="tareas")