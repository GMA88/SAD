from app.database.database import get_db
from bson.objectid import ObjectId

# Operaciones relacionadas con los proveedores
def get_proveedores(filter_term=None):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    query = {"nombre": {"$regex": filter_term, "$options": "i"}} if filter_term else {}
    return list(db["proveedores"].find(query))

def add_proveedor(nombre, telefono, direccion):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    db["proveedores"].insert_one({
        "nombre": nombre,
        "telefono": telefono,
        "direccion": direccion
    })
    return True

def delete_proveedor(proveedor_id):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    result = db["proveedores"].delete_one({"_id": ObjectId(proveedor_id)})
    return result.deleted_count > 0


# Archivo: operations/empleados.py
from app.database.database import get_db
from bson.objectid import ObjectId
from datetime import datetime

# Operaciones relacionadas con los empleados
def get_empleados(filter_term=None):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    query = {"nombre": {"$regex": filter_term, "$options": "i"}} if filter_term else {}
    return list(db["empleados"].find(query))

def add_empleado(nombre, puesto, salario, departamento):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    db["empleados"].insert_one({
        "nombre": nombre,
        "puesto": puesto,
        "salario": salario,
        "departamento": departamento,
        "fecha_contratacion": datetime.now()
    })
    return True

def delete_empleado(empleado_id):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    result = db["empleados"].delete_one({"_id": ObjectId(empleado_id)})
    return result.deleted_count > 0