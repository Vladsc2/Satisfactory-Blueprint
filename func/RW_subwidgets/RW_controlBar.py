from PySide6.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from func.Samples.Background import Background

class RW_ControlBar(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.control_bar = self
        super().__init__(parent)

        self.resize(parent.width(), 60)
        self.move(0, parent.height() - self.height())
        self.show()
        background = Background("144, 238, 144", self)

        self.btns = []

        self.init_ui_control_bar()


    def changeLvl(self):
        text = self.lvl_line_edit.text()
        config = self.GV.config
        if not text.isdigit():
            self.lvl_line_edit.setText(str(config.current_lvl))
            return
        lvl = int(text)
        if lvl < 0:
            lvl = 0
        if lvl > 9:
            lvl = 9
        config.current_lvl = lvl
        self.lvl_line_edit.setText(str(config.current_lvl))



    def changeFlag(self, flag_name):
        if flag_name == "SC":
            self.GV.production_area.isSimpleCraft = not self.GV.production_area.isSimpleCraft
        elif flag_name == "PC":
            self.GV.production_area.isPrintCurrent = not self.GV.production_area.isPrintCurrent
        elif flag_name == "PT":
            self.GV.production_area.isPrintTypes = not self.GV.production_area.isPrintTypes
        elif flag_name == "PL":
            self.GV.production_area.isPrintLogistic = not self.GV.production_area.isPrintLogistic
        elif flag_name == "PTL":
            self.GV.production_area.isPrintTypesLogistic = not self.GV.production_area.isPrintTypesLogistic
        elif flag_name == "SH":
            self.GV.config.show_hotkeys = not self.GV.config.show_hotkeys
            self.GV.hotkeys.show_hide_from_config()
        self.GV.production_area.tick()


    def set_hz_images(self):
        hz = self.hz_mouse_image_line_edit.text()
        config = self.GV.config
        if not hz.isdigit():
            self.hz_mouse_image_line_edit.setText(str(config.hz_mouse_image))
            return
        hz = int(hz)
        if hz < 1:
            self.hz_mouse_image_line_edit.setText("1")
            hz = 1
        if hz > 1000:
            self.hz_mouse_image_line_edit.setText("1000")
            hz = 1000
        config.hz_mouse_image = hz
        self.GV.mouse_image.update_hz_mouse_image()
        self.GV.group_mouse_image.update_hz_group_image()


    def set_hz_conv_lines(self):
        hz = self.hz_conv_line_edit.text()
        config = self.GV.config
        if not hz.isdigit():
            self.hz_conv_line_edit.setText(str(config.hz_conv_lines))
            return
        hz = int(hz)
        if hz < 1:
            self.hz_conv_line_edit.setText("1")
            hz = 1
        if hz > 1000:
            self.hz_conv_line_edit.setText("1000")
            hz = 1000
        config.hz_conv_lines = hz
        self.GV.blueprint.paint_area.update_hz_lines()


    def changeBlueprintHeight(self):
        blueprint = self.GV.blueprint
        text = self.blueprint_height_line_edit.text()
        if len(text) < 2:
            self.blueprint_height_line_edit.setText(str(blueprint.height())+"px")
            return
        if text[-1] == "x" and text[-2] == "p":
            text = text[:-2]
        if not text.isdigit():
            self.blueprint_height_line_edit.setText(str(blueprint.height())+"px")
            return
        text = int(text)
        if text < 1080:
            self.blueprint_height_line_edit.setText("100px")
            text = 1080
        if text > 10000:
            self.blueprint_height_line_edit.setText("10000px")
            text = 10000
        self.GV.config.blueprint_height = text
        blueprint.update_size_from_config_and_zoom()
        self.blueprint_height_line_edit.setText(str(text)+"px")



    def changeBlueprintWidth(self):
        blueprint = self.GV.blueprint
        text = self.blueprint_width_line_edit.text()
        if len(text) < 2:
            self.blueprint_width_line_edit.setText(str(blueprint.width())+"px")
            return
        if text[-1] == "x" and text[-2] == "p":
            text = text[:-2]
        if not text.isdigit():
            self.blueprint_width_line_edit.setText(str(blueprint.width())+"px")
            return
        text = int(text)
        if text < 1920:
            self.blueprint_width_line_edit.setText("100px")
            text = 1920
        if text > 10000:
            self.blueprint_width_line_edit.setText("10000px")
            text = 10000
        self.GV.config.blueprint_width = text
        blueprint.update_size_from_config_and_zoom()
        self.blueprint_width_line_edit.setText(str(text)+"px")


    def init_ui_control_bar(self):
        # self.height() = 60
        offset_x = 10

        label = QLabel("Размер:", self)
        label.setFont(QFont("Arial", 18))
        label.adjustSize()
        label.move(offset_x, self.height() // 2 - label.height() // 2)
        label.show()

        offset_x += label.width() + 10

        blpr = self.GV.blueprint

        self.blueprint_width_line_edit = QLineEdit(self)
        self.blueprint_width_line_edit.resize(100, 34)
        self.blueprint_width_line_edit.move(offset_x, 13)
        self.blueprint_width_line_edit.setFont(QFont("Arial", 16))
        self.blueprint_width_line_edit.setAlignment(Qt.AlignCenter)
        self.blueprint_width_line_edit.show()
        self.blueprint_width_line_edit.editingFinished.connect(self.changeBlueprintWidth)

        offset_x += self.blueprint_width_line_edit.width() + 6

        label = QLabel("x", self)
        label.setFont(QFont("Arial", 24))
        label.adjustSize()
        label.move(offset_x, self.height() // 2 - label.height() // 2 - 3)
        label.show()

        offset_x += label.width() + 6

        self.blueprint_height_line_edit = QLineEdit(self)
        self.blueprint_height_line_edit.resize(100, 34)
        self.blueprint_height_line_edit.move(offset_x, 13)
        self.blueprint_height_line_edit.setFont(QFont("Arial", 16))
        self.blueprint_height_line_edit.setAlignment(Qt.AlignCenter)
        self.blueprint_height_line_edit.show()
        self.blueprint_height_line_edit.editingFinished.connect(self.changeBlueprintHeight)

        offset_x += self.blueprint_height_line_edit.width() + 30

        # Инициализируем LineEditы для выставления герцовки таймеров
        label = QLabel("Герцовка:", self)
        label.setFont(QFont("Arial", 18))
        label.adjustSize()
        label.move(offset_x, self.height() // 2 - label.height() // 2)
        label.show()

        offset_x += label.width() + 10

        config = self.GV.config

        self.hz_conv_line_edit = QLineEdit(str(config.hz_conv_lines), self)
        self.hz_conv_line_edit.resize(70, 34)
        self.hz_conv_line_edit.move(offset_x, 13)
        self.hz_conv_line_edit.setFont(QFont("Arial", 17))
        self.hz_conv_line_edit.setAlignment(Qt.AlignCenter)
        self.hz_conv_line_edit.show()
        self.hz_conv_line_edit.editingFinished.connect(self.set_hz_conv_lines)

        offset_x += self.hz_conv_line_edit.width() + 15

        self.hz_mouse_image_line_edit = QLineEdit(str(config.hz_mouse_image), self)
        self.hz_mouse_image_line_edit.resize(70, 34)
        self.hz_mouse_image_line_edit.move(offset_x, 13)
        self.hz_mouse_image_line_edit.setFont(QFont("Arial", 17))
        self.hz_mouse_image_line_edit.setAlignment(Qt.AlignCenter)
        self.hz_mouse_image_line_edit.show()
        self.hz_mouse_image_line_edit.editingFinished.connect(self.set_hz_images)

        offset_x += self.hz_mouse_image_line_edit.width() + 30

        # Инициализируем кнопки флагов
        label = QLabel("Флаги:", self)
        label.setFont(QFont("Arial", 18))
        label.adjustSize()
        label.move(offset_x, self.height() // 2 - label.height() // 2)
        label.show()

        offset_x += label.width() + 15

        btn = QPushButton("SC", self)
        btn.setFont(QFont("Arial", 16))
        btn.setCheckable(True)
        btn.setChecked(config.flag_simple_craft)
        btn.resize(60, 40)
        btn.move(offset_x, 10)
        btn.show()
        btn.clicked.connect(lambda clicked=False: self.changeFlag("SC"))
        self.btns.append(btn)

        offset_x += btn.width() + 5

        btn = QPushButton("PC", self)
        btn.setFont(QFont("Arial", 16))
        btn.setCheckable(True)
        btn.setChecked(config.flag_print_current)
        btn.resize(60, 40)
        btn.move(offset_x, 10)
        btn.show()
        btn.clicked.connect(lambda clicked=False: self.changeFlag("PC"))
        self.btns.append(btn)

        offset_x += btn.width() + 5

        btn = QPushButton("PT", self)
        btn.setFont(QFont("Arial", 16))
        btn.setCheckable(True)
        btn.setChecked(config.flag_print_types)
        btn.resize(60, 40)
        btn.move(offset_x, 10)
        btn.show()
        btn.clicked.connect(lambda clicked=False: self.changeFlag("PT"))
        self.btns.append(btn)

        offset_x += btn.width() + 5

        btn = QPushButton("PL", self)
        btn.setFont(QFont("Arial", 16))
        btn.setCheckable(True)
        btn.setChecked(config.flag_print_logistics)
        btn.resize(60, 40)
        btn.move(offset_x, 10)
        btn.show()
        btn.clicked.connect(lambda clicked=False: self.changeFlag("PL"))
        self.btns.append(btn)

        offset_x += btn.width() + 5

        btn = QPushButton("PTL", self)
        btn.setFont(QFont("Arial", 16))
        btn.setCheckable(True)
        btn.setChecked(config.flag_print_types_logistics)
        btn.resize(60, 40)
        btn.move(offset_x, 10)
        btn.show()
        btn.clicked.connect(lambda clicked=False: self.changeFlag("PTL"))
        self.btns.append(btn)

        offset_x += btn.width() + 10

        btn = QPushButton("SH", self)
        btn.setFont(QFont("Arial", 16))
        btn.setCheckable(True)
        btn.setChecked(config.show_hotkeys)
        btn.resize(60, 40)
        btn.move(offset_x, 10)
        btn.show()
        btn.clicked.connect(lambda clicked=False: self.changeFlag("SH"))
        self.btns.append(btn)

        offset_x += btn.width() + 25

        # Инициализируем LineEdit для уровня
        label = QLabel("Ур:", self)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.move(offset_x, self.height() // 2 - label.height() // 2)
        label.show()

        offset_x += label.width() + 10

        self.lvl_line_edit = QLineEdit(str(config.current_lvl), self)
        self.lvl_line_edit.resize(80, 34)
        self.lvl_line_edit.move(offset_x, 13)
        self.lvl_line_edit.setFont(QFont("Arial", 20))
        self.lvl_line_edit.setAlignment(Qt.AlignCenter)
        self.lvl_line_edit.show()
        self.lvl_line_edit.editingFinished.connect(self.changeLvl)

        offset_x += self.lvl_line_edit.width() + 40

        # Инициализируем кнопки и текст масштаба
        btn = QPushButton("–", self)
        btn.setFont(QFont("Arial", 27))
        btn.resize(40, 34)
        btn.move(offset_x, 13)
        btn.show()
        btn.clicked.connect(self.GV.scale.zoom_out)

        offset_x += btn.width()

        btn = QPushButton("+", self)
        btn.setFont(QFont("Arial", 27))
        btn.resize(40, 34)
        btn.move(offset_x, 13)
        btn.show()
        btn.clicked.connect(self.GV.scale.zoom_in)

        offset_x += btn.width() + 10

        self.current_scale_label = QLabel("100%", self)
        self.current_scale_label.setFont(QFont("Arial", 20))
        self.current_scale_label.adjustSize()
        self.current_scale_label.move(offset_x, self.height() // 2 - self.current_scale_label.height() // 2)
        self.current_scale_label.show()