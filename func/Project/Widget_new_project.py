from PySide6.QtWidgets import QWidget, QLabel, QPushButton
from PySide6.QtGui import QFont
from func.Samples.Background import Background
from decimal import Decimal
from GF.GlobalVariables import GlobalVariables
from PySide6.QtCore import Qt


class Widget_new_project(QWidget):
    def __init__(self, GV: GlobalVariables, parent):
        self.GV = GV
        GV.widget_new_project = self
        super().__init__(parent)

        self.resize(parent.size())
        self.hide()
        background = Background("219, 112, 147", self)

        self.init_UI_if_not_save()


    def create_new_project(self):
        project = self.GV.project
        if not project.isSaved:
            project.show_widget_new_project()
            return

        project.name = "Завод"

        for scheme in self.GV.blueprint.schemes:
            scheme.deleteLater()
        self.GV.blueprint.schemes.clear()
        for comm in self.GV.blueprint.comments:
            comm.deleteLater()
        self.GV.blueprint.comments.clear()

        self.GV.config.load_config()

        blueprint = self.GV.blueprint
        config = self.GV.config
        control_bar = self.GV.control_bar

        # Обновляем зум
        self.GV.scale.current_scale_percent = Decimal("100")
        self.GV.scale.k = Decimal("1")
        control_bar.current_scale_label.setText(str(self.GV.scale.current_scale_percent)+"%")
        control_bar.current_scale_label.adjustSize()

        # Обновляем размер blueprint
        control_bar.blueprint_width_line_edit.setText(str(config.blueprint_width)+"px")
        control_bar.blueprint_height_line_edit.setText(str(config.blueprint_height)+"px")
        blueprint.update_size_from_config_and_zoom()
        blueprint.move(0 - blueprint.width() // 2 + blueprint.parent.width() // 2,
                       0 - blueprint.height() // 2 + blueprint.parent.height() // 2)

        # Обновляем герцовку
        control_bar.hz_conv_line_edit.setText(str(config.hz_conv_lines))
        control_bar.hz_mouse_image_line_edit.setText(str(config.hz_mouse_image))
        blueprint.paint_area.update_hz_lines()
        self.GV.mouse_image.update_hz_mouse_image()
        self.GV.group_mouse_image.update_hz_group_image()

        # Обновляем флаги
        production_area = self.GV.production_area
        flags = [config.flag_simple_craft, config.flag_print_current, config.flag_print_types,
                 config.flag_print_logistics, config.flag_print_types_logistics, config.show_hotkeys]
        names_flags = []
        i = 0
        for btn in control_bar.btns:
            btn.setChecked(flags[i])
            i += 1
        production_area.isSimpleCraft = flags[0]
        production_area.isPrintCurrent = flags[1]
        production_area.isPrintTypes = flags[2]
        production_area.isPrintLogistic = flags[3]
        production_area.isPrintTypesLogistic = flags[4]
        self.GV.hotkeys.show_hide_from_config()

        # Обновляем уровень
        control_bar.lvl_line_edit.setText(str(config.current_lvl))

        # Чтобы удалить неактуальные виджеты подсказок
        self.GV.production_area.tick()

        # Очищаем undo-redo
        self.GV.historyManager.clear_arrays()

        blueprint.free_index_object = 0


    def start_save_as_widget(self):
        self.GV.project.hide()
        self.GV.project.show_widget_save_as(isNewProjectSave=True)


    def not_save(self):
        self.GV.project.hide()
        self.GV.project.isSaved = True
        self.create_new_project()


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

        label = QLabel("Вы хотите сохранить проект перед созданием нового?", self)
        font = QFont("Arial", 20)
        label.setFont(font)
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2, 54)
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