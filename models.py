from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True) # unique=True: No pueden haber dos emails iguales
    hashed_password = Column(String(255)) # Aquí guardaremos la contraseña encriptada
    is_active = Column(Boolean, default=True)
    rol = Column(String(20), default="estudiante")

    # RELACIÓN: Un usuario tiene muchas tareas
    # "Tarea" es el nombre de la clase de abajo
    # back_populates crea un vínculo de ida y vuelta
    tareas = relationship("Tarea", back_populates="propietario")


class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100))
    descripcion = Column(String(255))
    completada = Column(Boolean, default=False)
    
    # CLAVE FORÁNEA (Foreign Key): Aquí guardamos el ID del dueño
    # usuarios.id hace referencia a la tabla 'usuarios' columna 'id'
    owner_id = Column(Integer, ForeignKey("usuarios.id"))

    # RELACIÓN INVERSA: Para saber quién es el dueño desde la tarea
    propietario = relationship("Usuario", back_populates="tareas")