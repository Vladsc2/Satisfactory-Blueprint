from PySide6.QtWidgets import QWidget
from func.RW_subwidgets.RW_Blueprint import Blueprint

class CellForBlueprint(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.cell_blueprint = self
        super().__init__(parent)

        self.resize(parent.width(), parent.height() - 60)
        self.show()

        self.blueprint = Blueprint(GV, self)