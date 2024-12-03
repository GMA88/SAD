from app.database.database import get_db
from bson.objectid import ObjectId
from datetime import datetime

# Operaciones relacionadas con las ventas
def get_ventas(filter_term=None):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    query = {"producto": {"$regex": filter_term, "$options": "i"}} if filter_term else {}
    return list(db["ventas"].find(query))

def add_venta(nombre_o_codigo_producto, cantidad, vendedor, cliente_nombre, cliente_contacto, cliente_telefono, cliente_email):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")

    producto = db["inventario"].find_one({"$or": [{"codigo": nombre_o_codigo_producto}, {"nombre_producto": nombre_o_codigo_producto}]})
    if not producto:
        raise ValueError("Producto no encontrado.")
    if producto["cantidad_disponible"] < cantidad:
        raise ValueError("Cantidad insuficiente en inventario.")

    total_venta = cantidad * producto["precio_unitario"]

    db["ventas"].insert_one({
        "fecha_venta": datetime.now(),
        "nombre_producto": producto["nombre_producto"],
        "codigo_producto": producto["codigo"],
        "cantidad": cantidad,
        "precio_unitario": producto["precio_unitario"],
        "total_venta": total_venta,
        "vendedor": vendedor,
        "cliente_nombre": cliente_nombre,
        "cliente_contacto": cliente_contacto,
        "cliente_telefono": cliente_telefono,
        "cliente_email": cliente_email
    })

    db["inventario"].update_one({"_id": producto["_id"]}, {"$inc": {"cantidad_disponible": -cantidad}})

    db["finanzas"].insert_one({
        "descripcion": f"Ingreso por venta de {producto['nombre_producto']}",
        "tipo": "Ingreso",
        "monto": total_venta,
        "fecha": datetime.now(),
        "responsable": vendedor
    })
    return True

def delete_venta(venta_id):
    db = get_db()
    if db is None:
        raise ConnectionError("No se pudo conectar a la base de datos.")
    result = db["ventas"].delete_one({"_id": ObjectId(venta_id)})
    return result.deleted_count > 0