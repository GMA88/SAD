from app.database.database import get_db
from bson.objectid import ObjectId
from datetime import datetime

# Operaciones relacionadas con el inventario
def get_inventario(filter_term=None):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    query = {"nombre_producto": {"$regex": filter_term, "$options": "i"}} if filter_term else {}
    return list(db["inventario"].find(query))

def add_inventario(nombre, cantidad, categoria, precio_unitario):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    db["inventario"].insert_one({
        "nombre_producto": nombre,
        "cantidad_disponible": cantidad,
        "categoria": categoria,
        "precio_unitario": precio_unitario,
        "fecha_agregado": datetime.now()
    })
    return True

def delete_inventario(inventario_id):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    result = db["inventario"].delete_one({"_id": ObjectId(inventario_id)})
    return result.deleted_count > 0