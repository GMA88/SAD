from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox
from app.operations.usuarios import get_pending_requests, approve_user

class UserManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Usuarios")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tbl_users = QTableWidget(self)
        self.tbl_users.setColumnCount(2)
        self.tbl_users.setHorizontalHeaderLabels(["Usuario", "Acción"])
        layout.addWidget(self.tbl_users)

        self.btn_reload_users = QPushButton("Cargar Solicitudes Pendientes")
        self.btn_reload_users.clicked.connect(self.load_pending_requests)
        layout.addWidget(self.btn_reload_users)

        self.btn_approve_user = QPushButton("Aprobar Usuario")
        self.btn_approve_user.clicked.connect(self.approve_selected_user)
        layout.addWidget(self.btn_approve_user)

        self.load_pending_requests()

    def load_pending_requests(self):
        pending_requests = get_pending_requests()
        self.tbl_users.setRowCount(0)
        for row_idx, request in enumerate(pending_requests):
            self.tbl_users.insertRow(row_idx)
            self.tbl_users.setItem(row_idx, 0, QTableWidgetItem(request["username"]))

    def approve_selected_user(self):
        selected_items = self.tbl_users.selectedItems()
        if selected_items:
            username = selected_items[0].text()
            role, ok_role = QInputDialog.getText(self, "Aprobar Usuario", "Asignar Rol:")
            if ok_role and role:
                if approve_user(username, role):
                    QMessageBox.information(self, "Éxito", f"Usuario '{username}' aprobado con rol '{role}'.")
                    self.load_pending_requests()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo aprobar el usuario.")
        else:
            QMessageBox.warning(self, "Error", "Seleccione un usuario para aprobar.")


# Añadir funcionalidad para gestionar distribuidores a la ventana de ventas
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox
from app.operations.distribuidores import get_distribuidores, add_distribuidor, delete_distribuidor

class DistributorManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Distribuidores")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tbl_distribuidores = QTableWidget(self)
        self.tbl_distribuidores.setColumnCount(4)
        self.tbl_distribuidores.setHorizontalHeaderLabels(["ID", "Nombre", "Contacto", "Teléfono"])
        layout.addWidget(self.tbl_distribuidores)

        self.btn_reload_distribuidores = QPushButton("Cargar Distribuidores")
        self.btn_reload_distribuidores.clicked.connect(self.load_distribuidores)
        layout.addWidget(self.btn_reload_distribuidores)

        self.btn_add_distribuidor = QPushButton("Añadir Distribuidor")
        self.btn_add_distribuidor.clicked.connect(self.add_distribuidor)
        layout.addWidget(self.btn_add_distribuidor)

        self.btn_delete_distribuidor = QPushButton("Eliminar Distribuidor")
        self.btn_delete_distribuidor.clicked.connect(self.delete_distribuidor)
        layout.addWidget(self.btn_delete_distribuidor)

        self.load_distribuidores()

    def load_distribuidores(self):
        distribuidores = get_distribuidores()
        self.tbl_distribuidores.setRowCount(0)
        for row_idx, distribuidor in enumerate(distribuidores):
            self.tbl_distribuidores.insertRow(row_idx)
            self.tbl_distribuidores.setItem(row_idx, 0, QTableWidgetItem(str(distribuidor["_id"])))
            self.tbl_distribuidores.setItem(row_idx, 1, QTableWidgetItem(distribuidor["nombre"]))
            self.tbl_distribuidores.setItem(row_idx, 2, QTableWidgetItem(distribuidor["contacto"]))
            self.tbl_distribuidores.setItem(row_idx, 3, QTableWidgetItem(distribuidor["telefono"]))

    def add_distribuidor(self):
        nombre, ok_nombre = QInputDialog.getText(self, "Nuevo Distribuidor", "Nombre:")
        if not ok_nombre or not nombre:
            return

        contacto, ok_contacto = QInputDialog.getText(self, "Nuevo Distribuidor", "Contacto:")
        if not ok_contacto or not contacto:
            return

        telefono, ok_telefono = QInputDialog.getText(self, "Nuevo Distribuidor", "Teléfono:")
        if not ok_telefono or not telefono:
            return

        if add_distribuidor(nombre, contacto, telefono):
            QMessageBox.information(self, "Éxito", "Distribuidor añadido correctamente.")
            self.load_distribuidores()

    def delete_distribuidor(self):
        selected_items = self.tbl_distribuidores.selectedItems()
        if selected_items:
            distribuidor_id = selected_items[0].text()
            confirm = QMessageBox.question(self, "Confirmar", "¿Está seguro de que desea eliminar este distribuidor?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                if delete_distribuidor(distribuidor_id):
                    QMessageBox.information(self, "Éxito", "Distribuidor eliminado.")
                    self.load_distribuidores()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el distribuidor.")
        else:
            QMessageBox.warning(self, "Error", "Seleccione un distribuidor para eliminar.")

