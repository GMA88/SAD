from app.database.database import get_db
import hashlib

# Manejo de usuarios y roles
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    if db.users.find_one({"username": username}):
        return False  # Usuario ya registrado
    db.requests.insert_one({
        "username": username,
        "password": hash_password(password),
        "role": None  # El rol se asigna posteriormente
    })
    return True

def login_user(username, password):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    user = db.users.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        return user["role"]
    return None

def approve_user(username, role):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    request = db.requests.find_one({"username": username})
    if request:
        db.users.insert_one({
            "username": request["username"],
            "password": request["password"],
            "role": role
        })
        db.requests.delete_one({"username": username})
        return True
    return False

def get_pending_requests():
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    return list(db.requests.find())
