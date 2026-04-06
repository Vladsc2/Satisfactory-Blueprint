from func.Samples.IButton import IButton
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QFont

C_CREATORS = "creators"
C_SMELTERS = "smelters"
C_BOERS = "boers"
C_EXTRACTORS = "extractors"
C_ENERGY = "energy"
C_LOGISTICS = "logistics"
C_STORAGE = "storage"
C_CUSTOM = "custom"

class AddObjectBtn(IButton):
    def __init__(self, parent):
        super().__init__(parent)

        self.object = None

        self.name_label = QLabel(self)
        self.name_label.setFont(QFont("Arial", 20))
        self.name_label.show()

        self.scheme = QLabel(self)
        self.scheme.show()

        self.image = QLabel(self)
        self.image.show()

        self.hoverImage.raise_()

        self.setStyleSheet("")

        # Для реализации поиска
        self.name = ""
        self.category = ""
        self.energy = 0


    def set_dragging_size(self, width, height):
        self.dragging_width = width
        self.dragging_height = height


    def set_scheme_size(self, width, height):
        self.scheme_width = width
        self.scheme_height = height


    def set_energy(self, energy):
        self.energy = energy


    def set_category(self, category):
        self.category = category


    def set_name_scheme_image(self, name, scheme, image):
        self.name = name
        self.name_label.setText(name)
        self.name_label.adjustSize()
        self.name_label.move(5, self.height() // 2 - self.name_label.height() // 2)

        self.scheme.resize(self.width() // 5 + 10, self.height() - 20)
        self.scheme.move(self.width() - self.scheme.width()*2 - 20, 10)
        pixmap = QPixmap(scheme)
        self.scheme.setPixmap(pixmap.scaled(self.scheme.size()))

        self.image.resize(self.width() // 5 + 10, self.height() - 20)
        self.image.move(self.width() - self.image.width() - 10, 10)
        pixmap = QPixmap(image)
        self.image.setPixmap(pixmap.scaled(self.image.size()))


    def set_object(self, object):
        self.object = object