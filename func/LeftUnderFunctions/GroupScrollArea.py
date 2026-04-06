from PySide6.QtWidgets import QWidget, QLabel, QScrollArea
from PySide6.QtGui import QFont, QPainter, QPen
from PySide6.QtCore import Qt, QPoint, QSize
from func.Samples.Background import Background
from func.Samples.IButton import IButton
from GF.Constants import *
from func.Samples.SchemeInGroupBtn import SchemeInGroupBtn

class GroupScrollArea(QScrollArea):
    def __init__(self, GV, parent: QWidget):
        self.GV = GV
        GV.schemes_group_scroll_area = self
        super().__init__(parent)

        self.resize(parent.width(),
                    parent.height() - 65)
        self.move(0, parent.height() - self.height())
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)  # Обработка событий мыши
        self.show()


        self.contentWidget = QWidget()
        self.contentWidget.resize(self.size() + QSize(-19, 0))
        self.contentWidget.show()

        self.setWidget(self.contentWidget)

        self.btns = []


    def set_schemes_btns(self, group):
        for btn in self.btns:
            btn.deleteLater()
        self.btns.clear()

        offset_x = 0
        offset_y = 0
        btn_height = 46
        isRight = False
        for scheme in group:
            btn = SchemeInGroupBtn(self.GV, self.contentWidget, scheme)
            btn.move(offset_x, offset_y)
            self.btns.append(btn)

            if isRight:
                offset_x = 0
                offset_y += btn.height()
            else:
                offset_x = btn.width()

            isRight = not isRight

        self.contentWidget.resize(self.contentWidget.width(),
                                  offset_y + btn_height + 20)