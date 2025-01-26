from fastapi import Depends,APIRouter,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from utils.hashing import hash_password
from schemas import UserModel,CreateUserResponse
from models import User
from database import get_db
from auth import  encode_token, get_user, validate_user

route = APIRouter(prefix="/user")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="user/token")

# Registra un usuario
@route.post("/create",response_model=UserModel)
async def create_user(user_data:CreateUserResponse,db:Annotated[Session, Depends(get_db)]):
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

@route.post("/token")
async def login(form_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = validate_user(db,username=form_data.username,password=form_data.password)
    if user == True:
        token = encode_token(payload={"username":form_data.username})
        return {
            "access_token":token,
            "token_type": "bearer"
            }
    else:
        raise HTTPException(status_code=401,detail=user["message"])

@route.get("/api/v1/profile" , response_model=UserModel)
async def profile(db:Session = Depends(get_db),token:str = Depends(oauth2_schema)):
    user = get_user(db,token)
    return user