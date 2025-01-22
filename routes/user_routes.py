from fastapi import Depends,APIRouter
from schemas import UserModel,CreateUserResponse
from typing import Annotated
from database import get_db
from sqlalchemy.orm import Session
from models import User

route = APIRouter(prefix="/user")


@route.post("/create",response_model=UserModel)
async def user(user_data:CreateUserResponse,db:Annotated[Session, Depends(get_db)]):
    user = User(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user