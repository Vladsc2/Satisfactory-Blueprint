from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QPushButton
from PySide6.QtGui import QFont, QPainter, QPen
from PySide6.QtCore import Qt, QPoint
from func.Samples.Background import Background
from func.Samples.IButton import IButton
from GF.Constants import *
from func.LeftUnderFunctions.GroupScrollArea import GroupScrollArea

class CommentWidget(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(parent.width(),
                    parent.height())
        self.hide()
        background = Background("215, 215, 215", self)

        self.init_ui_comments()

        self.comment = None


    def update_comment_info(self, comment):
        self.comment = comment

        self.btn_up_comment.setChecked(not comment.setLower)

        self.comment_text_le.setText(comment.text.text())

        self.text_layout_cb.setCurrentText(comment.text_layout)

        self.color_text_le.setText(comment.text_color)
        self.color_head_le.setText(comment.head_color)
        self.color_body_le.setText(comment.body_color)


    def update_comment_name(self):
        text = self.comment_text_le.text().strip()
        self.comment.text.setText(text)
        self.comment.text.adjustSize()


    def set_text_layout(self, text):
        self.comment.text_layout = text.strip()
        self.comment.set_pos_text_from_layout()
        self.GV.historyManager.notSave()


    def check_hex_color(self, text):
        text = text[1:]
        new_text = "#"
        for char in text:
            if char == " ":
                continue
            new_text += char
        if len(new_text) == 7:
            return new_text
        else:
            return "None"


    def check_text(self, text):
        if len(text) == 0:
            return "None"

        if text[0] == "#":
            return self.check_hex_color(text)
        elif text[:4] == "rgb(" and text[-1] == ")":
            return text
        elif text[:5] == "rgba(" and text[-1] == ")":
            return text
        else:
            return "None"


    def set_body_color(self):
        text = self.color_body_le.text().strip()
        text = self.check_text(text)
        if text == "None":
            return
        self.comment.body_color = text
        self.comment.update_style_sheet()
        self.GV.historyManager.notSave()


    def set_head_color(self):
        text = self.color_head_le.text().strip()
        text = self.check_text(text)
        if text == "None":
            return
        self.comment.head_color = text
        self.comment.update_style_sheet()
        self.GV.historyManager.notSave()

    def set_text_color(self):
        text = self.color_text_le.text().strip()
        text = self.check_text(text)
        if text == "None":
            return
        self.comment.text_color = text
        self.comment.update_style_sheet()
        self.GV.historyManager.notSave()


    def finishSetName(self):
        self.GV.historyManager.notSave()


    def set_comment_up_flag_state(self):
        self.comment.setLower = not self.btn_up_comment.isChecked()
        self.comment.set_Z_from_flag()
        self.GV.historyManager.notSave()


    def init_ui_comments(self):
        self.btn_up_comment = QPushButton("Up", self)
        self.btn_up_comment.setFont(QFont("Arial", 16))
        self.btn_up_comment.setCheckable(True)  # Делаем кнопку переключаемой
        self.btn_up_comment.resize(50, 30)
        self.btn_up_comment.move(self.width() - self.btn_up_comment.width(), 0)
        self.btn_up_comment.show()
        self.btn_up_comment.clicked.connect(self.set_comment_up_flag_state)

        self.comment_text_le = QLineEdit(self)
        self.comment_text_le.resize(self.width() - 86, 50)
        self.comment_text_le.move(self.width() // 2 - self.comment_text_le.width() // 2, 35)
        self.comment_text_le.setFont(QFont("Arial", 21))
        self.comment_text_le.setAlignment(Qt.AlignCenter)
        self.comment_text_le.show()
        self.comment_text_le.textChanged.connect(self.update_comment_name)
        self.comment_text_le.editingFinished.connect(self.finishSetName)

        self.text_layout_cb = QComboBox(self)
        self.text_layout_cb.setFont(QFont("Arial", 24))
        self.text_layout_cb.addItems(["left", "center", "right"])
        self.text_layout_cb.setStyleSheet("padding-left: 5px;")
        self.text_layout_cb.resize(120, 50)
        self.text_layout_cb.move(20, 100)
        self.text_layout_cb.show()
        self.text_layout_cb.currentTextChanged.connect(self.set_text_layout)

        label = QLabel("Расположение\n"
                       "  текста", self)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.show()
        label.move(self.text_layout_cb.pos().x() + self.text_layout_cb.width() + 20,
                   self.text_layout_cb.pos().y() - 5)


        font = QFont("Arial", 21)
        offset_y = 170
        distans = 20

        self.color_text_le = QLineEdit(self)
        self.color_text_le.resize(self.width() - 60, 50)
        self.color_text_le.move(self.width() // 2 - self.color_text_le.width() // 2, offset_y)
        self.color_text_le.setFont(font)
        self.color_text_le.setAlignment(Qt.AlignCenter)
        self.color_text_le.show()
        self.color_text_le.editingFinished.connect(self.set_text_color)

        offset_y += self.color_text_le.height() + distans

        self.color_head_le = QLineEdit(self)
        self.color_head_le.resize(self.width() - 60, 50)
        self.color_head_le.move(self.width() // 2 - self.color_head_le.width() // 2, offset_y)
        self.color_head_le.setFont(font)
        self.color_head_le.setAlignment(Qt.AlignCenter)
        self.color_head_le.show()
        self.color_head_le.editingFinished.connect(self.set_head_color)

        offset_y += self.color_head_le.height() + distans

        self.color_body_le = QLineEdit(self)
        self.color_body_le.resize(self.width() - 60, 50)
        self.color_body_le.move(self.width() // 2 - self.color_body_le.width() // 2, offset_y)
        self.color_body_le.setFont(font)
        self.color_body_le.setAlignment(Qt.AlignCenter)
        self.color_body_le.show()
        self.color_body_le.editingFinished.connect(self.set_body_color)