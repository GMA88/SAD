import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

client = None

def get_db():
    global client
    if not client:
        try:
            # Usa variables de entorno para las credenciales de la base de datos
            mongo_uri = os.getenv("MONGODB_URI", "")
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            # Prueba de conexión
            client.admin.command('ping')
            print("Conexión exitosa a MongoDB Atlas")
        except ConnectionFailure as e:
            print(f"Error al conectar a MongoDB: {e}")
            return None
    return client["empresa"]