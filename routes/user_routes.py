from fastapi import Depends,APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from utils.hashing import hash_password
from schemas import UserModel,CreateUserResponse
from models import User
from database import get_db

route = APIRouter(prefix="/user")


@route.post("/create",response_model=UserModel)
async def user(user_data:CreateUserResponse,db:Annotated[Session, Depends(get_db)]):
    user_password_hashed = hash_password(user_data.password) # Encripta la contraseña
    user = User(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email
    )
    user.password = user_password_hashed # Le asigna la contraseña encriptada al usuario para guardarla en la bd
    db.add(user)
    db.commit()
    db.refresh(user)
    return user