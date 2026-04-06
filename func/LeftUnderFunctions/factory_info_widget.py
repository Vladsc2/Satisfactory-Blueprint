from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import QTimer, Qt
from func.Samples.Background import Background
from func.Samples.IButton import IButton
from GF.Constants import *

class FactoryInfoWidget(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(parent.width(),
                    parent.height())
        self.show()
        background = Background("255, 140, 0", self)

        type_font = "Arial"
        self.font_1 = QFont(type_font, 36)
        self.font_2 = QFont(type_font, 30)
        self.font_3 = QFont(type_font, 25)
        self.font_4 = QFont(type_font, 20)
        self.font_5 = QFont(type_font, 14)

        self.init_change_project_widget()

        self.init_UI()

        self.counter = 0

        self.change_name_widget.raise_()
        self.change_name_widget.hide()

        self.images = []


    def set_name_project_label_font(self):
        limit = self.width() // 3 * 2

        self.name_project_label.setFont(self.font_1)
        self.name_project_label.adjustSize()
        if self.name_project_label.width() < limit:
            return
        self.name_project_label.setFont(self.font_2)
        self.name_project_label.adjustSize()
        if self.name_project_label.width() < limit:
            return
        self.name_project_label.setFont(self.font_3)
        self.name_project_label.adjustSize()
        if self.name_project_label.width() < limit:
            return
        self.name_project_label.setFont(self.font_4)
        self.name_project_label.adjustSize()
        if self.name_project_label.width() < limit:
            return
        self.name_project_label.setFont(self.font_5)
        self.name_project_label.adjustSize()



    def update_factory_info_widget(self):
        if self.counter < 3:
            self.counter += 1
            return

        project_name = self.GV.project.name
        self.name_project_label.setText(project_name)
        self.set_name_project_label_font()
        self.name_project_label.move(self.width() // 2 - self.name_project_label.width() // 2, 20)

        all_voltage = 0
        for scheme in self.GV.blueprint.schemes:
            voltage = scheme.object.energy
            voltage = get_voltage(voltage, scheme.count_batteries)
            all_voltage += voltage

        self.voltage_label.setText(f"{str(all_voltage)}МВт")
        self.voltage_label.adjustSize()

        # Так же обновляем подвиджет
        self.project_name_line_edit.setText(self.GV.project.name)

        # Удаляем старые картинки
        for image in self.images:
            image.deleteLater()
        self.images.clear()

        # Рисуем сколько заводу нужно ресурсов в минуту
        self.create_input_images()

        # Рисуем сколько всего производит схема в минуту
        self.create_output_images()


    def create_input_images(self):
        self.input_count_label.setText("")
        self.input_count_label2.setText("")

        # Считаем инпуты
        input_types = []
        input_counts = []
        for scheme in self.GV.blueprint.schemes:
            if not( (len(scheme.input_schemes) == 0 and len(scheme.input_schemes_liquid) == 0) ):
                continue
            if scheme.current_recipe_index is None:
                continue
            r_index = scheme.current_recipe_index
            recipe = scheme.object.recipes[r_index]

            for res_type in recipe.types_input_list:
                input_types.append(res_type)
            for res_count in recipe.count_input_list:
                res_count = res_count + (Decimal(res_count)/100 * (scheme.count_batteries * 50))
                input_counts.append(res_count)

        for scheme in self.GV.blueprint.schemes:
            if not (scheme.object.category == "boers" or scheme.object.category == "extractors"):
                continue
            if scheme.current_recipe_index is None:
                continue

            r_index = scheme.current_recipe_index
            recipe = scheme.object.recipes[r_index]

            for res_type in recipe.types_output_list:
                input_types.append(res_type)
            for res_count in recipe.count_output_list:
                input_counts.append(res_count)


        # Объединяем одинаковые ресурсы
        new_types = []
        new_counts = []
        for i in range(len(input_types)):

            current_type = input_types[i]

            if current_type in new_types:
                continue

            new_types.append(current_type)
            new_counts.append(input_counts[i])

            for j in range(i+1, len(input_types)):
                if input_types[i] == input_types[j]:
                    new_counts[-1] += input_counts[j]
        input_types = new_types[:]
        input_counts = new_counts[:]

        # Рисуем инпуты
        offset_x = 0
        offset_y = 240
        btnW = 40
        btnH = 40
        s = ""
        s2 = ""
        for i in range(len(input_types)):
            res = input_types[i]
            count = input_counts[i]

            count = Decimal(count).normalize()

            if i < 4:
                s += str(format(count, "f"))
                for j in range(7):
                    s += " "
                self.input_count_label.setText(s)
                self.input_count_label.adjustSize()
            else:
                s2 += str(format(count, "f"))
                for j in range(7):
                    s2 += " "
                self.input_count_label2.setText(s2)
                self.input_count_label2.adjustSize()

            if i < 4:
                image = QLabel(self.input_widget)
                image.move(offset_x + self.input_count_label.width() - 50, self.input_count_label.pos().y()-4)
            else:
                image = QLabel(self.input_widget2)
                image.move(offset_x + self.input_count_label2.width() - 50, self.input_count_label2.pos().y()-4)

            image.resize(btnW, btnH)
            image.show()
            pixmap = QPixmap(res.image)
            image.setPixmap(pixmap.scaled(image.size()))

            self.images.append(image)

        self.input_widget.resize(self.input_count_label.width(), 60)
        self.input_widget2.resize(self.input_count_label2.width(), 60)

        self.input_widget.move(self.width() // 2 - self.input_widget.width() // 2, 150)
        self.input_widget2.move(self.width() // 2 - self.input_widget2.width() // 2, 200)


    def create_output_images(self):
        self.output_count_label.setText("")
        self.output_count_label2.setText("")


        # Считаем вывод со схемы
        output_types = []
        output_counts = []
        for scheme in self.GV.blueprint.schemes:
            if scheme.object.category == "logistics":
                continue

            if len(scheme.output_schemes) > 0 or len(scheme.output_schemes_liquid) > 0:
                continue

            for res_type in scheme.types_resources_output:
                output_types.append(res_type)
            for res_count in scheme.count_resources_output:
                output_counts.append(res_count)

            for res_type in scheme.types_resources_output_liquid:
                output_types.append(res_type)
            for res_count in scheme.count_resources_output_liquid:
                output_counts.append(res_count)


        # Объединяем одинаковые ресурсы
        new_types = []
        new_counts = []
        for i in range(len(output_types)):

            current_type = output_types[i]

            if current_type in new_types:
                continue

            new_types.append(current_type)
            new_counts.append(output_counts[i])

            for j in range(i+1, len(output_types)):
                if output_types[i] == output_types[j]:
                    new_counts[-1] += output_counts[j]
        output_types = new_types[:]
        output_counts = new_counts[:]


        # Рисуем оутпуты
        offset_x = 0
        offset_y = 240
        btnW = 40
        btnH = 40
        s = ""
        s2 = ""
        for i in range(len(output_types)):
            res = output_types[i]
            count = output_counts[i]

            count = Decimal(count).normalize()

            if i < 4:
                s += str(format(count, "f"))
                for j in range(7):
                    s += " "
                self.output_count_label.setText(s)
                self.output_count_label.adjustSize()
            else:
                s2 += str(format(count, "f"))
                for j in range(7):
                    s2 += " "
                self.output_count_label2.setText(s2)
                self.output_count_label2.adjustSize()


            if i < 4:
                image = QLabel(self.output_widget)
                image.move(offset_x + self.output_count_label.width() - 50, self.output_count_label.pos().y()-4)
            else:
                image = QLabel(self.output_widget2)
                image.move(offset_x + self.output_count_label2.width() - 50, self.output_count_label2.pos().y()-4)



            image.resize(btnW, btnH)
            image.show()
            pixmap = QPixmap(res.image)
            image.setPixmap(pixmap.scaled(image.size()))

            self.images.append(image)

        self.output_widget.resize(self.output_count_label.width(), 60)
        self.output_widget2.resize(self.output_count_label2.width(), 60)

        self.output_widget.move(self.width() // 2 - self.output_widget.width() // 2, 280)
        self.output_widget2.move(self.width() // 2 - self.output_widget2.width() // 2, 335)



    def check_valid_text(self, text):
        wrong_symbols = r'<>:"/\\|?*'
        for char in text:
            if char in wrong_symbols:
                return False
        return True

    def change_project_name(self):
        text = self.project_name_line_edit.text().strip()

        if text == "":
            name = self.GV.project.name
            self.project_name_line_edit.setText(name)
            return

        valid = self.check_valid_text(text)
        if not valid:
            name = self.GV.project.name
            self.project_name_line_edit.setText(name)
            return

        self.project_name_line_edit.setText(text)
        self.GV.project.name = text


    def hide_subwidgets_and_update(self):
        self.change_name_widget.hide()
        self.update_factory_info_widget()


    def init_change_project_widget(self):
        self.change_name_widget = QWidget(self)
        self.change_name_widget.resize(self.size())
        self.change_name_widget.show()
        back = Background("255, 140, 0", self.change_name_widget)

        back_btn = IButton(self.change_name_widget)
        back_btn.setPathsToImages(r"assets\LWidget\Back_btn\image.jpg",
                                  r"assets\LWidget\Back_btn\image_pressed.jpg",
                                  r"assets\LWidget\Back_btn\hover.png")
        back_btn.resize(100, 40)
        back_btn.move(10, 10)
        back_btn.show()
        back_btn.clicked.connect(self.hide_subwidgets_and_update)

        label = QLabel("Имя проекта", self.change_name_widget)
        label.setFont(QFont("Arial", 30))
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2, 90)
        label.show()

        self.project_name_line_edit = QLineEdit("Завод", self.change_name_widget)
        self.project_name_line_edit.resize(self.width() - 40, 60)
        self.project_name_line_edit.move(self.width() // 2 - self.project_name_line_edit.width() // 2, 100 + 50)
        self.project_name_line_edit.setFont(QFont("Arial", 26))
        self.project_name_line_edit.setAlignment(Qt.AlignCenter)
        self.project_name_line_edit.show()
        self.project_name_line_edit.editingFinished.connect(self.change_project_name)



    def init_UI(self):
        self.name_project_label = QLabel("Завод", self)
        self.name_project_label.setFont(self.font_1)
        self.name_project_label.adjustSize()
        self.name_project_label.move(self.width() // 2 - self.name_project_label.width() // 2, 20)
        self.name_project_label.show()

        btn = IButton(self)
        btn.setFont(QFont("Arial", 20))
        btn.resize(40, 40)
        btn.move(self.width() - btn.width(), 0)
        btn.setPathsToImages(r"assets\LWidget\Edit_name_project_btn\icon.png",
                             r"assets\LWidget\Edit_name_project_btn\icon_pressed.png",
                             r"assets\LWidget\Edit_name_project_btn\hover.png")
        btn.show()
        btn.clicked.connect(self.change_name_widget.show)

        offset_x = 10

        label = QLabel("Потребление:", self)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.move(offset_x, 80)
        label.show()

        self.voltage_label = QLabel("0МВт", self)
        self.voltage_label.setFont(QFont("Arial", 24))
        self.voltage_label.adjustSize()
        self.voltage_label.move(offset_x + label.width() + 8, 78)
        self.voltage_label.show()

        label = QLabel("Потребление ресурсов", self)
        label.setFont(QFont("Arial", 22))
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2 - 10, 120)
        label.show()


        self.input_widget = QWidget(self)
        self.input_widget.show()
        self.input_widget2 = QWidget(self)
        self.input_widget2.show()

        self.input_count_label = QLabel("", self.input_widget)
        self.input_count_label.setFont(QFont("Arial", 22))
        self.input_count_label.adjustSize()
        self.input_count_label.move(0, 10)
        self.input_count_label.show()

        self.input_count_label2 = QLabel("", self.input_widget2)
        self.input_count_label2.setFont(QFont("Arial", 22))
        self.input_count_label2.adjustSize()
        self.input_count_label2.move(0, 10)
        self.input_count_label2.show()


        label = QLabel("Производство в минуту", self)
        label.setFont(QFont("Arial", 22))
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2 - 10, 245)
        label.show()

        self.output_widget = QWidget(self)
        self.output_widget.show()
        self.output_widget2 = QWidget(self)
        self.output_widget2.show()

        self.output_count_label = QLabel("", self.output_widget)
        self.output_count_label.setFont(QFont("Arial", 22))
        self.output_count_label.adjustSize()
        self.output_count_label.move(0, 10)
        self.output_count_label.show()

        self.output_count_label2 = QLabel("", self.output_widget2)
        self.output_count_label2.setFont(QFont("Arial", 22))
        self.output_count_label2.adjustSize()
        self.output_count_label2.move(0, 10)
        self.output_count_label2.show()