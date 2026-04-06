from PySide6.QtWidgets import QWidget, QLabel, QPushButton
from PySide6.QtGui import QFont, QPainter, QPen
from PySide6.QtCore import Qt, QPoint, QTimer
from func.Samples.Background import Background
from func.Samples.IButton import IButton
from GF.Constants import *
from func.Samples.RecipeBtn import RecipeBtn
from func.Samples.SchemeLabel import SchemeLabel

class ObjectInfoWidget(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(parent.width(),
                    parent.height())
        self.show()
        background = Background("255, 140, 0", self)

        self.current_scheme = None

        self.font_1 = QFont("Arial", 36)
        self.font_2 = QFont("Arial", 30)
        self.font_3 = QFont("Arial", 24)
        self.font_4 = QFont("Arial", 18)
        self.font_5 = QFont("Arial", 12)

        self.init_UI()

        # Исправление супер странного бага, из-за которого ломается картинка
        self.timer = QTimer(self)
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.self_show)
        self.timer.start()


    def self_show(self):
        self.timer.stop()
        self.hide()


    def start_choice_recipe(self):
        self.GV.production_area.tick()
        scheme = self.recipe_btn.scheme
        if len(scheme.object.recipes) == 1:
            return
        self.recipe_btn.scheme = None
        self.recipe_btn.object = None
        self.recipe_btn.index_recipe = None
        self.GV.main_under_widget.selectRecipes(scheme)


    def update_voltage_label(self):
        standard_voltage = self.current_scheme.object.energy
        voltage = get_voltage(standard_voltage, self.current_scheme.count_batteries)

        self.voltage_label.setText(str(voltage) + "МВт")
        self.voltage_label.adjustSize()


    def set_font_name_label(self):
        self.name_label.setFont(self.font_1)
        self.name_label.adjustSize()

        if not self.name_label.width() > self.width() // 3 * 2:
            return

        self.name_label.setFont(self.font_2)
        self.name_label.adjustSize()

        if not self.name_label.width() > self.width() // 3 * 2:
            return

        self.name_label.setFont(self.font_3)
        self.name_label.adjustSize()

        if not self.name_label.width() > self.width() // 3 * 2:
            return

        self.name_label.setFont(self.font_4)
        self.name_label.adjustSize()

        if not self.name_label.width() > self.width() // 3 * 2:
            return

        self.name_label.setFont(self.font_5)
        self.name_label.adjustSize()



    def update_object_info_widget(self, scheme: SchemeLabel):
        self.current_scheme = scheme

        name = scheme.object.name + " #" + str(scheme.id)
        self.name_label.setText(name)
        self.set_font_name_label()
        self.name_label.move(self.width() // 2 - self.name_label.width() // 2, self.name_label.pos().y())

        self.update_voltage_label()

        self.count_battery_label.setText(str(scheme.count_batteries))

        self.createWidgetBtn.setChecked(scheme.createWidget)

        self.recipe_btn.set_recipe(scheme, scheme.current_recipe_index)
        self.recipe_btn.forming_ui()
        if len(scheme.object.recipes) == 0:
            self.recipe_btn.hide()
        else:
            self.recipe_btn.show()



    def sub_power_shard(self):
        count = int(self.count_battery_label.text())
        if count == 0:
            return
        count -= 1
        self.count_battery_label.setText(str(count))
        self.current_scheme.count_batteries = count
        self.update_voltage_label()
        self.GV.production_area.tick()


    def add_power_shard(self):
        count = int(self.count_battery_label.text())
        if count == 3:
            return
        count += 1
        self.count_battery_label.setText(str(count))
        self.current_scheme.count_batteries = count
        self.update_voltage_label()
        self.GV.production_area.tick()


    def hide(self):
        self.GV.main_under_widget.factory_info_widget.update_factory_info_widget()
        super().hide()


    def set_scheme_create_widget_flag(self):
        if self.current_scheme is None:
            return
        self.current_scheme.createWidget = self.createWidgetBtn.isChecked()
        self.GV.historyManager.notSave()
        self.GV.production_area.tick()


    def init_UI(self):
        self.createWidgetBtn = QPushButton("CW", self)
        self.createWidgetBtn.setFont(QFont("Arial", 16))
        self.createWidgetBtn.setCheckable(True)  # Делаем кнопку переключаемой
        self.createWidgetBtn.resize(50, 30)
        self.createWidgetBtn.move(self.width() - self.createWidgetBtn.width(), 0)
        self.createWidgetBtn.show()
        self.createWidgetBtn.clicked.connect(self.set_scheme_create_widget_flag)

        self.name_label = QLabel("Текст имени", self)
        self.name_label.setFont(self.font_1)
        self.name_label.adjustSize()
        self.name_label.move(self.width() // 2 - self.name_label.width() // 2, 20)
        self.name_label.show()

        label = QLabel("Потребление:", self)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.move(20, 100)
        label.show()

        self.voltage_label = QLabel("0МВт", self)
        self.voltage_label.setFont(QFont("Arial", 24))
        self.voltage_label.adjustSize()
        self.voltage_label.move(20 + label.width() + 6, 98)
        self.voltage_label.show()

        # Кол-во батарей
        label = QLabel("Батареи:", self)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.move(20, 140)
        label.show()

        btn = IButton(self)
        btn.resize(30, 30)
        btn.move(20 + label.width() + 10, 140)
        btn.setPathsToImages(r"assets/LWidget/Plus_Minus_count_battery/minus.png",
                             r"assets/LWidget/Plus_Minus_count_battery/minus_pressed.png",
                             r"assets/LWidget/Plus_Minus_count_battery/hover.png")
        btn.clicked.connect(self.sub_power_shard)

        self.count_battery_label = QLabel("0", self)
        self.count_battery_label.setFont(QFont("Arial", 24))
        self.count_battery_label.adjustSize()
        self.count_battery_label.move(20 + label.width() + 10 + btn.width() + 10, 138)
        self.count_battery_label.show()

        btn = IButton(self)
        btn.resize(30, 30)
        btn.move(20 + label.width() + 10 + btn.width() + 10 + self.count_battery_label.width() + 10,
                 140)
        btn.setPathsToImages(r"assets/LWidget/Plus_Minus_count_battery/plus.png",
                             r"assets/LWidget/Plus_Minus_count_battery/plus_pressed.png",
                             r"assets/LWidget/Plus_Minus_count_battery/hover.png")
        btn.clicked.connect(self.add_power_shard)

        # Рецепт
        label = QLabel("Установленный рецепт", self)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2, 190)
        label.show()

        self.recipe_btn = RecipeBtn(self.GV, self)
        self.recipe_btn.resize(self.width() - 40, 110)
        self.recipe_btn.move(20, 225)
        self.recipe_btn.clicked.connect(self.start_choice_recipe)