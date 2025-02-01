from bcrypt import hashpw, checkpw, gensalt

# Encripta la contraseña
def hash_password(password:str):
    hashed_password = hashpw(password=password.encode("utf-8"), salt = gensalt())
    return hashed_password.decode("utf-8")

# Valida la contraseña
def validate_password(password:str,hashed_password:str):
    return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

