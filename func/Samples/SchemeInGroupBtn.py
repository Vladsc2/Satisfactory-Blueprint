from PySide6.QtWidgets import QPushButton, QLabel, QWidget
from PySide6.QtGui import QFont, QPixmap
from func.Samples.SchemeLabel import SchemeLabel

class SchemeInGroupBtn(QPushButton):
    def __init__(self, GV, parent: QWidget, scheme: SchemeLabel):
        self.GV = GV
        super().__init__(parent)
        self.scheme = scheme

        self.resize(parent.width() // 2, 50)
        self.show()

        self.init_ui()

        self.clicked.connect(self.select_scheme)


    def select_scheme(self):
        self.GV.blueprint.selected_group.clear()
        self.GV.blueprint.current_scheme = self.scheme
        self.GV.main_under_widget.selectScheme(self.scheme)


    def init_ui(self):
        font = QFont("Arial", 20)
        id_label = QLabel(f"id {self.scheme.id}", self)
        id_label.setFont(font)
        id_label.adjustSize()
        id_label.move(10, self.height() // 2 - id_label.height() // 2)
        id_label.show()

        image = QLabel(self)
        pixmap = QPixmap(self.scheme.object.image)
        image.resize(70, self.height() - 8)
        image.move(self.width() - image.width() - 10, 4)
        image.setPixmap(pixmap.scaled(image.size()))
        image.show()