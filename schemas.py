from pydantic import BaseModel,EmailStr

class UserModel(BaseModel):
    name:str 
    username:str
    email:EmailStr

    class Config:
        from_attributes = True

class UserModelPassword(UserModel):
    password:str