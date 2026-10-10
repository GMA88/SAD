import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api.main import app
from api.database import Base, get_db

# Base de datos en memoria aislada para las pruebas automáticas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_root_and_status():
    response = client.get("/")
    assert response.status_code == 200
    assert "SAD" in response.json()["message"]

    status_resp = client.get("/status")
    assert status_resp.status_code == 200
    assert "correctamente" in status_resp.json()["status"]

def test_registro_usuario_y_login():
    user_payload = {
        "username": "test_user_admin",
        "password": "secure_password_123",
        "role": "Administrador"
    }
    # 1. Registro de usuario
    resp = client.post("/usuarios/registro", json=user_payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "test_user_admin"
    assert data["role"] == "Administrador"
    assert "password" not in data

    # 2. Login con credenciales válidas
    login_resp = client.post("/usuarios/login", json=user_payload)
    assert login_resp.status_code == 200
    assert login_resp.json()["message"] == "Login exitoso"

    # 3. Login rechazado con contraseña incorrecta
    bad_login = client.post("/usuarios/login", json={
        "username": "test_user_admin",
        "password": "wrong_password"
    })
    assert bad_login.status_code == 401

def test_inventario_crud():
    prod_payload = {
        "codigo": "TEST-SKU-001",
        "nombre_producto": "Teclado para Pruebas",
        "cantidad_disponible": 10,
        "precio_unitario": 45.50
    }
    # 1. Crear producto
    resp = client.post("/inventario/", json=prod_payload)
    assert resp.status_code == 201
    created = resp.json()
    assert created["codigo"] == "TEST-SKU-001"
    assert created["cantidad_disponible"] == 10
    prod_id = created["id"]

    # 2. Rechazar código SKU duplicado
    dup_resp = client.post("/inventario/", json=prod_payload)
    assert dup_resp.status_code == 400

    # 3. Listar productos
    list_resp = client.get("/inventario/")
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert any(p["id"] == prod_id for p in items)

def test_transaccion_venta_y_descuento_stock():
    # 1. Crear producto con 15 unidades a $100.0 c/u
    prod_resp = client.post("/inventario/", json={
        "codigo": "TEST-VENTA-002",
        "nombre_producto": "Monitor de Pruebas",
        "cantidad_disponible": 15,
        "precio_unitario": 100.0
    })
    assert prod_resp.status_code == 201
    prod_id = prod_resp.json()["id"]

    # 2. Registrar venta de 5 unidades
    venta_payload = {
        "producto_id": prod_id,
        "cantidad": 5,
        "vendedor": "Andrea Varela",
        "cliente_nombre": "Empresa Cliente Test",
        "cliente_contacto": "Empresa Cliente Test",
        "cliente_telefono": "+52 55 0000 0000",
        "cliente_email": "cliente@test.com"
    }
    venta_resp = client.post("/ventas/", json=venta_payload)
    assert venta_resp.status_code == 201
    venta_data = venta_resp.json()
    assert venta_data["total_venta"] == 500.0
    assert venta_data["cantidad"] == 5

    # 3. Validar consistencia transaccional ACID: el stock disponible debe ser exactamente 10 (15 - 5)
    check_prod = client.get(f"/inventario/{prod_id}")
    assert check_prod.status_code == 200
    assert check_prod.json()["cantidad_disponible"] == 10

def test_venta_rechazada_por_stock_insuficiente():
    # Intentar vender 50 unidades cuando solo quedan 10
    prods = client.get("/inventario/").json()
    prod = next(p for p in prods if p["codigo"] == "TEST-VENTA-002")

    venta_excesiva = {
        "producto_id": prod["id"],
        "cantidad": 50,
        "vendedor": "Andrea Varela",
        "cliente_nombre": "Empresa Cliente",
        "cliente_contacto": "Empresa Cliente",
        "cliente_telefono": "+52 55 0000 0000",
        "cliente_email": "cliente@test.com"
    }
    resp = client.post("/ventas/", json=venta_excesiva)
    assert resp.status_code == 400
    assert "Stock insuficiente" in resp.json()["detail"]

def test_reporte_ai():
    # Validar que el endpoint analítico devuelva la estructura de Business Intelligence
    resp = client.get("/ai/reporte")
    assert resp.status_code == 200
    data = resp.json()
    assert "resumen_ejecutivo" in data
    assert "alertas_criticas" in data
    assert "recomendaciones" in data
    assert "proyeccion_crecimiento" in data

def test_ai_configuracion_multi_proveedor():
    # 1. Obtener lista de proveedores y guardar estado previo
    resp = client.get("/ai/config")
    assert resp.status_code == 200
    prev_config = resp.json()["current"]
    providers = resp.json()["providers"]
    assert "local_engine" in providers
    assert "cloud_standard" in providers
    assert "cloud_custom" in providers
    assert "simulated" in providers

    try:
        # 2. Configurar Servicio Cloud Estándar
        update_resp = client.post("/ai/config", json={
            "provider": "cloud_standard",
            "api_key": "sk-test12345678",
            "model": "standard-model-v1"
        })
        assert update_resp.status_code == 200
        assert update_resp.json()["provider"] == "cloud_standard"
    finally:
        # 3. Restaurar estado previo
        client.post("/ai/config", json={
            "provider": prev_config.get("provider", "local_engine"),
            "model": prev_config.get("model", ""),
            "base_url": prev_config.get("base_url", "")
        })


def test_ai_chat_asistente():
    # Validar que el Asistente Virtual interactúe respondiendo consultas sobre el ERP
    chat_payload = {
        "messages": [
            {"role": "user", "content": "¿Cuáles son los productos con alerta de stock bajo?"}
        ],
        "lang": "es"
    }
    resp = client.post("/ai/chat", json=chat_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "reply" in data
    assert len(data["reply"]) > 10

def test_ai_chat_asistente_english():
    # Validar que el endpoint acepte parámetro de idioma en inglés
    chat_payload = {
        "messages": [
            {"role": "user", "content": "What are the products with critical low stock today?"}
        ],
        "lang": "en"
    }
    resp = client.post("/ai/chat", json=chat_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "reply" in data
    assert len(data["reply"]) > 10

def test_reporte_ai_english():
    # Validar generación de reporte ejecutivo en inglés
    resp = client.get("/ai/reporte?lang=en")
    assert resp.status_code == 200
    data = resp.json()
    assert "resumen_ejecutivo" in data
    assert "alertas_criticas" in data
    assert "recomendaciones" in data


