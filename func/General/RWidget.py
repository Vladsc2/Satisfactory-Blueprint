from PySide6.QtWidgets import QWidget
from func.Samples.Background import Background
from func.Samples.IButton import IButton
from GF.Constants import *
from func.RW_subwidgets.RW_controlBar import RW_ControlBar
from func.RW_subwidgets.RW_blueprint_cell import CellForBlueprint

class RightWidget(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.rw = self
        super().__init__(parent)

        self.resize(MONITOR_WIDTH-parent.left_widget.width(), MONITOR_HEIGHT)
        self.move(parent.left_widget.width(), 0)
        self.show()
        background = Background("70, 130, 180", self)

        self.control_bar = RW_ControlBar(GV, self)

        self.blueprint = CellForBlueprint(GV, self)


        self.init_btns()


    def init_btns(self):
        closeBtn = IButton(self)
        closeBtn.resize(60, 60)
        closeBtn.move(self.width() - closeBtn.width(), 0)
        closeBtn.setPathsToImages(r"assets/RWidget/closeBtn.png",
                                  r"assets/RWidget/closeBtn_pressed.png",
                                  r"assets/RWidget/closeBtn_hover.png")
        closeBtn.clicked.connect(self.GV.exit_application)