from PySide6.QtWidgets import QWidget
from func.Samples.Background import Background
from GF.Constants import *
from func.LW_subwidgets.LW_ControlProject import ControlProject
from func.ComponentsWidgets.MainCWidget import MainCWidget
from func.LeftUnderFunctions.UnderWidget import UnderWidget

class LeftWidget(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.lw = self
        super().__init__(parent)

        self.resize(400, MONITOR_HEIGHT)
        self.show()
        background = Background("255, 160, 122", self)

        self.control_projects = ControlProject(GV, self)

        self.components_widget = MainCWidget(GV, self)

        self.under_widget = UnderWidget(GV, self)