from PySide6.QtWidgets import QWidget
from func.Samples.Background import Background
from func.ComponentsWidgets.Search import Search
from func.ComponentsWidgets.CategoriesWidget import CategoriesWidget
from func.ComponentsWidgets.ComponentsWidget import ComponentsWidget

class MainCWidget(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(parent.width(), 600)
        self.move(0, 80)
        self.show()
        background = Background("147, 112, 219", self)

        self.components_widget = ComponentsWidget(GV, self)

        self.categories_widget = CategoriesWidget(GV, self)

        self.search = Search(GV, self)