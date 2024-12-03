from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox
from app.operations.ventas import get_ventas, add_venta, delete_venta
from gui.manage_users import DistributorManagementWindow  # Importar la ventana de gestión de distribuidores

class SalesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Ventas")
        self.setGeometry(100, 100, 1000, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tbl_ventas = QTableWidget(self)
        self.tbl_ventas.setColumnCount(4)
        self.tbl_ventas.setHorizontalHeaderLabels(["ID", "Producto", "Cantidad", "Total"])
        layout.addWidget(self.tbl_ventas)

        self.btn_reload_ventas = QPushButton("Cargar Ventas")
        self.btn_reload_ventas.clicked.connect(self.load_ventas)
        layout.addWidget(self.btn_reload_ventas)

        self.btn_add_venta = QPushButton("Registrar Venta")
        self.btn_add_venta.clicked.connect(self.add_venta)
        layout.addWidget(self.btn_add_venta)

        self.btn_delete_venta = QPushButton("Eliminar Venta")
        self.btn_delete_venta.clicked.connect(self.delete_venta)
        layout.addWidget(self.btn_delete_venta)

        # Agregar botón para gestionar distribuidores
        self.btn_manage_distribuidores = QPushButton("Gestionar Distribuidores")
        self.btn_manage_distribuidores.clicked.connect(self.open_distributor_management)
        layout.addWidget(self.btn_manage_distribuidores)

        self.load_ventas()

    def load_ventas(self):
        ventas = get_ventas()
        self.tbl_ventas.setRowCount(0)
        for row_idx, venta in enumerate(ventas):
            self.tbl_ventas.insertRow(row_idx)
            self.tbl_ventas.setItem(row_idx, 0, QTableWidgetItem(str(venta["_id"])))
            self.tbl_ventas.setItem(row_idx, 1, QTableWidgetItem(venta["nombre_producto"]))
            self.tbl_ventas.setItem(row_idx, 2, QTableWidgetItem(str(venta["cantidad"])))
            self.tbl_ventas.setItem(row_idx, 3, QTableWidgetItem(f"{venta['total_venta']:.2f}"))

    def add_venta(self):
        nombre_o_codigo_producto, ok_producto = QInputDialog.getText(self, "Nueva Venta", "Nombre o Código del Producto:")
        if not ok_producto or not nombre_o_codigo_producto:
            return

        cantidad, ok_cantidad = QInputDialog.getInt(self, "Nueva Venta", "Cantidad:")
        if not ok_cantidad or cantidad <= 0:
            return

        vendedor, ok_vendedor = QInputDialog.getText(self, "Nueva Venta", "Vendedor:")
        if not ok_vendedor or not vendedor:
            return

        cliente_nombre, ok_cliente = QInputDialog.getText(self, "Nueva Venta", "Nombre del Cliente:")
        if not ok_cliente or not cliente_nombre:
            return

        try:
            if add_venta(nombre_o_codigo_producto, cantidad, vendedor, cliente_nombre, "", "", ""):
                QMessageBox.information(self, "Éxito", "Venta registrada correctamente.")
                self.load_ventas()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def delete_venta(self):
        selected_items = self.tbl_ventas.selectedItems()
        if selected_items:
            venta_id = selected_items[0].text()
            confirm = QMessageBox.question(self, "Confirmar", "¿Está seguro de que desea eliminar esta venta?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                if delete_venta(venta_id):
                    QMessageBox.information(self, "Éxito", "Venta eliminada.")
                    self.load_ventas()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar la venta.")
        else:
            QMessageBox.warning(self, "Error", "Seleccione una venta para eliminar.")

    def open_distributor_management(self):
        # Abrir la ventana de gestión de distribuidores
        self.distributor_management_window = DistributorManagementWindow()
        self.distributor_management_window.show()
