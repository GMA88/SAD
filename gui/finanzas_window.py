from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox
from app.operations.finanzas import get_finanzas, add_finanza, delete_finanza

class FinanceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Finanzas")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tbl_finanzas = QTableWidget(self)
        self.tbl_finanzas.setColumnCount(4)
        self.tbl_finanzas.setHorizontalHeaderLabels(["ID", "Descripción", "Tipo", "Monto"])
        layout.addWidget(self.tbl_finanzas)

        self.btn_reload = QPushButton("Cargar Finanzas")
        self.btn_reload.clicked.connect(self.load_finanzas)
        layout.addWidget(self.btn_reload)

        self.btn_add = QPushButton("Registrar Transacción")
        self.btn_add.clicked.connect(self.add_finanza)
        layout.addWidget(self.btn_add)

        self.btn_delete = QPushButton("Eliminar Transacción")
        self.btn_delete.clicked.connect(self.delete_finanza)
        layout.addWidget(self.btn_delete)

        self.load_finanzas()

    def load_finanzas(self):
        finanzas = get_finanzas()
        self.tbl_finanzas.setRowCount(0)
        for row_idx, finanza in enumerate(finanzas):
            self.tbl_finanzas.insertRow(row_idx)
            self.tbl_finanzas.setItem(row_idx, 0, QTableWidgetItem(str(finanza["_id"])))
            self.tbl_finanzas.setItem(row_idx, 1, QTableWidgetItem(finanza["descripcion"]))
            self.tbl_finanzas.setItem(row_idx, 2, QTableWidgetItem(finanza["tipo"]))
            self.tbl_finanzas.setItem(row_idx, 3, QTableWidgetItem(f"{finanza['monto']:.2f}"))

    def add_finanza(self):
        descripcion, ok_desc = QInputDialog.getText(self, "Nueva Transacción", "Descripción:")
        if not ok_desc or not descripcion:
            return

        tipo, ok_tipo = QInputDialog.getItem(self, "Nueva Transacción", "Tipo:", ["Ingreso", "Egreso"], editable=False)
        if not ok_tipo:
            return

        monto, ok_monto = QInputDialog.getDouble(self, "Nueva Transacción", "Monto:", decimals=2)
        if not ok_monto:
            return

        responsable = "Usuario Actual"
        if add_finanza(descripcion, tipo, monto, responsable):
            QMessageBox.information(self, "Éxito", "Transacción registrada correctamente.")
            self.load_finanzas()

    def delete_finanza(self):
        selected_items = self.tbl_finanzas.selectedItems()
        if selected_items:
            finanza_id = selected_items[0].text()
            confirm = QMessageBox.question(self, "Confirmar", "¿Está seguro de que desea eliminar esta transacción?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                if delete_finanza(finanza_id):
                    QMessageBox.information(self, "Éxito", "Transacción eliminada.")
                    self.load_finanzas()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar la transacción.")
        else:
            QMessageBox.warning(self, "Error", "Seleccione una transacción para eliminar.")
