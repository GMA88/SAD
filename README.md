# 📋 SAD - Sistema de Administración de Datos

Aplicación de escritorio desarrollada en Python y PyQt para la gestión, consulta y edición de registros almacenados en MongoDB. El sistema implementa una interfaz gráfica de tablas dinámicas con control de vistas y permisos según el tipo de usuario.

---

## 🎯 Funcionalidades

- **Autenticación y Permisos por Rol:** Vistas y niveles de edición personalizados según el perfil del usuario autenticado.
- **Gestión de Datos (CRUD):** Visualización tabular, búsqueda, edición directa y actualización de registros.
- **Persistencia NoSQL:** Conexión y sincronización de datos en tiempo real mediante MongoDB (PyMongo).
- **Interfaz de Escritorio:** GUI interactiva desarrollada con componentes nativos de PyQt.

---

## 🛠 Tecnologías

- **Lenguaje:** Python 3.x
- **Interfaz Gráfica:** PyQt
- **Base de Datos:** MongoDB (`pymongo`)
- **Empaquetado:** PyInstaller (`main.spec`)

---

## 📁 Estructura del Repositorio

SAD/
├── app/                  # Lógica de operaciones y conexión a MongoDB
├── gui/                  # Interfaces de usuario, ventanas y tablas (PyQt)
├── data/                 # Muestras y archivos de prueba locales
├── main.py               # Punto de entrada de la aplicación
├── main.spec             # Archivo de configuración para PyInstaller
└── README.md

---

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/GMA88/SAD.git](https://github.com/GMA88/SAD.git)
   cd SAD
   
Crear entorno e instalar dependencias:

Bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

pip install PyQt5 pymongo pyinstaller
Ejecutar aplicación:

Bash
python main.py

👥 Autora

Andrea Varela Medina

GitHub: @GMA88

LinkedIn: linkedin.com/in/andrea-varela-2058311a2

📋 SAD - Data Administration System (English)
Desktop application built with Python and PyQt for managing, browsing, and editing database records stored in MongoDB. The system features a dynamic table interface with customized views and editing permissions based on user roles.

🎯 Features
Role-Based Access Control: Tailored views and edit permissions according to the user profile.

CRUD Management: Tabular display, search, inline editing, and updating of database documents.

NoSQL Persistence: Data connection and storage handling using MongoDB (PyMongo).

Desktop UI: Responsive graphical interface built with PyQt widgets.

🛠 Tech Stack
Language: Python 3.x

GUI Framework: PyQt

Database: MongoDB (pymongo)

Packaging: PyInstaller (main.spec)

🚀 Setup & Execution
Clone the repository:

Bash
git clone [https://github.com/GMA88/SAD.git](https://github.com/GMA88/SAD.git)
cd SAD
Create virtual environment and install requirements:

Bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install PyQt5 pymongo pyinstaller
Run the app:

Bash
python main.py

👥 Author

Andrea Varela Medina

GitHub: @GMA88

LinkedIn: linkedin.com/in/andrea-varela-2058311a2

---

# 📋 SAD - Data Management System (English)

Desktop application developed in Python and PyQt for browsing, updating, and managing records stored in MongoDB. The application provides dynamic table views with role-based access control.

### 🎯 Key Features
- **Role-Based Access Control:** View and edit privileges tailored to user credentials.
- **CRUD Operations:** Search, filter, inline editing, and record updates.
- **NoSQL Persistence:** Real-time collection queries and storage handled via MongoDB (`pymongo`).
- **Native GUI:** Event-driven desktop interface designed with PyQt widgets.

### 🛠 Tech Stack
- **Language:** Python 3.x
- **GUI Framework:** PyQt
- **Database:** MongoDB (`pymongo`)
- **Distribution:** PyInstaller (`main.spec`)

### 🚀 Quick Start
1. **Clone repository:**
   ```bash
   git clone [https://github.com/GMA88/SAD.git](https://github.com/GMA88/SAD.git)
   cd SAD

Install dependencies:

Bash
pip install PyQt5 pymongo pyinstaller
Run app:

Bash
python main.py
👥 Author
Andrea Varela Medina

GitHub: @GMA88

LinkedIn: linkedin.com/in/andrea-varela-2058311a2
