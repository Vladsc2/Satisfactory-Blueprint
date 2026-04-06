from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtGui import QFont
from func.Samples.Background import Background

class CategoriesWidget(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.categories_widget = self
        super().__init__(parent)

        self.resize(parent.width(), parent.height() - 60)
        self.move(0, 60)
        self.show()
        background = Background("176, 196, 222", self)

        self.init_btns()


    def init_btns(self):
        self.btns = []

        btns_names = ["Изготовители", "Плавильни", "Буры", "Экстракторы", "Энергия", "Логистика", "Хранилища",
                        "Подсхемы"]
        argvs = ["#изготовители", "#плавильни", "#буры", "#экстракторы", "#энергия", "#логистика", "#хранилища",
                        "#custom"]

        btn_width = self.width()
        btn_height = self.height() // len(btns_names)

        offset_x = 0
        offset_y = 0

        for i in range(len(btns_names)):
            btn = QPushButton(btns_names[i], self)
            btn.setFont(QFont("Arial", 24))
            btn.resize(btn_width, btn_height)
            btn.move(offset_x, offset_y)
            btn.show()
            btn.clicked.connect(lambda clicked=False, index=i: self.search_category(argvs[index]))

            self.btns.append(btn)

            offset_y += btn_height


    def search_category(self, argvs):
        self.GV.search.lineEdit.setText(argvs)
        self.GV.search.lineEdit.deselect()