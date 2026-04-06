from PySide6.QtWidgets import QWidget, QLabel, QPushButton
from PySide6.QtGui import QFont, QPainter, QPen
from PySide6.QtCore import Qt, QPoint
from func.Samples.Background import Background
from func.Samples.IButton import IButton
from GF.Constants import *
from func.LeftUnderFunctions.GroupScrollArea import GroupScrollArea

class GroupWidget(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(parent.width(),
                    parent.height())
        self.hide()
        background = Background("0, 255, 0", self)

        self.init_ui()

        self.scroll_area = GroupScrollArea(GV, self)


    def update_group_widget(self, group):
        all_voltage = 0
        counter_schemes = len(group)
        for scheme in group:
            voltage = scheme.object.energy
            voltage = get_voltage(voltage, scheme.count_batteries)
            all_voltage += voltage

        self.count_schemes_label.setText(str(counter_schemes))
        self.voltage_label.setText(f"{str(all_voltage)}МВт")
        self.count_schemes_label.adjustSize()
        self.voltage_label.adjustSize()

        self.createWidgetBtn.setChecked(False)
        for scheme in group:
            if scheme.createWidget:
                self.createWidgetBtn.setChecked(True)
                break


    def hide(self):
        self.GV.main_under_widget.factory_info_widget.update_factory_info_widget()
        super().hide()


    def set_schemes_create_widget_flag(self):
        flag = self.createWidgetBtn.isChecked()
        for scheme in self.GV.blueprint.selected_group:
            scheme.createWidget = flag

        self.GV.historyManager.notSave()
        self.GV.production_area.tick()


    def init_ui(self):
        self.createWidgetBtn = QPushButton("CW", self)
        self.createWidgetBtn.setFont(QFont("Arial", 16))
        self.createWidgetBtn.setCheckable(True)  # Делаем кнопку переключаемой
        self.createWidgetBtn.resize(50, 30)
        self.createWidgetBtn.move(self.width() - self.createWidgetBtn.width(), 0)
        self.createWidgetBtn.show()
        self.createWidgetBtn.clicked.connect(self.set_schemes_create_widget_flag)

        label = QLabel("Выделено схем: ", self)
        label.setFont(QFont("Arial", 16))
        label.adjustSize()
        label.move(10, 5)
        label.show()

        self.count_schemes_label = QLabel("2", self)
        self.count_schemes_label.setFont(QFont("Arial", 18))
        self.count_schemes_label.adjustSize()
        self.count_schemes_label.move(label.width() + 10 + 6, 4)
        self.count_schemes_label.show()

        label = QLabel("Потребление: ", self)
        label.setFont(QFont("Arial", 16))
        label.adjustSize()
        label.move(10, 30)
        label.show()

        self.voltage_label = QLabel("20 МВт", self)
        self.voltage_label.setFont(QFont("Arial", 19))
        self.voltage_label.adjustSize()
        self.voltage_label.move(label.width() + 10 + 6, 29)
        self.voltage_label.show()