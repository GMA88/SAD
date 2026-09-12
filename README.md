# 📊 SAD - Sistema de Análisis de Datos

Aplicación de escritorio de alto rendimiento desarrollada en Python y PyQt para la ingesta, procesamiento analítico y visualización interactiva de datos, con persistencia no relacional en MongoDB. SAD implementa una interfaz gráfica reactiva basada en Qt para explorar colecciones de datos, calcular métricas estadísticas descriptivas y renderizar dashboards analíticos en un entorno desacoplado y seguro.

---

## 🎯 Descripción del Proyecto

SAD optimiza el flujo de trabajo de análisis exploratorio de datos (EDA) conectando directamente la analítica de escritorio con bases de datos modernas orientadas a documentos:
- **Persistencia NoSQL:** Almacenamiento, consulta y modelado de colecciones heterogéneas mediante MongoDB (PyMongo).
- **Procesamiento Asíncrono de Datos:** Ingesta y depuración de registros fuera del hilo principal de la interfaz para evitar bloqueos visuales.
- **Motor Estadístico:** Cálculo automático de métricas descriptivas, dispersión, percentiles y resúmenes analíticos.
- **Visualización Interactiva Integrada:** Gráficos estadísticos embebidos directamente en lienzos de Qt mediante Matplotlib/Seaborn.
- **Distribución de Escritorio:** Empaquetado ejecutable mediante PyInstaller para entornos de escritorio Windows/Linux.

---

## 🏗 Arquitectura del Sistema

┌─────────────────────────────────────────────────────────┐│              Capa de Presentación (PyQt GUI)            ││  ┌───────────────────────────────────────────────────┐  ││  │ Ventanas, Widgets y Layouts (gui/ & app/)         │  ││  │ - Interfaz Modular PyQt (Signals & Slots)         │  ││  │ - Lienzos de Visualización Embebidos (Canvas Qt)  │  ││  └───────────────────────────────────────────────────┘  │└────────────────────────────┬────────────────────────────┘│Eventos / Hilos (QThread / Worker)│▼┌─────────────────────────────────────────────────────────┐│             Lógica de Negocio y Analítica               ││  ┌───────────────────────────────────────────────────┐  ││  │ Núcleo de Procesamiento (main.py / app/)          │  ││  │ - Normalización y Limpieza de Datasets            │  ││  │ - Motor Estadístico (Pandas / NumPy)              │  ││  │ - Generador Gráfico (Matplotlib / Seaborn)        │  ││  └───────────────────────────────────────────────────┘  │└────────────────────────────┬────────────────────────────┘│▼┌─────────────────────────────────────────────────────────┐│            Capa de Datos y Persistencia (NoSQL)         ││  ┌───────────────────────────────────────────────────┐  ││  │ Conexión y Gestión de Base de Datos (PyMongo)     │  ││  │ - Base de Datos: MongoDB                          │  ││  │ - Colecciones de Datos, Muestras y Resultados     │  ││  │ - Importación/Exportación de Archivos (data/)     │  ││  └───────────────────────────────────────────────────┘  │└─────────────────────────────────────────────────────────┘
---

## 🛠 Tecnologías Utilizadas

- **Lenguaje Principal:** Python 3.8+
- **Framework de Interfaz Gráfica:** PyQt (Qt Widgets, Signal-Slot Architecture)
- **Base de Datos:** MongoDB (gestión e integración vía `pymongo`)
- **Procesamiento de Datos:** Pandas, NumPy
- **Visualización Analítica:** Matplotlib (Backend Qt), Seaborn
- **Distribución:** PyInstaller (especificación de empaquetado en `main.spec`)

---

## 📁 Estructura del Repositorio

SAD/│├── app/                  # Lógica analítica, conexión a MongoDB y workers en segundo plano├── gui/                  # Componentes de la interfaz de usuario PyQt (vistas y controles)├── data/                 # Conjuntos de datos locales y archivos de intercambio├── main.py               # Punto de entrada y orquestación de la aplicación Qt├── main.spec             # Especificación para compilación de ejecutable con PyInstaller└── README.md             # Documentación del proyecto
> **Nota sobre el entorno:** Se recomienda compilar y ejecutar el proyecto ignorando las carpetas temporales de compilación (`build/`, `dist/` y cachés `__pycache__`).

---

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Contar con una instancia de **MongoDB** local o un clúster remoto (MongoDB Atlas).

