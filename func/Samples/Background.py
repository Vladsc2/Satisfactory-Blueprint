from PySide6.QtWidgets import QLabel

class Background(QLabel):
    def __init__(self, color_rgb, parent):
        super().__init__(parent)

        self.resize(parent.size())
        self.setStyleSheet(f"background-color: rgb({color_rgb});")
        self.show()