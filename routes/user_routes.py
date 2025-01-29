from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from utils.hashing import hash_password, validate_password
from schemas import UserModel, UserModelPassword
from models import User
from database import get_db
from auth import encode_token, get_user

route = APIRouter(prefix="/api/v1/user")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/user/token")

# Crear un nuevo usuario
@route.post(
    "/create",
    response_model=UserModel,
    tags=["user"],
    summary="Crear usuario",
    description="Registra un nuevo usuario en la base de datos."
)
async def create_user(
    user_data: UserModelPassword,
    db: Annotated[Session, Depends(get_db)]
):
    """
    ## Crear usuario
    Permite registrar un nuevo usuario en la base de datos.

    ### Argumentos:
    - **user_data**: Información del usuario en formato `UserModelPassword`, que incluye:
        - `name` (str): Nombre completo del usuario.
        - `username` (str): Nombre único del usuario.
        - `email` (str): Dirección de correo electrónico única.
        - `password` (str): Contraseña del usuario.

    ### Respuesta:
    Retorna un objeto de tipo `UserModel` con la información del usuario registrado:
        - `id` (int): ID único del usuario.
        - `name` (str): Nombre del usuario.
        - `username` (str): Nombre de usuario.
        - `email` (str): Correo electrónico del usuario.

    ### Errores:
    - **400 Bad Request**: Si el correo electrónico ya está registrado.
    """
    user_password_hashed = hash_password(user_data.password)
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe."
        )
    user = User(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email
    )
    user.password = user_password_hashed
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Iniciar sesión y generar un token
@route.post(
    "/token",
    tags=["user"],
    summary="Iniciar sesión",
    description="Valida las credenciales de un usuario y genera un token de acceso."
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    ## Iniciar sesión
    Valida el nombre de usuario y contraseña de un usuario. Si las credenciales son válidas, genera un token JWT.

    ### Argumentos:
    - **form_data**: Datos enviados como `form-data`, que incluyen:
        - `username` (str): Nombre de usuario.
        - `password` (str): Contraseña del usuario.

    ### Respuesta:
    Retorna un token de acceso (`JWT`) si las credenciales son correctas:
        - `access_token` (str): Token de acceso generado.
        - `token_type` (str): Tipo de token (siempre "bearer").

    ### Errores:
    - **401 Unauthorized**: Si las credenciales son inválidas.
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if user and validate_password(form_data.password, user.password):
        token = encode_token(payload={"sub": form_data.username})
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas."
    )


# Obtener el perfil del usuario autenticado
@route.get(
    "/profile",
    response_model=UserModel,
    tags=["user"],
    summary="Obtener perfil del usuario",
    description="Retorna la información del perfil del usuario autenticado basado en el token."
)
async def profile(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema)
):
    """
    ## Obtener perfil del usuario
    Permite al usuario autenticado obtener los datos de su perfil.

    ### Encabezados requeridos:
    - **Authorization**: Bearer `<token>` (El token generado al iniciar sesión).

    ### Respuesta:
    Retorna un objeto de tipo `UserModel` con la información del usuario autenticado:
        - `id` (int): ID único del usuario.
        - `name` (str): Nombre completo del usuario.
        - `username` (str): Nombre único del usuario.
        - `email` (str): Correo electrónico del usuario.

    ### Errores:
    - **401 Unauthorized**: Si el token es inválido o no fue proporcionado.
    """
    user = get_user(db, token)
    return user
