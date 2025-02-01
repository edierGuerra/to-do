from fastapi import FastAPI
from routes.user_routes import route as user_route
from routes.task_routes import router as task_route
from database import Base, engine

# Instancia de la api
app = FastAPI(
    title="FastAPI ToDo",
    description="Api para la gestión de tareas y validación de usuarios.",
    version="0.0.1",
)

# Ruta inicial
@app.get("/")
def root():
    return {"message":"Bienvenido a tu gestor de tareas"}
if __name__ == "__main__":
    # Iniciar la base de datos
    Base.metadata.create_all(engine)
app.include_router(router= user_route)
app.include_router(router= task_route)