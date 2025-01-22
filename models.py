from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

# Clase base que heredan las demás 
class Base(DeclarativeBase):
    pass

# Clase que recibe los datos del usuario
class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(String(50),nullable=False)
    username:Mapped[str] = mapped_column(String(100),nullable=False,unique=True)
    email:Mapped[str] = mapped_column(String(50),nullable=False,unique=True)
