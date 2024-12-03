from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox
from app.operations.inventario import get_inventario, add_inventario, delete_inventario

class InventoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Inventario")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tbl_inventario = QTableWidget(self)
        self.tbl_inventario.setColumnCount(4)
        self.tbl_inventario.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "Categoría"])
        layout.addWidget(self.tbl_inventario)

        self.btn_reload_inventario = QPushButton("Cargar Inventario")
        self.btn_reload_inventario.clicked.connect(self.load_inventario)
        layout.addWidget(self.btn_reload_inventario)

        self.btn_add_inventario = QPushButton("Añadir Producto")
        self.btn_add_inventario.clicked.connect(self.add_inventario)
        layout.addWidget(self.btn_add_inventario)

        self.btn_delete_inventario = QPushButton("Eliminar Producto")
        self.btn_delete_inventario.clicked.connect(self.delete_inventario)
        layout.addWidget(self.btn_delete_inventario)

        self.load_inventario()

    def load_inventario(self):
        inventario = get_inventario()
        self.tbl_inventario.setRowCount(0)
        for row_idx, producto in enumerate(inventario):
            self.tbl_inventario.insertRow(row_idx)
            self.tbl_inventario.setItem(row_idx, 0, QTableWidgetItem(str(producto["_id"])))
            self.tbl_inventario.setItem(row_idx, 1, QTableWidgetItem(producto["nombre_producto"]))
            self.tbl_inventario.setItem(row_idx, 2, QTableWidgetItem(str(producto["cantidad_disponible"])))
            self.tbl_inventario.setItem(row_idx, 3, QTableWidgetItem(producto["categoria"]))

    def add_inventario(self):
        nombre, ok_nombre = QInputDialog.getText(self, "Nuevo Producto", "Nombre:")
        if not ok_nombre or not nombre:
            return

        cantidad, ok_cantidad = QInputDialog.getInt(self, "Nuevo Producto", "Cantidad:")
        if not ok_cantidad or cantidad <= 0:
            return

        categoria, ok_categoria = QInputDialog.getText(self, "Nuevo Producto", "Categoría:")
        if not ok_categoria or not categoria:
            return

        precio, ok_precio = QInputDialog.getDouble(self, "Nuevo Producto", "Precio Unitario:", decimals=2)
        if not ok_precio:
            return

        if add_inventario(nombre, cantidad, categoria, precio):
            QMessageBox.information(self, "Éxito", "Producto añadido correctamente.")
            self.load_inventario()

    def delete_inventario(self):
        selected_items = self.tbl_inventario.selectedItems()
        if selected_items:
            producto_id = selected_items[0].text()
            confirm = QMessageBox.question(self, "Confirmar", "¿Está seguro de que desea eliminar este producto?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                if delete_inventario(producto_id):
                    QMessageBox.information(self, "Éxito", "Producto eliminado.")
                    self.load_inventario()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el producto.")
        else:
            QMessageBox.warning(self, "Error", "Seleccione un producto para eliminar.")
