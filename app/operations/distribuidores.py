from app.database.database import get_db
from bson.objectid import ObjectId

# Obtener distribuidores
def get_distribuidores():
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    return list(db["distribuidores"].find())

# Añadir distribuidor
def add_distribuidor(nombre, contacto, telefono):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    db["distribuidores"].insert_one({
        "nombre": nombre,
        "contacto": contacto,
        "telefono": telefono
    })
    return True

# Eliminar distribuidor
def delete_distribuidor(distribuidor_id):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    result = db["distribuidores"].delete_one({"_id": ObjectId(distribuidor_id)})
    return result.deleted_count > 0
