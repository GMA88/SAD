from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QLineEdit, QLabel, QDialog, QDialogButtonBox, QFormLayout, QMessageBox
from app.operations.usuarios import login_user
from gui.admin import AdminWindow
from gui.ventas_window import SalesWindow
from gui.investigacion_window import ResearchWindow
from gui.finanzas_window import FinanceWindow
from gui.rrhh_window import HRWindow
from gui.inventario_window import InventoryWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.clicked.connect(self.login)
        layout.addWidget(self.btn_login)

    def login(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Inicio de Sesión")

        layout = QFormLayout(dialog)
        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)

        layout.addRow(QLabel("Usuario:"), username_input)
        layout.addRow(QLabel("Contraseña:"), password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            username = username_input.text()
            password = password_input.text()
            role = login_user(username, password)
            if role:
                QMessageBox.information(self, "Inicio de Sesión", f"Bienvenido, {username}")
                self.open_window_by_role(role)
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

    def open_window_by_role(self, role):
        if role == "admin":
            self.admin_window = AdminWindow()
            self.admin_window.show()
        elif role == "ventas":
            self.sales_window = SalesWindow()
            self.sales_window.show()
        elif role == "investigador":
            self.research_window = ResearchWindow()
            self.research_window.show()
        elif role == "finanzas":
            self.finance_window = FinanceWindow()
            self.finance_window.show()
        elif role == "recursos_humanos":
            self.hr_window = HRWindow()
            self.hr_window.show()
        elif role == "inventario":
            self.inventory_window = InventoryWindow()
            self.inventory_window.show()
        else:
            QMessageBox.warning(self, "Error", "Rol no reconocido.")
