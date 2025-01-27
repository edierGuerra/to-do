# TODO: Mejorar la validación de usuarios y agregar expiración al token.
from fastapi import Depends,HTTPException,status
from jose import jwt, JWTError,ExpiredSignatureError
from decouple import config
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import User
from utils.hashing import validate_password
from datetime import datetime, timedelta

oauth2_schema = OAuth2PasswordBearer(tokenUrl="user/token")

# Valida que el usuario exista
def validate_user(db:Session,username:str,password:str):
    user_valide = db.query(User).filter(User.username == username).first()
    if not user_valide:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if not validate_password():
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password")
    return True

# Crea un token

def encode_token(payload: dict):
    expiration = datetime.utcnow() + timedelta(hours=1)  # Expiración de 1 hora
    payload.update({"exp": expiration})
    token = jwt.encode(payload, key=config("KEY"), algorithm="HS256")
    return token



def get_user(db: Session, token: str):
    try:
        payload = jwt.decode(token, config("KEY"), algorithms=["HS256"])
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user
