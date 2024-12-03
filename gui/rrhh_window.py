from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox
from app.operations.empleados import get_empleados, add_empleado, delete_empleado

class HRWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Recursos Humanos")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tbl_empleados = QTableWidget(self)
        self.tbl_empleados.setColumnCount(4)
        self.tbl_empleados.setHorizontalHeaderLabels(["ID", "Nombre", "Puesto", "Salario"])
        layout.addWidget(self.tbl_empleados)

        self.btn_reload = QPushButton("Cargar Empleados")
        self.btn_reload.clicked.connect(self.load_empleados)
        layout.addWidget(self.btn_reload)

        self.btn_add = QPushButton("Añadir Empleado")
        self.btn_add.clicked.connect(self.add_empleado)
        layout.addWidget(self.btn_add)

        self.btn_delete = QPushButton("Eliminar Empleado")
        self.btn_delete.clicked.connect(self.delete_empleado)
        layout.addWidget(self.btn_delete)

        self.load_empleados()

    def load_empleados(self):
        empleados = get_empleados()
        print(empleados)  # Verifica si estás obteniendo los datos correctos
    
        self.tbl_empleados.setRowCount(0)
        for row_idx, empleado in enumerate(empleados):
            self.tbl_empleados.insertRow(row_idx)
            self.tbl_empleados.setItem(row_idx, 0, QTableWidgetItem(str(empleado["_id"])))
            self.tbl_empleados.setItem(row_idx, 1, QTableWidgetItem(empleado["nombre"]))
            self.tbl_empleados.setItem(row_idx, 2, QTableWidgetItem(empleado["puesto"]))
            self.tbl_empleados.setItem(row_idx, 3, QTableWidgetItem(str(empleado["salario"])))
    
        # Actualizar la vista de la tabla
        self.tbl_empleados.viewport().update()

    def add_empleado(self):
        nombre, ok_nombre = QInputDialog.getText(self, "Nuevo Empleado", "Nombre:")
        if not ok_nombre or not nombre:
            return
    
        puesto, ok_puesto = QInputDialog.getText(self, "Nuevo Empleado", "Puesto:")
        if not ok_puesto or not puesto:
            return
    
        departamento, ok_departamento = QInputDialog.getText(self, "Nuevo Empleado", "Departamento:")
        if not ok_departamento or not departamento:
            return
    
        salario, ok_salario = QInputDialog.getInt(self, "Nuevo Empleado", "Salario:")
        if not ok_salario or salario <= 0:
            return
    
        fecha_contratacion, ok_fecha = QInputDialog.getText(self, "Nuevo Empleado", "Fecha de Contratación (AAAA-MM-DD):")
        if not ok_fecha or not fecha_contratacion:
            return
    
        email, ok_email = QInputDialog.getText(self, "Nuevo Empleado", "Correo Electrónico:")
        if not ok_email or not email:
            return
    
        telefono, ok_telefono = QInputDialog.getText(self, "Nuevo Empleado", "Teléfono:")
        if not ok_telefono or not telefono:
            return
    
        if add_empleado(nombre, puesto, departamento, salario, fecha_contratacion, email, telefono):
            QMessageBox.information(self, "Éxito", "Empleado añadido correctamente.")
            self.load_empleados()

    def delete_empleado(self):
        selected_items = self.tbl_empleados.selectedItems()
        if selected_items:
            empleado_id = selected_items[0].text()
            confirm = QMessageBox.question(self, "Confirmar", "¿Está seguro de que desea eliminar este empleado?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                if delete_empleado(empleado_id):
                    QMessageBox.information(self, "Éxito", "Empleado eliminado.")
                    self.load_empleados()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el empleado.")
        else:
            QMessageBox.warning(self, "Error", "Seleccione un empleado para eliminar.")
