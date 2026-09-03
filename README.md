# 📱 SAD - Sistema de Análisis de Datos

Una aplicación web interactiva desarrollada en HTML, CSS y JavaScript para el análisis, visualización y procesamiento de datos. SAD proporciona una interfaz intuitiva para trabajar con conjuntos de datos complejos y generar reportes visuales.

## ✨ Características

- **Interfaz Responsiva**: Diseño adaptable a dispositivos móviles y desktop
- **Análisis de Datos**: Herramientas para procesar y analizar información
- **Visualización Interactiva**: Gráficos dinámicos y dashboards
- **Exportación de Reportes**: Descarga de resultados en múltiples formatos
- **Gestión de Datos**: Importar, filtrar y transformar datos
- **Tema Oscuro/Claro**: Modo de visualización personalizable

## 🛠️ Tecnologías

- **HTML5**: Estructura y semántica
- **CSS3**: Diseño responsivo y animaciones
- **JavaScript (ES6+)**: Funcionalidad interactiva
- **Librerías**:
  - `Chart.js` - Visualización de gráficos
  - `DataTables` - Manipulación de tablas
  - `Axios` - Llamadas AJAX
  - `Bootstrap` - Framework CSS (opcional)

## 📦 Requisitos Previos

- Navegador moderno (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Servidor web para desarrollo local
- Editor de código (VS Code, Sublime Text, etc.)

## 🚀 Instalación y Uso

### Opción 1: Ejecución Directa

1. Clonar el repositorio:
```bash
git clone https://github.com/GMA88/SAD.git
cd SAD
```

2. Abrir en el navegador:
```bash
# En Linux/Mac
open index.html

# En Windows
start index.html

# O usar un servidor HTTP
python -m http.server 8000
# Luego visitar: http://localhost:8000
```

### Opción 2: Usar un Servidor Local

```bash
# Con Python 3
python -m http.server 8000

# Con Python 2
python -m SimpleHTTPServer 8000

# Con Node.js (http-server)
npx http-server

# Con Live Server (VS Code)
# Instalar extensión "Live Server" y hacer clic derecho > Open with Live Server
```

## 📁 Estructura del Proyecto

```
SAD/
├── index.html                # Página principal
├── css/
│   ├── style.css             # Estilos principales
│   └── responsive.css        # Diseño responsivo
├── js/
│   ├── main.js               # Lógica principal
│   ├── data-processor.js      # Procesamiento de datos
│   └── charts.js             # Generación de gráficos
├── data/
│   └── sample-data.json       # Datos de ejemplo
├── assets/
│   ├── images/               # Imágenes
│   └── icons/                # Iconos
└── README.md                 # Este archivo
```

## 📊 Uso Rápido

### 1. Importar Datos

```javascript
// Cargar datos desde archivo CSV/JSON
const data = await loadDataFile('data/sample-data.json');
```

### 2. Procesar Datos

```javascript
// Filtrar, transformar y limpiar datos
const processedData = processDataset(data, {
    removeNulls: true,
    normalizeValues: true
});
```

### 3. Visualizar

```javascript
// Generar gráficos
const chart = createChart('canvas-id', {
    type: 'bar',
    data: processedData,
    options: { responsive: true }
});
```

### 4. Exportar Resultados

```javascript
// Descargar reportes
exportToCSV(processedData, 'reporte.csv');
exportToPDF(processedData, 'reporte.pdf');
```

## 🎨 Interfaz Principal

### Secciones

1. **Dashboard**: Vista general de los datos principales
2. **Análisis**: Herramientas de análisis estadístico
3. **Visualización**: Gráficos y representaciones visuales
4. **Reportes**: Generación y descarga de informes
5. **Configuración**: Opciones de personalización

## 🔧 Configuración

Editar `config.js`:

```javascript
const CONFIG = {
    theme: 'light',           // 'light' o 'dark'
    language: 'es',           // Idioma de la interfaz
    maxDataPoints: 10000,     // Máximo de puntos de datos
    chartType: 'bar',         // Tipo de gráfico por defecto
    exportFormats: ['csv', 'json', 'pdf']
};
```

## 📚 Funciones Principales

### Análisis Estadístico
- Media, Mediana, Desviación Estándar
- Percentiles y Cuartiles
- Análisis de Correlación

### Visualización
- Gráficos de Barras
- Gráficos de Líneas
- Gráficos Circulares
- Histogramas
- Heatmaps

### Filtrado y Búsqueda
- Filtros multidimensionales
- Búsqueda en tiempo real
- Ordenamiento personalizado

## 💻 Desarrollo

### Estructura de Código

```html
<!-- Contenedor principal -->
<div id="app-container">
    <header id="navbar"></header>
    <main id="content"></main>
    <footer id="footer"></footer>
</div>

<!-- Scripts -->
<script src="js/main.js"></script>
<script src="js/data-processor.js"></script>
<script src="js/charts.js"></script>
```

### Agregar Nueva Funcionalidad

```javascript
// 1. Crear módulo
const MyModule = (() => {
    const init = () => { /* ... */ };
    return { init };
})();

// 2. Registrar en main.js
document.addEventListener('DOMContentLoaded', () => {
    MyModule.init();
});
```

## 🧪 Testing

Para realizar pruebas en navegador:

1. Abrir consola (F12)
2. Verificar que no hay errores
3. Probar funciones en consola:
```javascript
// Prueba de carga de datos
loadDataFile('data/sample-data.json').then(console.log);

// Prueba de procesamiento
processDataset(sampleData, {}).then(console.log);
```

## 📱 Compatibilidad

| Navegador | Versión Mínima |
|-----------|----------------|
| Chrome    | 90+            |
| Firefox   | 88+            |
| Safari    | 14+            |
| Edge      | 90+            |

## 🐛 Problemas Comunes

**Problema**: Gráficos no se cargan
```javascript
// Solución: Verificar que Chart.js está cargado
console.log(Chart); // Debe retornar función
```

**Problema**: Datos no se importan
```javascript
// Solución: Verificar formato del archivo
// JSON: { "data": [...] }
// CSV: col1,col2,col3
```

## 📝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📚 Recursos

- [MDN Web Docs](https://developer.mozilla.org/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [DataTables Documentation](https://datatables.net/)
- [HTML5 Specification](https://html.spec.whatwg.org/)

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE). Ver archivo `LICENSE` para más detalles.

## 👥 Autor

**GMA88** - [GitHub Profile](https://github.com/GMA88)

## 💬 Soporte

Para soporte o sugerencias:
- Abre un [Issue](https://github.com/GMA88/SAD/issues)
- Crea una [Discussion](https://github.com/GMA88/SAD/discussions)
- Contacta directamente mediante GitHub

---

⭐ Si este proyecto te fue útil, considera darle una estrella

**Versión**: 1.0.0  
**Última actualización**: 2024
