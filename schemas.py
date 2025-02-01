from pydantic import BaseModel,EmailStr
from typing import Optional

class UserModel(BaseModel):
    name:str 
    username:str
    email:EmailStr

    class Config:
        from_attributes = True

class UserModelPassword(UserModel):
    password:str

class TaskModelCreate(BaseModel):
    title:str
    description:str

class TaskModelUpdate(BaseModel):
    title:Optional[str] = None
    description:Optional[str] = None
class TaskModel(TaskModelCreate):
    id_task:int
    id_user:int

    class Config:
        from_attributes = True
