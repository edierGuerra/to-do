from pydantic import BaseModel,EmailStr

class UserModel(BaseModel):
    name:str 
    username:str
    email:EmailStr

    class Config:
        orm_mode = True

class CreateUserResponse(BaseModel):
    name:str
    username:str
    email:EmailStr
