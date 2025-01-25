from pydantic import BaseModel,EmailStr

class UserModel(BaseModel):
    name:str 
    username:str
    email:EmailStr
    password:str

    class Config:
        from_attributes = True

class CreateUserResponse(BaseModel):
    name:str
    username:str
    email:EmailStr
    password:str

