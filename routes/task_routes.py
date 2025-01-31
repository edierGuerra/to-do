from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from schemas import TaskModel,TaskModelCreate,TaskModelUpdate
from auth import get_user, oauth2_schema
from database import get_db
from CRUD import create_task,delete_task,update_task

router = APIRouter(prefix="/api/v1/task", tags=["tasks"])

@router.get(
    "/",
    summary="Obtener tareas",
    description="Retorna todas las tareas de un usuario autenticado.")
def get_tasks(db:Session = Depends(get_db),token:str = Depends(oauth2_schema)):
    """
    Obtiene todas las tareas asociadas al usuario autenticado.

    - **token**: Token de autenticación del usuario.
    - **db**: Sesión de base de datos.

    **Retorna:**  
    Una lista de tareas del usuario autenticado.
    """
    user = get_user(db,token)
    tasks_of_user = user.tasks
    return tasks_of_user

@router.post(
    "/",
    summary="Crear una tarea",
    description="Crea una nueva tarea para el usuario autenticado.",
    response_model=TaskModel
)
def create_tasks(form_data_task: TaskModelCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    """
    Crea una nueva tarea para el usuario autenticado.

    - **token**: Token de autenticación del usuario.
    - **db**: Sesión de base de datos.
    - **form_data_task**: Datos de la tarea a crear (título y descripción).
    
    **Retorna:**  
    La información de la tarea recién creada.
    """
    user = get_user(db,token)
    task = create_task(db,id_user=user.id, title_task=form_data_task.title,description_task=form_data_task.description)
    task_data = {
        "title":task.title,
        "description":task.description,
        "id_task":task.id,
        "id_user":task.id_user
        }
    return task_data


@router.put(
    "/{id_task}",
    summary="Actualizar una tarea",
    description="Actualiza una tarea existente del usuario autenticado.",
    response_model=TaskModel
)
def update_tasks(task_data: TaskModelUpdate, id_task: int, db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    """
    Actualiza una tarea existente del usuario autenticado.

    - **token**: Token de autenticación del usuario.
    - **db**: Sesión de base de datos.
    - **id_task**: ID de la tarea a actualizar.
    - **task_data**: Datos actualizados de la tarea (título y descripción).
    
    **Retorna:**  
    La información de la tarea actualizada.
    """
    user = get_user(db, token)
    task = update_task(db, user.id, id_task, task_data.title, task_data.description)
    
    task_update = {
        "title": task.title,
        "description": task.description,
        "id_task": task.id,
        "id_user": task.id_user
    }
    return task_update


@router.delete(
    "/",
    summary="Eliminar una tarea",
    description="Elimina una tarea existente del usuario autenticado."
)
def delete_tasks(id_task: int, db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    """
    Elimina una tarea existente del usuario autenticado.

    - **token**: Token de autenticación del usuario.
    - **db**: Sesión de base de datos.
    - **id_task**: ID de la tarea a eliminar.
    
    **Retorna:**  
    Un mensaje de confirmación de eliminación.
    """
    user = get_user(db, token)
    return delete_task(db, user.id, id_task)