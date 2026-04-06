from PySide6.QtWidgets import QWidget
from func.Samples.Background import Background

from func.LeftUnderFunctions.MainObjectWidget import MainObjectWidget

class UnderWidget(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(parent.width(),
                    parent.height() - 600 - 80)
        self.move(0, 80 + 600)
        self.show()
        background = Background("255, 99, 71", self)

        self.mainObjectWidget = MainObjectWidget(GV, self)