### Opción 1: Ejecución desde Código Fuente

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/GMA88/SAD.git](https://github.com/GMA88/SAD.git)
   cd SAD
Crear y activar un entorno virtual:Bashpython -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
Instalar dependencias:Bashpip install PyQt5 pymongo pandas numpy matplotlib seaborn pyinstaller
# O PyQt6 según el entorno configurado
Configurar la URI de conexión de MongoDB en las variables de entorno o archivo de configuración:Bash# Ejemplo local
export MONGO_URI="mongodb://localhost:27017/"
Iniciar la aplicación:Bashpython main.py
Opción 2: Compilación con PyInstallerPara generar el ejecutable binario de escritorio para distribución:Bashpyinstaller main.spec
El archivo ejecutable listo para producción se creará dentro del directorio dist/.🎓 Competencias Técnicas DemostradasIngeniería de Software de Escritorio: Implementación de arquitectura orientada a eventos (Signals & Slots) con PyQt.Integración NoSQL: Diseño y gestión de colecciones en MongoDB para persistencia de datos analíticos.Ciencia y Exploración de Datos: Procesamiento de datos estructurados/semiestructurados y generación de dashboards gráficos.Empaquetado y Despliegue: Creación de artefactos ejecutables reproducibles con PyInstaller.👥 Autora & ContactoAndrea Varela MedinaLinkedIn: linkedin.com/in/andrea-varela-2058311a2  GitHub: @GMA88  Email: avarelam8@gmail.com  Ubicación: Salamanca, Guanajuato, México  📊 SAD - Data Analysis System (English)High-performance desktop software developed in Python and PyQt for dataset ingestion, statistical processing, and interactive visual reporting, backed by MongoDB for NoSQL persistence. SAD provides a Qt-driven graphical user interface to query collections, compute descriptive analytics, and render interactive dashboards in an isolated local runtime.🎯 Project OverviewSAD streamlines exploratory data analysis (EDA) workflows by connecting desktop performance with document-based database storage:NoSQL Persistence: Storage, querying, and schema flexibility using MongoDB (PyMongo).Responsive Data Processing: Multi-threaded ingestion and cleaning routines executed outside the GUI thread to ensure responsiveness.Statistical Engine: Automated evaluation of central tendency, dispersion, percentiles, and categorical metrics.Embedded Visualization: Statistical visualizations rendered directly onto Qt-integrated canvases using Matplotlib/Seaborn.Desktop Packaging: Standalone deployment support using PyInstaller for zero-dependency binary execution.🏗 System Architecture┌─────────────────────────────────────────────────────────┐
│              Presentation Layer (PyQt GUI)              │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Windows, Widgets & Layouts (gui/ & app/)          │  │
│  │ - Modular PyQt Interface (Signals & Slots)        │  │
│  │ - Embedded Data Canvases (Qt FigureCanvas)        │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────┘
                             │
             Events / Threads (QThread / Worker)
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│            Business Logic & Data Processing             │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Analytical Engine (main.py / app/)                │  │
│  │ - Data Cleaning & Schema Normalization            │  │
│  │ - Statistical Analysis (Pandas / NumPy)           │  │
│  │ - Visual Rendering Engine (Matplotlib / Seaborn)  │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│            Data Layer & Persistence (NoSQL)             │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Database Integration & Storage (PyMongo)          │  │
│  │ - Database Engine: MongoDB                        │  │
│  │ - Dataset Collections, Samples & Results          │  │
│  │ - Local Data Files & Exports (data/)              │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
🛠 Tech StackCore Language: Python 3.8+GUI Framework: PyQt (Qt Widgets, Signal-Slot Architecture)Database: MongoDB (integrated via pymongo)Data Engineering: Pandas, NumPyVisual Analytics: Matplotlib (Qt Backend), SeabornPackaging & Build: PyInstaller (main.spec configuration file)📁 Repository StructureSAD/
│
├── app/                  # Analytics engine, MongoDB connectors, and thread workers
├── gui/                  # PyQt interface components, custom layouts, and views
├── data/                 # Local data assets and file exports
├── main.py               # Application entry point and Qt loop orchestrator
├── main.spec             # PyInstaller build specification file
└── README.md             # Project documentation
🚀 Setup & InstallationPrerequisitesA running local or remote MongoDB instance.Option 1: Running from SourceClone the repository:Bashgit clone [https://github.com/GMA88/SAD.git](https://github.com/GMA88/SAD.git)
cd SAD
Initialize virtual environment:Bashpython -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
Install dependencies:Bashpip install PyQt5 pymongo pandas numpy matplotlib seaborn pyinstaller
# Or PyQt6 depending on your local setup
Set your MongoDB connection URI:Bashexport MONGO_URI="mongodb://localhost:27017/"
Run application:Bashpython main.py
Option 2: Building Standalone ExecutableTo compile a standalone binary using the repository specification:Bashpyinstaller main.spec
The compiled output will be generated inside the dist/ directory.🎓 Key CompetenciesDesktop Application Architecture: Event-driven design with PyQt, decoupling 
presentation from background workers.NoSQL Data Modeling: Document storage and query execution via MongoDB.Exploratory Data Analysis: Schema parsing, statistical routines, and dynamic canvas rendering.Application Distribution: Managing reproducible binary packaging using PyInstaller.👥 Author & ContactAndrea Varela MedinaLinkedIn: linkedin.com/in/andrea-varela-2058311a2  GitHub: @GMA88  Email: avarelam8@gmail.com  Location: Salamanca, Guanajuato, Mexico 
