# ⚡ SAD ERP - Sistema de Administración y Analítica Empresarial

[![CI Pipeline](https://github.com/GMA88/SAD/actions/workflows/ci.yml/badge.svg)](https://github.com/GMA88/SAD/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Pytest](https://img.shields.io/badge/Tests-Pytest%20Passing-10b981?logo=pytest&logoColor=white)

Sistema Integral de Gestión Empresarial (ERP) modernizado a una arquitectura desacoplada de alto rendimiento: **Backend RESTful con FastAPI + SQLAlchemy (SQLite/PostgreSQL)** y **Frontend moderno con React + Vite**, complementado con **Dashboard de Inteligencia de Negocios (BI)** con Recharts y diagnósticos estratégicos asistidos por **Inteligencia Artificial**.


> **Nota:** El proyecto conserva su versión original de escritorio en Python + PyQt5 y MongoDB, sirviendo como caso de estudio de modernización tecnológica hacia la web y análisis de datos en tiempo real.

---

## 🚀 Características Principales

### 📊 Dashboard de Inteligencia de Negocios (BI)
- **KPIs en tiempo real**: Ingresos totales, volumen de órdenes registradas, ticket promedio por transacción y monitoreo de stock crítico.
- **Visualización de Datos**: Curvas de tendencias de facturación histórica y distribución de inventario utilizando componentes interactivos de `Recharts`.
- **Diagnóstico AI**: Módulo analítico integrado (`/ai/reporte`) que genera resúmenes ejecutivos, detección de riesgos de desabasto y recomendaciones de crecimiento de negocio.

### 📦 Gestión de Inventario (CRUD)
- Catálogo de productos con código SKU, precio unitario y control de stock disponible.
- Sistema de alertas automáticas para inventario bajo (< 5 unidades) o agotado.
- Búsqueda dinámica en tiempo real por nombre de producto o código.
- Registro y actualización mediante endpoints RESTful.

### 🛒 Punto de Venta (POS) y Registro de Ventas
- Registro de transacciones con validación de inventario en tiempo real.
- Operaciones transaccionales seguras (ACID) con SQLAlchemy: deducción automática de stock y registro en libro de finanzas al confirmar una venta.
- Historial detallado con fecha, datos del cliente y vendedor responsable.

### 👥 Administración de Usuarios y Seguridad
- Gestión de usuarios y control de acceso basado en roles (*Administrador*, *Gerente*, *Vendedor*).
- Encriptación segura de contraseñas con SHA-256.

---

## 🛠 Stack Tecnológico

| Capa | Tecnologías |
|---|---|
| **Frontend** | React 18, Vite, Lucide Icons, Recharts, CSS Glassmorphism |
| **Backend** | Python 3.12, FastAPI, Pydantic v2, Uvicorn, SQLAlchemy |
| **Base de Datos** | SQLite (preparado para migración a PostgreSQL) |
| **Desktop Legacy** | Python 3.x, PyQt5, MongoDB (`pymongo`) |

---

## 📁 Estructura del Repositorio

```text
SAD/
├── api/                     # Backend FastAPI
│   ├── main.py              # Punto de entrada de la API y rutas raíz / AI / Seed
│   ├── database.py          # Configuración del motor SQLAlchemy
│   ├── models.py            # Modelos ORM (Usuarios, Inventario, Ventas, Finanzas)
│   ├── schemas.py           # Validaciones de entrada y salida con Pydantic
│   └── routers/             # Módulos de rutas desacopladas
│       ├── inventario.py    # CRUD de productos y stock
│       ├── ventas.py        # Transacciones de venta y deducción de existencias
│       └── usuarios.py      # Autenticación y registro de personal
├── frontend/                # Frontend Web SPA
│   ├── src/
│   │   ├── App.jsx          # Aplicación principal, navegación y modales
│   │   ├── index.css        # Sistema de diseño Glassmorphism y temas oscuros
│   │   └── main.jsx         # Punto de montaje React
│   ├── package.json         # Dependencias (recharts, lucide-react, vite)
│   └── vite.config.js       # Configuración del bundler
├── app/                     # (Legacy) Módulos de escritorio
├── gui/                     # (Legacy) Ventanas PyQt
├── requirements.txt         # Dependencias de Python
└── README.md
```

---

## ⚡ Guía de Instalación y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/GMA88/SAD.git
cd SAD
```

### 2. Iniciar el Backend (FastAPI)
```bash
# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate       # En Windows
# source venv/bin/activate  # En Linux/macOS

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor Uvicorn
uvicorn api.main:app --reload --port 8000
```
> La documentación interactiva de Swagger UI estará disponible en: **http://127.0.0.1:8000/docs**

### 3. Iniciar el Frontend (React + Vite)
En una nueva terminal:
```bash
cd frontend
npm install
npm run dev
```
> Abre tu navegador en: **http://localhost:5173**

---

## 👥 Autora

**Andrea Varela Medina**
- GitHub: [@GMA88](https://github.com/GMA88)
- LinkedIn: [Andrea Varela](https://linkedin.com/in/andrea-varela-2058311a2)
