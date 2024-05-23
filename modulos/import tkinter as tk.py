import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox, QLineEdit, QMessageBox

class SistemaHotel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Hotel")
        self.setGeometry(100, 100, 500, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.btn_gestionar = QPushButton("Gestionar Habitaciones", self)
        self.btn_gestionar.clicked.connect(self.open_gestionar)
        self.layout.addWidget(self.btn_gestionar)

        self.central_widget.setLayout(self.layout)

    def open_gestionar(self):
        self.clearLayout(self.layout)

        self.lbl_titulo = QLabel("Gestión de Habitaciones", self)
        self.layout.addWidget(self.lbl_titulo)

        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.clicked.connect(self.open_main)
        self.layout.addWidget(self.btn_volver)

        self.btn_agregar = QPushButton("Agregar Habitación", self)
        self.btn_agregar.clicked.connect(self.open_agregar)
        self.layout.addWidget(self.btn_agregar)

        self.btn_eliminar = QPushButton("Eliminar Habitación", self)
        self.btn_eliminar.clicked.connect(self.open_eliminar)
        self.layout.addWidget(self.btn_eliminar)

    def open_agregar(self):
        self.clearLayout(self.layout)

        self.lbl_titulo = QLabel("Agregar Habitación", self)
        self.layout.addWidget(self.lbl_titulo)

        self.lbl_ocupantes = QLabel("Cantidad de ocupantes:", self)
        self.layout.addWidget(self.lbl_ocupantes)

        self.entry_ocupantes = QLineEdit(self)
        self.layout.addWidget(self.entry_ocupantes)

        self.lbl_orientacion = QLabel("Orientación:", self)
        self.layout.addWidget(self.lbl_orientacion)

        self.orientation_options = ["Norte", "Sur", "Este", "Oeste"]
        self.orientation_dropdown = QComboBox(self)
        self.orientation_dropdown.addItems(self.orientation_options)
        self.layout.addWidget(self.orientation_dropdown)

        self.btn_confirmar = QPushButton("Confirmar", self)
        self.btn_confirmar.clicked.connect(self.confirmar_agregar)
        self.layout.addWidget(self.btn_confirmar)

    def confirmar_agregar(self):
        ocupantes = self.entry_ocupantes.text()
        orientacion = self.orientation_dropdown.currentText()
        # Aquí puedes agregar la lógica para guardar la habitación en la base de datos o donde corresponda
        QMessageBox.information(self, "Confirmación", "Habitación agregada correctamente.")

    def open_eliminar(self):
        # Aquí puedes implementar la lógica para abrir la ventana de eliminar habitación
        pass

    def open_main(self):
        self.clearLayout(self.layout)
        self.open_gestionar()

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SistemaHotel()
    ventana.show()
    sys.exit(app.exec_())
