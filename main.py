from fastapi import FastAPI

# Instancia de la api
app = FastAPI(
    title="FastAPI ToDo",
    description="Api para la gestión de tareas y validación de usuarios.",
    version="0.0.1",
)

# Ruta inicial
@app.get("/")
def root():
    return "Bienvenido a tu gestor de tareas"