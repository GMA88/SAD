from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QMenuBar, QMenu, QAction, QLineEdit, QLabel, QComboBox
from pymongo import MongoClient
import hashlib
import sys

# Conexión a la base de datos
MONGO_URI = ""
client = MongoClient(MONGO_URI)
db = client["empresa"]

collections = {
    "Compras": db.compras,
    "Distribuidores": db.distribuidores,
    "Finanzas": db.finanzas,
    "Inventario": db.inventario,
    "Investigación": db.investigacion,
    "Proveedores": db.proveedores,
    "Recursos Humanos": db.rrhh,
    "Usuarios": db.users,
    "Ventas": db.ventas
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Administrador")
        self.setGeometry(100, 100, 1000, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.data_table = QTableWidget()
        layout.addWidget(self.data_table)

        # Crear menú para seleccionar la colección
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.collection_menu = QMenu("Colecciones", self)
        self.menu_bar.addMenu(self.collection_menu)

        self.current_collection = None
        for collection_name in collections.keys():
            action = QAction(collection_name, self)
            action.triggered.connect(lambda checked, name=collection_name: self.load_collection(name))
            self.collection_menu.addAction(action)

        self.add_row_button = QPushButton("Agregar Fila")
        self.add_row_button.clicked.connect(self.add_row)
        layout.addWidget(self.add_row_button)

        self.delete_row_button = QPushButton("Eliminar Fila Seleccionada")
        self.delete_row_button.clicked.connect(self.delete_row)
        layout.addWidget(self.delete_row_button)

        self.save_data_button = QPushButton("Guardar Cambios")
        self.save_data_button.clicked.connect(self.save_data)
        layout.addWidget(self.save_data_button)

        # Campos para agregar nuevos usuarios
        self.username_label = QLabel("Nombre de usuario:")
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Contraseña:")
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.role_label = QLabel("Rol:")
        layout.addWidget(self.role_label)
        self.role_input = QComboBox()
        self.role_input.addItems(["admin", "investigador", "ventas", "inventario", "recursos_humanos", "finanzas"])
        layout.addWidget(self.role_input)

        self.add_user_button = QPushButton("Agregar Usuario")
        self.add_user_button.clicked.connect(self.add_user)
        layout.addWidget(self.add_user_button)

    def load_collection(self, collection_name):
        # Cargar los datos de la colección seleccionada en la tabla
        self.current_collection = collections[collection_name]
        documents = list(self.current_collection.find())

        if documents:
            self.data_table.setColumnCount(len(documents[0].keys()))
            self.data_table.setHorizontalHeaderLabels(documents[0].keys())
        else:
            self.data_table.setColumnCount(1)
            self.data_table.setHorizontalHeaderLabels(["Datos"])

        self.data_table.setRowCount(0)
        for row_idx, document in enumerate(documents):
            self.data_table.insertRow(row_idx)
            for col_idx, key in enumerate(document.keys()):
                value = document[key]
                if isinstance(value, dict) and "$oid" in value:
                    value = value["$oid"]
                elif isinstance(value, dict) and "$date" in value:
                    value = value["$date"]
                self.data_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_user(self):
        # Obtener la información ingresada
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText()

        # Validar que los campos no estén vacíos
        if not username or not password or not role:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return

        # Hashear la contraseña
        hashed_password = hash_password(password)

        # Crear el usuario y guardarlo en la base de datos
        usuario = {"username": username, "password": hashed_password, "role": role}
        db.users.update_one({"username": username}, {"$set": usuario}, upsert=True)

        # Limpiar los campos y mostrar un mensaje de confirmación
        self.username_input.clear()
        self.password_input.clear()
        QMessageBox.information(self, "Éxito", "Usuario agregado correctamente.")

    def add_row(self):
        # Agregar una nueva fila a la tabla de datos
        current_row_count = self.data_table.rowCount()
        self.data_table.insertRow(current_row_count)

    def delete_row(self):
        # Eliminar la fila seleccionada de la tabla de datos
        current_row = self.data_table.currentRow()
        if current_row != -1:
            self.data_table.removeRow(current_row)
        else:
            QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para eliminar.")

    def save_data(self):
        # Guardar los cambios realizados en la tabla de datos en la base de datos
        if self.current_collection is None:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna colección.")
            return

        updated_documents = []
        for row_idx in range(self.data_table.rowCount()):
            document = {}
            for col_idx in range(self.data_table.columnCount()):
                header = self.data_table.horizontalHeaderItem(col_idx).text()
                item = self.data_table.item(row_idx, col_idx)
                value = item.text() if item else ""
                document[header] = value
            updated_documents.append(document)

        # Actualizar la base de datos
        self.current_collection.delete_many({})
        self.current_collection.insert_many(updated_documents)
        QMessageBox.information(self, "Éxito", "Datos guardados correctamente.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = AdminWindow()
    main_window.show()
    sys.exit(app.exec_())