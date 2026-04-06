from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFileDialog
from PySide6.QtGui import QFont
from func.Samples.Background import Background
from PySide6.QtCore import Qt


class Widget_if_not_save(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(parent.size())
        self.hide()
        background = Background("255, 160, 122", self)

        self.init_UI_if_not_save()

    def start_save_as_widget(self):
        self.GV.project.hide()
        self.GV.project.show_widget_save_as(True)


    def not_save(self):
        self.GV.project.isSaved = True
        self.GV.exit_application()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.start_save_as_widget()
        elif event.key() == Qt.Key_Escape:
            self.GV.project.hide()
        elif event.key() == Qt.Key_Q or event.key() == Qt.Key_E:
            self.not_save()


    def init_UI_if_not_save(self):
        label = QLabel("Проект не сохранен", self)
        font = QFont("Arial", 30)
        label.setFont(font)
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2, 10)
        label.show()

        label = QLabel("Вы хотите сохранить проект?", self)
        font = QFont("Arial", 22)
        label.setFont(font)
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2, 50)
        label.show()

        btn = QPushButton("Отменить", self)
        font = QFont("Arial", 24)
        btn.setFont(font)
        btn.resize(200, 64)
        btn.move(20, self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.GV.project.hide)

        btn = QPushButton("Не сохранять", self)
        font = QFont("Arial", 22)
        btn.setFont(font)
        btn.resize(200, 64)
        btn.move(self.width()//2-btn.width()//2, self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.not_save)


        btn = QPushButton("Сохранить", self)
        font = QFont("Arial", 24)
        btn.setFont(font)
        btn.resize(200, 64)
        btn.move(self.width() - 20 - btn.width(), self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.start_save_as_widget)