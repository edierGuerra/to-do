from fastapi import Depends,HTTPException
from jose import jwt, JWTError
from decouple import config
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import User
from utils.hashing import validate_password

oauth2_schema = OAuth2PasswordBearer(tokenUrl="user/token")

# Valida que el usuario exista
def validate_user(db:Session,username:str,password:str):
    user_valide = db.query(User).filter(User.username == username).first()
    if user_valide:
        password = validate_password(password, user_valide.password)
        if password:
            return True
        return {"message":"Invalide password"}
    return {"message":"Invalide user"}

# Crea un token
def encode_token(payload:dict):
    token = jwt.encode(payload,key=config("KEY"),algorithm="HS256")
    return token

def get_user(db:Session, token:str):
        try:
            # Decodificar el token, pasando la clave secreta para verificarlo
            payload = jwt.decode(token, config("KEY"), algorithms=["HS256"])
            username: str = payload.get("username")  
            if username is None:
                raise HTTPException(status_code=401, detail="Token inválido")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")

        # Buscar al usuario en la base de datos
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return user