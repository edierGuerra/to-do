from sqlalchemy.orm import Session
from fastapi import HTTPException, status 
from database import SessionLocal
from models import Task,User

# Registra tareas
def create_task(db:Session, id_user:int,title_task:str,description_task:str):
    user = db.get(User,id_user)
    if not user: 
        raise ValueError(f"El usuario con id {id_user} no existe")
    task = Task(id_user = id_user, title = title_task, description = description_task)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# Visualiza tareas de usuario 
def get_user_tasks(db:Session, user_id:int):
    user_tasks = db.query(Task).filter(Task.id_user == user_id).all()
    if not user_tasks: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= "Not task for this user")
    return user_tasks



# Actualiza datos de una tarea
def update_task(db:Session, id_user:int, id_task:int, new_title:str = None, new_description:str = None):
    task = db.query(Task).filter(Task.id_user == id_user, Task.id == id_task).first()

    if not task: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= "Task not found")
    
    if new_title: 
        task.title = new_title
    if new_description:
        task.description = new_description
    
    db.commit()
    db.refresh(task)

    return task

# Elimina una tarea
def delete_task(db:Session,id_user:int,id_task:int):
    task_to_delete = db.query(Task).filter(Task.id_user == id_user, Task.id == id_task).first()
    if not task_to_delete: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= "Task not found")

    db.delete(task_to_delete)
    db.commit()
    if db.query(Task).filter(Task.id_user == id_user, Task.id == id_task).first():
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,detail= "Fail to delete task")
    
    return {"message":"Task successfully delete"}



