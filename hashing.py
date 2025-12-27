from passlib.context import CryptContext

# VARIABLE NUEVA: pwd_context
# -----------------------------
# Es el objeto de configuración.
# schemes=["bcrypt"]: Le decimos "Usa el algoritmo bcrypt". 
# bcrypt es el estándar de oro actual: es lento a propósito para que los hackers 
# no puedan adivinar contraseñas rápido.
# deprecated="auto": Si en el futuro bcrypt se vuelve obsoleto, Passlib lo manejará.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    # CONCEPTO: @staticmethod
    # Significa que no necesito crear una instancia (objeto) de la clase Hash para usar esto.
    # Puedo llamar directamente Hash.bcrypt() sin hacer h = Hash().
    @staticmethod
    def bcrypt(password: str):
        # Aquí ocurre la magia. 
        # Entra "12345" -> Sale "$2b$12$EixZaYVK1fsdf..."
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password, hashed_password):
        # Esta función la usaremos en el LOGIN.
        # Compara la contraseña que escribe el usuario (plain) 
        # contra el garabato que está en la base de datos (hashed).
        return pwd_context.verify(plain_password, hashed_password) 