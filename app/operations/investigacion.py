from app.database.database import get_db
from bson.objectid import ObjectId

# Obtener investigaciones desde la colección correcta
def get_investigaciones():
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    return list(db["investigacion"].find())  # Asegúrate de que aquí diga "investigacion"

# Añadir investigación a la colección correcta
def add_investigacion(titulo, descripcion, responsable):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    db["investigacion"].insert_one({  # Asegúrate de que aquí diga "investigacion"
        "nombre_proyecto": titulo,
        "descripcion": descripcion,
        "responsable": responsable
    })
    return True

# Eliminar investigación de la colección correcta
def delete_investigacion(investigacion_id):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    result = db["investigacion"].delete_one({"_id": ObjectId(investigacion_id)})  # Asegúrate de que aquí diga "investigacion"
    return result.deleted_count > 0
