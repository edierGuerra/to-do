from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from decouple import config

# url de base de datos
URL_DB = f"postgresql://{config('MySQL_USER')}:{config('MySQL_PASSWORD')}@{config('MySQL_HOST')}:5432/{config('MySQL_DB')}"

# Motor de base de datos 
engine = create_engine(url=URL_DB,echo=True)

# Fabrica de sesiones
SessionLocal = sessionmaker(bind = engine)

# Dependencia para fastapi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

