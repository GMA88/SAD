from app.database.database import get_db
from bson.objectid import ObjectId
from datetime import datetime

# Operaciones relacionadas con las finanzas
def get_finanzas(filter_term=None):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    query = {"descripcion": {"$regex": filter_term, "$options": "i"}} if filter_term else {}
    return list(db["finanzas"].find(query))

def add_finanza(descripcion, tipo, monto, responsable):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    db["finanzas"].insert_one({
        "descripcion": descripcion,
        "tipo": tipo,
        "monto": monto,
        "responsable": responsable,
        "fecha": datetime.now()
    })
    return True

def delete_finanza(finanza_id):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    result = db["finanzas"].delete_one({"_id": ObjectId(finanza_id)})
    return result.deleted_count > 0