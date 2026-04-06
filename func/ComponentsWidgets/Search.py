from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import QSize
from func.Samples.Background import Background
from func.Samples.IButton import IButton
from GF.Constants import *

class Search(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.search = self
        super().__init__(parent)

        self.resize(parent.width(), 60)
        self.move(0, 0)
        self.show()
        background = Background("255, 140, 0", self)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.resize(self.size() + QSize(-10, -10))
        self.lineEdit.move(5, 5)
        self.lineEdit.setFont(QFont("Arial", 20))
        self.lineEdit.show()
        self.lineEdit.setStyleSheet("padding: 10px;")
        self.lineEdit.textChanged.connect(lambda l=self.lineEdit: self.finish_editing(l))

        self.clear_lineEdit_btn = IButton(self)
        self.clear_lineEdit_btn.resize(self.lineEdit.height() // 3 * 2,
                                  self.lineEdit.height() // 3 * 2)
        self.clear_lineEdit_btn.move(self.lineEdit.width() - self.clear_lineEdit_btn.width() - 1,
                                (self.lineEdit.height() // 3 * 2) // 2)
        self.clear_lineEdit_btn.setPathsToImages(r"assets/LWidget/ClearSearchBtn/close_btn.png",
                                            r"assets/LWidget/ClearSearchBtn/close_btn_pressed.png",
                                            r"assets/LWidget/ClearSearchBtn/hover.png")
        self.clear_lineEdit_btn.clicked.connect(self.GV.components_widget.click_clear_btn)
        self.clear_lineEdit_btn.hide()


    def finish_editing(self, text):
        self.GV.components_widget.search_from_text(text)