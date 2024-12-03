from app.database.database import get_db
from bson.objectid import ObjectId
from datetime import datetime

# Obtener empleados
def get_empleados():
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    return list(db["rrhh"].find())  # Cambiar "empleados" por "rrhh"

# Añadir empleado
def add_empleado(nombre, puesto, departamento, salario, fecha_contratacion, email, telefono):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    db["rrhh"].insert_one({  # Cambiar "empleados" por "rrhh"
        "nombre": nombre,
        "puesto": puesto,
        "departamento": departamento,
        "salario": salario,
        "fecha_contratacion": fecha_contratacion,
        "email": email,
        "telefono": telefono
    })
    return True

# Eliminar empleado
def delete_empleado(empleado_id):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    result = db["rrhh"].delete_one({"_id": ObjectId(empleado_id)})  # Cambiar "empleados" por "rrhh"
    return result.deleted_count > 0