from fastapi import HTTPException,status
from jose import jwt, JWTError,ExpiredSignatureError
from decouple import config
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import User
from datetime import datetime, timedelta

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/user/token")

# Crea un token
def encode_token(payload: dict):
    expiration = datetime.utcnow() + timedelta(hours=1)  # Expiración de 1 hora
    payload.update({"exp": expiration})
    token = jwt.encode(payload, key=config("KEY"), algorithm="HS256")
    return token


# Solicita un usuario
def get_user(db: Session, token: str):
    try:
        payload = jwt.decode(token, config("KEY"), algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    return user
