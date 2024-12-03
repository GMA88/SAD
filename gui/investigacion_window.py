from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox
from app.operations.investigacion import get_investigaciones, add_investigacion, delete_investigacion

class ResearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Investigación")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tbl_investigaciones = QTableWidget(self)
        self.tbl_investigaciones.setColumnCount(4)
        self.tbl_investigaciones.setHorizontalHeaderLabels(["ID", "Título", "Descripción", "Responsable"])
        layout.addWidget(self.tbl_investigaciones)

        self.btn_reload_investigaciones = QPushButton("Cargar Investigaciones")
        self.btn_reload_investigaciones.clicked.connect(self.load_investigaciones)
        layout.addWidget(self.btn_reload_investigaciones)

        # Botón para añadir investigación
        self.btn_add_investigacion = QPushButton("Añadir Investigación")
        self.btn_add_investigacion.clicked.connect(self.add_investigacion)
        layout.addWidget(self.btn_add_investigacion)

        # Botón para eliminar investigación
        self.btn_delete_investigacion = QPushButton("Eliminar Investigación")
        self.btn_delete_investigacion.clicked.connect(self.delete_investigacion)
        layout.addWidget(self.btn_delete_investigacion)

        self.load_investigaciones()

    def load_investigaciones(self):
        investigaciones = get_investigaciones()
        print(investigaciones)  # Verifica si estás obteniendo los datos
    
        self.tbl_investigaciones.setRowCount(0)
        for row_idx, investigacion in enumerate(investigaciones):
            self.tbl_investigaciones.insertRow(row_idx)
            self.tbl_investigaciones.setItem(row_idx, 0, QTableWidgetItem(str(investigacion["_id"])))
            self.tbl_investigaciones.setItem(row_idx, 1, QTableWidgetItem(investigacion["nombre_proyecto"]))
            self.tbl_investigaciones.setItem(row_idx, 2, QTableWidgetItem(investigacion["descripcion"]))
            self.tbl_investigaciones.setItem(row_idx, 3, QTableWidgetItem(investigacion["responsable"]))
    
        # Actualizar la vista de la tabla
        self.tbl_investigaciones.viewport().update()


    def add_investigacion(self):
        titulo, ok_titulo = QInputDialog.getText(self, "Nueva Investigación", "Título de la Investigación:")
        if not ok_titulo or not titulo:
            return

        descripcion, ok_descripcion = QInputDialog.getText(self, "Nueva Investigación", "Descripción:")
        if not ok_descripcion or not descripcion:
            return

        responsable, ok_responsable = QInputDialog.getText(self, "Nueva Investigación", "Responsable:")
        if not ok_responsable or not responsable:
            return

        if add_investigacion(titulo, descripcion, responsable):
            QMessageBox.information(self, "Éxito", "Investigación añadida correctamente.")
            self.load_investigaciones()

    def delete_investigacion(self):
        selected_items = self.tbl_investigaciones.selectedItems()
        if selected_items:
            investigacion_id = selected_items[0].text()
            confirm = QMessageBox.question(self, "Confirmar", "¿Está seguro de que desea eliminar esta investigación?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                if delete_investigacion(investigacion_id):
                    QMessageBox.information(self, "Éxito", "Investigación eliminada.")
                    self.load_investigaciones()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar la investigación.")
        else:
            QMessageBox.warning(self, "Error", "Seleccione una investigación para eliminar.")
