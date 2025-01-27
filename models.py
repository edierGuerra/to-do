from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import String, Integer, ForeignKey

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
    password:Mapped[str] = mapped_column(String(250),nullable=False)
    tasks:Mapped[list["Task"]] = relationship("Task", back_populates="user",cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, username={self.username})>"

# Clase que recibe los datos de las tareas
class Task(Base):
    __tablename__ = "tasks"
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    title:Mapped[str] = mapped_column(String(50),unique=False,nullable=False)
    description:Mapped[str] = mapped_column(String(250),unique=False,nullable=False)
    id_user:Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    user:Mapped["User"] = relationship("User",back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, description={self.description}), autor={self.id_user}>"