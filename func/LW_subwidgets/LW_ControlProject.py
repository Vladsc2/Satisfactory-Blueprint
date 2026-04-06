from PySide6.QtWidgets import QWidget
from func.Samples.Background import Background
from func.Samples.IButton import IButton
from PySide6.QtCore import Qt

class ControlProject(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.control_project = self
        super().__init__(parent)

        self.resize(parent.width(), 80)
        self.show()
        background = Background("32, 178, 170", self)

        self.btns = []
        # self.init_btns()


    def check_control_projects_hotkeys(self, event):
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_N:
            print("Функция создания нового проекта")
            self.GV.widget_new_project.create_new_project()

        elif event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_R:
            print("Вызов функции загрузки")
            self.GV.project.show_widget_load_project()

        elif event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_S:
            print("Вызов функции сохранения")
            self.GV.project.show_widget_save_as()

        elif event.key() == Qt.Key_T:
            print("Вызов функции сохранение как схемы")
            self.GV.project.show_widget_save_as_scheme()

        elif event.key() == Qt.Key_Q:
            self.start_del_input_logistic()
        elif event.key() == Qt.Key_E:
            self.start_del_output_logistic()



    def init_btns(self):
        standard_images = [ r"assets/LWidget/New_project/icon.png",
                            r"assets/LWidget/00 LoadProject/icon.png",
                            r"assets/LWidget/01 Save as/icon.png",
                            r"assets/LWidget/02 Save as scheme/icon.png",
                            r"assets/LWidget/DelLogisticInBtn/delBtn.png",
                            r"assets/LWidget/DelLogisticOutBtn/delBtn.png"]

        pressed_images = [  r"assets/LWidget/New_project/icon_pressed.png",
                            r"assets/LWidget/00 LoadProject/icon_pressed.png",
                            r"assets/LWidget/01 Save as/icon_pressed.png",
                            r"assets/LWidget/02 Save as scheme/icon_pressed.png",
                            r"assets/LWidget/DelLogisticInBtn/delBtn_pressed.png",
                            r"assets/LWidget/DelLogisticOutBtn/delBtn_pressed.png"]

        hover_images = [    r"assets/LWidget/New_project/hover.png",
                            r"assets/LWidget/00 LoadProject/hover.png",
                            r"assets/LWidget/01 Save as/hover.png",
                            r"assets/LWidget/02 Save as scheme/hover.png",
                            r"assets/LWidget/DelLogisticInBtn/hover.png",
                            r"assets/LWidget/DelLogisticOutBtn/hover.png"]
        functions = [   self.GV.widget_new_project.create_new_project,
                        self.GV.project.show_widget_load_project,
                        self.GV.project.show_widget_save_as,
                        self.GV.project.show_widget_save_as_scheme,
                        self.start_del_input_logistic,
                        self.start_del_output_logistic]

        tooltips = [    "Создать новый проект (Ctrl+N)",
                        "Загрузить проект (Ctrl+R)",
                        "Сохранить проект (Ctrl+S)",
                        "Сохранить как схему (T)",
                        "Удаляет все input конвейеры у выбранного объекта (Q)",
                        "Удаляет все output конвейеры у выбранного объекта (E)"]

        border_x = 5
        border_y = 10
        distans_x = 8

        btn_width = ( (self.width() - border_x*2) // len(standard_images) ) - distans_x + 1
        btn_height = self.height() - border_y*2

        offset_x = border_x

        for i in range(len(standard_images)):
            btn = IButton(self)
            btn.resize(btn_width, btn_height)
            btn.move(offset_x, border_y)
            btn.setPathsToImages(standard_images[i], pressed_images[i], hover_images[i])
            btn.clicked.connect(functions[i])

            self.btns.append(btn)

            offset_x += btn.width() + distans_x

            if tooltips[i] is None or tooltips[i] == "":
                continue

            btn.setTooltip(tooltips[i])

        for btn in self.btns:
            btn.tooltipWidget.raise_()


    def start_del_input_logistic(self):
        self.GV.window.change_cursor_to_del_logistic_input(not self.GV.window.isDelLogisticCursorIn)


    def start_del_output_logistic(self):
        self.GV.window.change_cursor_to_del_logistic(not self.GV.window.isDelLogisticCursor)