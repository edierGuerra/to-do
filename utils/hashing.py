from bcrypt import hashpw, checkpw, gensalt

# Encripta la contraseña
def hash_password(password:str):
    hashed_password = hashpw(password=password.encode("utf-8"), salt = gensalt())
    return hashed_password

# Valida la contraseña
def validate_password(password:str,hashed_password:bytes):
    valid_password = checkpw(password=password.encode("utf-8"),hashed_password=hashed_password)
    return valid_password

