from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QScrollArea
from PySide6.QtGui import QFont, QKeyEvent, QPixmap, QColor
from PySide6.QtCore import Qt, QSize
from func.Samples.Background import Background
from GF.Constants import *
import os
import json
import time
from GF.SchemeData import SchemeData
from func.Samples.SchemeLabel import SchemeLabel
from decimal import Decimal
import shutil
from PIL import Image

class Widget_save_as_scheme(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(800, 650)
        self.move(parent.width() // 2 - self.width() // 2,
                  parent.height() // 2 - self.height() // 2)
        background = Background("135, 206, 250", self)

        self.path = "CustomSchemes"

        self.input_types = []
        self.input_counts = []
        self.output_types = []
        self.output_counts = []

        self.count_inputs = 0
        self.count_inputs_liquid = 0
        self.energy = 0

        self.image_width = 260
        self.image_height = 180
        self.scheme_width = 240
        self.scheme_height = 170

        self.have_conv_output = False
        self.have_pipe_output = False

        self.count_final_conv = 0
        self.count_final_pipes = 0
        self.zero_schemes = False

        self.path_to_image = r"assets\scheme\image.webp"
        self.path_to_scheme = r"assets\scheme\scheme.png"

        self.images = []

        self.init_UI_save_as_scheme()

        self.hide()

        self.index_widget = 0


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.index_widget < 3:
            self.hide()
        elif event.key() == Qt.Key_Escape and self.index_widget == 3:
            self.stop_widget3()
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.index_widget == 0:
                self.clickContinue1()
            elif self.index_widget == 1:
                self.clickContinue2()
            elif self.index_widget == 2:
                self.start_save()
            elif self.index_widget == 3:
                self.save_as_scheme(True)



    def show(self):
        for image in self.images:
            image.deleteLater()
        self.images.clear()

        self.widget1.hide()
        self.widget2.hide()
        self.widget3.hide()
        self.widget4.hide()

        self.checkConditions()

        self.set_colors()

        self.widget2.show()
        self.index_widget = 0
        super().show()


    def set_colors(self):
        green = "color: rgb(0, 240, 0);"
        red = "color: rgb(240, 0, 0);"

        color = "color: rgb(0, 0, 0);"
        if self.have_conv_output or self.have_pipe_output:
            color = green
        else:
            color = red
        self.label_or.setStyleSheet(color)

        if self.count_final_conv > 1:
            color = red
        else:
            color = green
        self.label_not_con.setStyleSheet(color)

        if self.count_final_pipes > 1:
            color = red
        else:
            color = green
        self.label_not_pip.setStyleSheet(color)

        if self.zero_schemes:
            color = red
        else:
            color = green
        self.label_not_empty.setStyleSheet(color)


    def checkConditions(self):
        if len(self.GV.blueprint.schemes) == 0:
            self.zero_schemes = True
        else:
            self.zero_schemes = False
        self.count_final_conv = 0
        self.count_final_pipes = 0
        self.have_conv_output = False
        self.have_pipe_output = False
        for scheme in self.GV.blueprint.schemes:
            if scheme.object.name == "FinalConv":
                self.count_final_conv += 1
                self.have_conv_output = True
            if scheme.object.name == "FinalPipes":
                self.count_final_pipes += 1
                self.have_pipe_output = True


    def clickContinue2(self):
        self.widget4.hide()

        self.set_scheme_values()
        self.index_widget = 2
        self.widget1.show()


    def clickContinue1(self):
        # Проверяем флаги
        if self.zero_schemes:
            return
        if not (self.have_conv_output or self.have_pipe_output):
            return
        if self.count_final_pipes > 1 or self.count_final_conv > 1:
            return

        # Проверяем имя
        name = self.name_line_edit.text().strip()
        if name == "":
            return

        self.widget2.hide()
        self.index_widget = 1
        self.widget4.show()


    def set_scheme_values(self):
        # Удаляем все старые картинки
        for image in self.images:
            image.deleteLater()
        self.images.clear()

        # Считаем потребление
        all_voltage = 0
        for scheme in self.GV.blueprint.schemes:
            voltage = scheme.object.energy
            voltage = get_voltage(voltage, scheme.count_batteries)
            all_voltage += voltage
        self.voltage_label.setText(f"{all_voltage}МВт")
        self.voltage_label.adjustSize()
        self.energy = all_voltage

        all_voltage = 0
        for scheme in self.GV.blueprint.schemes:
            if scheme.object.category == "boers" or scheme.object.category == "extractors":
                continue
            voltage = scheme.object.energy
            voltage = get_voltage(voltage, scheme.count_batteries)
            all_voltage += voltage
        self.voltage_without_label.setText(f"{all_voltage}МВт")
        self.voltage_without_label.adjustSize()

        # Считаем инпуты
        input_types = []
        input_counts = []
        for scheme in self.GV.blueprint.schemes:
            if not (len(scheme.input_schemes) == 0 and not len(scheme.input_schemes_liquid) == 0):
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
        self.input_types.clear()
        self.input_counts.clear()
        for i in range(len(input_types)):
            current_type = input_types[i]

            if current_type in self.input_types:
                continue

            self.input_types.append(current_type)
            self.input_counts.append(input_counts[i])

            for j in range(i+1, len(input_types)):
                if input_types[i] == input_types[j]:
                    self.input_counts[-1] += input_counts[j]



        # Считаем вывод со схемы
        output_types = []
        output_counts = []
        for scheme in self.GV.blueprint.schemes:
            if not ( scheme.object.name == "FinalConv" or scheme.object.name == "FinalPipes"):
                continue

            for res_type in scheme.types_resources_input:
                output_types.append(res_type)
            for res_count in scheme.count_resources_input:
                output_counts.append(res_count)

            for res_type in scheme.types_resources_output_liquid:
                output_types.append(res_type)
            for res_count in scheme.count_resources_output_liquid:
                output_counts.append(res_count)

        self.output_types = output_types[:]
        self.output_counts = output_counts[:]


        # Рисуем инпуты
        offset_x = 20
        offset_y = 260
        btnW = 40
        btnH = 40
        s = ""
        for i in range(len(self.input_types)):
            res = self.input_types[i]
            count = self.input_counts[i]

            count = Decimal(count).normalize()
            s += str(format(count, "f"))

            for j in range(6):
                s += " "

            self.input_label.setText(s)
            self.input_label.adjustSize()

            image = QLabel(self.widget1)
            image.resize(btnW, btnH)
            image.move(offset_x + self.input_label.width() - 50, offset_y)
            image.show()
            pixmap = QPixmap(res.image)
            image.setPixmap(pixmap.scaled(image.size()))

            self.images.append(image)


        # Рисуем оутпуты
        offset_x = 20
        offset_y = 360
        btnW = 40
        btnH = 40
        s = ""
        for i in range(len(self.output_types)):
            res = self.output_types[i]
            count = self.output_counts[i]

            count = Decimal(count).normalize()
            s += str(format(count, "f"))

            for j in range(6):
                s += " "

            self.output_label.setText(s)
            self.output_label.adjustSize()

            image = QLabel(self.widget1)
            image.resize(btnW, btnH)
            image.move(offset_x + self.output_label.width() - 50, offset_y)
            image.show()
            pixmap = QPixmap(res.image)
            image.setPixmap(pixmap.scaled(image.size()))

            self.images.append(image)

        # Ставим значения в поля input
        count_conv_input = 0
        count_pipe_input = 0
        for scheme in self.GV.blueprint.schemes:
            if not (len(scheme.input_schemes) == 0 and len(scheme.input_schemes_liquid) == 0):
                continue
            count_conv_input += scheme.free_input
            count_pipe_input += scheme.free_input_liquid
        self.count_conv_line_edit.setText(str(count_conv_input))
        self.count_pipe_line_edit.setText(str(count_pipe_input))
        self.count_inputs = count_conv_input
        self.count_inputs_liquid = count_pipe_input


    def changeCountInputsConv(self):
        text = self.count_conv_line_edit.text()
        if not text.isdigit():
            self.count_conv_line_edit.setText(str(self.count_inputs))
            return
        text = int(text)
        if text < 0 and text > 9:
            self.count_conv_line_edit.setText(str(self.count_inputs))
            return
        self.count_inputs = text


    def changeCountInputsPipe(self):
        text = self.count_pipe_line_edit.text()
        if not text.isdigit():
            self.count_pipe_line_edit.setText(str(self.count_inputs_liquid))
            return
        text = int(text)
        if text < 0 and text > 9:
            self.count_pipe_line_edit.setText(str(self.count_inputs_liquid))
            return
        self.count_inputs_liquid = text


    def select_scheme(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilters(["Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"])

        if file_dialog.exec():
            self.path_to_scheme = file_dialog.selectedFiles()[0]
            self.label_path_scheme.setText(self.path_to_scheme)
            self.label_path_scheme.adjustSize()


    def select_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilters(["Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"])

        if file_dialog.exec():
            self.path_to_image = file_dialog.selectedFiles()[0]
            self.label_path_image.setText(self.path_to_image)
            self.label_path_image.adjustSize()


    def start_save(self):
        name = self.name_line_edit.text().strip()

        if name in os.listdir(self.path):
            self.index_widget = 3
            self.start_widget3()
        else:
            self.save_as_scheme()



    def save_as_scheme(self, del_flag=False):
        self.grey_mask.hide()

        name = self.name_line_edit.text().strip()
        scheme_dir_path = os.path.join(self.path, name)

        # Создаем или пересоздаем папку
        if del_flag:
            if os.path.exists(scheme_dir_path):
                shutil.rmtree(scheme_dir_path)

        os.mkdir(scheme_dir_path)

        # Переносим картинки
        image = Image.open(self.path_to_image)
        image.save(os.path.join(scheme_dir_path, f"image.png"))

        image = Image.open(self.path_to_scheme)
        image.save(os.path.join(scheme_dir_path, f"scheme.png"))

        # Создаем файлик с размерами
        lines = [
            f"scheme width = {self.scheme_width}\n",
            f"scheme height = {self.scheme_height}\n",
            f"dragging width = {self.image_width}\n",
            f"dragging height = {self.image_height}\n"
        ]
        with open(os.path.join(scheme_dir_path, "sizes.txt"), "w", encoding="utf-8") as file:
            file.writelines(lines)

        # Создаем файлик с основными данными
        lines = [
            f"Название = {name}\n",
            f"Категория = custom\n"
            f"Потребление энергии = {self.energy}\n"
            f"Входящие потоки = {self.count_inputs}\n"
            f"Исходящие потоки = {1 if self.have_conv_output else 0}\n",
            f"Входящие жидкости = {self.count_inputs_liquid}\n",
            f"Исходящие жидкости = {1 if self.have_pipe_output else 0}\n",
            f"type (block, logistic) = block\n",
            f"Уровень появления = {self.GV.config.current_lvl}\n"
        ]
        with open(os.path.join(scheme_dir_path, "data.txt"), "w", encoding="utf-8") as file:
            file.writelines(lines)


        # Создаем папку с рецептами
        recipes_dir = os.path.join(scheme_dir_path, "Recipes")
        os.mkdir(recipes_dir)
        tooltip_path = r"DataBase\01 Конструктор\Recipes\00 tooltip.txt"
        shutil.copy(tooltip_path, recipes_dir)

        # Создаем рецепт
        lines = [f"lvl = {self.GV.config.current_lvl}\n"]
        for i in range(len(self.input_types)):
            lines.append(self.input_types[i].name+"\n")
            value = self.input_counts[i].normalize()
            lines.append(format(value, "f")+"\n")
        lines.append("===============================\n")
        for i in range(len(self.output_types)):
            lines.append(self.output_types[i].name+"\n")
            value = self.output_counts[i].normalize()
            lines.append(format(value, "f")+"\n")

        with open(os.path.join(recipes_dir, "recipe.txt"), "w", encoding="utf-8") as file:
            file.writelines(lines)

        self.hide()




    def stop_widget3(self):
        self.grey_mask.hide()
        self.index_widget = 2
        self.widget3.hide()

    def start_widget3(self):
        self.grey_mask.show()
        self.widget3.show()


    def check_current_size(self, size):
        if not size.isdigit():
            return False
        size = int(size)
        if size < 10:
            return False
        if size > 1000:
            return False
        return True


    def changeEditLineHeightScheme(self):
        text = self.scheme_height_line_edit.text()
        flag = self.check_current_size(text)
        if not flag:
            self.scheme_height_line_edit.setText(str(self.scheme_height))
            return
        self.scheme_height = int(text)


    def changeEditLineWidthScheme(self):
        text = self.scheme_width_line_edit.text()
        flag = self.check_current_size(text)
        if not flag:
            self.scheme_width_line_edit.setText(str(self.scheme_width))
            return
        self.scheme_width = int(text)


    def changeEditLineHeightImage(self):
        text = self.image_height_line_edit.text()
        flag = self.check_current_size(text)
        if not flag:
            self.image_height_line_edit.setText(str(self.image_height))
            return
        self.image_height = int(text)


    def changeEditLineWidthImage(self):
        text = self.image_width_line_edit.text()
        flag = self.check_current_size(text)
        if not flag:
            self.image_width_line_edit.setText(str(self.image_width))
            return
        self.image_width = int(text)


    def init_widget4(self):
        self.widget4 = QWidget(self)
        self.widget4.resize(self.size())
        self.widget4.hide()

        label = QLabel("Сохранить как схему", self.widget4)
        label.setFont(QFont("Arial", 30))
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2, 10)
        label.show()

        # Для изображения
        label = QLabel("Размер изображения в пикселях", self.widget4)
        label.setFont(QFont("Arial", 24))
        label.adjustSize()
        label.move(20, 80)
        label.show()

        self.image_width_line_edit = QLineEdit("260", self.widget4)
        self.image_width_line_edit.setFont(QFont("Arial", 20))
        self.image_width_line_edit.resize(160, 40)
        self.image_width_line_edit.setAlignment(Qt.AlignCenter)
        self.image_width_line_edit.move(40, 140)
        self.image_width_line_edit.show()
        self.image_width_line_edit.editingFinished.connect(self.changeEditLineWidthImage)

        label = QLabel("Ширина", self.widget4)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.move(40 + self.image_width_line_edit.width() + 15,
                   self.image_width_line_edit.pos().y() + self.image_width_line_edit.height() // 2 - label.height()//2 )
        label.show()

        self.image_height_line_edit = QLineEdit("180", self.widget4)
        self.image_height_line_edit.setFont(QFont("Arial", 20))
        self.image_height_line_edit.resize(160, 40)
        self.image_height_line_edit.setAlignment(Qt.AlignCenter)
        self.image_height_line_edit.move(40, 195)
        self.image_height_line_edit.show()
        self.image_height_line_edit.editingFinished.connect(self.changeEditLineHeightImage)

        label = QLabel("Высота", self.widget4)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.move(40 + self.image_height_line_edit.width() + 15,
                   self.image_height_line_edit.pos().y()+self.image_height_line_edit.height()//2-label.height()//2)
        label.show()


        # Для схемы
        label = QLabel("Размер схемы в пикселях", self.widget4)
        label.setFont(QFont("Arial", 24))
        label.adjustSize()
        label.move(20, 260)
        label.show()

        self.scheme_width_line_edit = QLineEdit("240", self.widget4)
        self.scheme_width_line_edit.setFont(QFont("Arial", 20))
        self.scheme_width_line_edit.resize(160, 40)
        self.scheme_width_line_edit.setAlignment(Qt.AlignCenter)
        self.scheme_width_line_edit.move(40, 320)
        self.scheme_width_line_edit.show()
        self.scheme_width_line_edit.editingFinished.connect(self.changeEditLineWidthScheme)

        label = QLabel("Ширина", self.widget4)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.move(40 + self.scheme_width_line_edit.width() + 15,
                   self.scheme_width_line_edit.pos().y() + self.scheme_width_line_edit.height()// 2 - label.height()//2)
        label.show()

        self.scheme_height_line_edit = QLineEdit("170", self.widget4)
        self.scheme_height_line_edit.setFont(QFont("Arial", 20))
        self.scheme_height_line_edit.resize(160, 40)
        self.scheme_height_line_edit.setAlignment(Qt.AlignCenter)
        self.scheme_height_line_edit.move(40, 375)
        self.scheme_height_line_edit.show()
        self.scheme_height_line_edit.editingFinished.connect(self.changeEditLineHeightScheme)

        label = QLabel("Высота", self.widget4)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.move(40 + self.scheme_height_line_edit.width() + 15,
                   self.scheme_height_line_edit.pos().y()+self.scheme_height_line_edit.height()//2-label.height()//2)
        label.show()


        # Инициализируем кнопки
        btn = QPushButton("Отменить", self.widget4)
        btn.setFont(QFont("Arial", 24))
        btn.resize(200, 64)
        btn.move(20, self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.hide)

        btn = QPushButton("Далее", self.widget4)
        font = QFont("Arial", 24)
        btn.setFont(font)
        btn.resize(200, 64)
        btn.move(self.width() - 20 - btn.width(), self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.clickContinue2)



    def init_widget3(self):
        self.grey_mask = QLabel(self)
        self.grey_mask.resize(self.size())
        self.grey_mask.setStyleSheet(f"background-color: rgba(0, 0, 0, 0.4);")
        self.grey_mask.hide()

        self.widget3 = QWidget(self)
        self.widget3.resize(self.width()-100, 300)
        self.widget3.hide()
        self.widget3.move(50, self.height() // 2 - self.widget3.height() // 2)
        back = Background("106, 90, 205", self.widget3)

        label = QLabel("Такая схема уже существует", self.widget3)
        label.setFont(QFont("Arial", 28))
        label.adjustSize()
        label.move(self.widget3.width() // 2 - label.width() // 2, 10)
        label.show()

        label = QLabel("Продолжение перезапишет существующую схему", self.widget3)
        label.setFont(QFont("Arial", 18))
        label.adjustSize()
        label.move(self.widget3.width() // 2 - label.width() // 2, 65)
        label.show()

        # Инициализируем кнопки
        btn = QPushButton("Отменить", self.widget3)
        btn.setFont(QFont("Arial", 24))
        btn.resize(200, 64)
        btn.move(20, self.widget3.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.stop_widget3)

        btn = QPushButton("Продолжить", self.widget3)
        font = QFont("Arial", 24)
        btn.setFont(font)
        btn.resize(200, 64)
        btn.move(self.widget3.width() - 20 - btn.width(), self.widget3.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(lambda clicked=False: self.save_as_scheme(True))


    def init_widget2(self):
        self.widget2 = QWidget(self)
        self.widget2.resize(self.size())
        self.widget2.hide()

        label = QLabel("Сохранить как схему", self.widget2)
        label.setFont(QFont("Arial", 30))
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2, 10)
        label.show()

        self.label_or = QLabel("Есть вывод для конвейеров или вывод для труб", self.widget2)
        self.label_or.setFont(QFont("Arial", 15))
        self.label_or.adjustSize()
        self.label_or.move(20, 60)
        self.label_or.show()

        self.label_not_con = QLabel("Не более одного вывода для конвейеров", self.widget2)
        self.label_not_con.setFont(QFont("Arial", 15))
        self.label_not_con.adjustSize()
        self.label_not_con.move(20, 90)
        self.label_not_con.show()

        self.label_not_pip = QLabel("Не более одного вывода для труб", self.widget2)
        self.label_not_pip.setFont(QFont("Arial", 15))
        self.label_not_pip.adjustSize()
        self.label_not_pip.move(20, 120)
        self.label_not_pip.show()

        self.label_not_empty = QLabel("Не пустая схема", self.widget2)
        self.label_not_empty.setFont(QFont("Arial", 15))
        self.label_not_empty.adjustSize()
        self.label_not_empty.move(20, 150)
        self.label_not_empty.show()

        # Инициализируем поле с данными
        label = QLabel("Название", self.widget2)
        label.setFont(QFont("Arial", 24))
        label.adjustSize()
        label.move(40, 190)
        label.show()

        self.name_line_edit = QLineEdit(self.GV.project.name, self.widget2)
        font = QFont("Arial", 25)
        self.name_line_edit.setFont(font)
        self.name_line_edit.resize(self.width() - 120, 50)
        self.name_line_edit.setAlignment(Qt.AlignCenter)
        self.name_line_edit.move(60, 230)
        self.name_line_edit.show()

        label = QLabel("Изображение", self.widget2)
        label.setFont(QFont("Arial", 24))
        label.adjustSize()
        label.move(40, 300)
        label.show()

        btn = QPushButton("Выбрать", self.widget2)
        btn.setFont(QFont("Arial", 24))
        btn.resize(180, 60)
        btn.move(20, 340)
        btn.show()
        btn.clicked.connect(self.select_image)

        self.label_path_image = QLabel(r"None", self.widget2)
        self.label_path_image.setFont(QFont("Arial", 20))
        self.label_path_image.adjustSize()
        self.label_path_image.move(20 + btn.width() + 10,
                                   btn.pos().y() + btn.height() // 2 - self.label_path_image.height() // 2)
        self.label_path_image.show()

        label = QLabel("Схема", self.widget2)
        label.setFont(QFont("Arial", 24))
        label.adjustSize()
        label.move(40, 420)
        label.show()

        btn = QPushButton("Выбрать", self.widget2)
        btn.setFont(QFont("Arial", 24))
        btn.resize(180, 60)
        btn.move(20, 460)
        btn.show()
        btn.clicked.connect(self.select_scheme)

        self.label_path_scheme = QLabel(r"None", self.widget2)
        self.label_path_scheme.setFont(QFont("Arial", 20))
        self.label_path_scheme.adjustSize()
        self.label_path_scheme.move(20 + btn.width() + 10,
                                   btn.pos().y() + btn.height() // 2 - self.label_path_scheme.height() // 2)
        self.label_path_scheme.show()

        # Инициализируем кнопки
        btn = QPushButton("Отменить", self.widget2)
        btn.setFont(QFont("Arial", 24))
        btn.resize(200, 64)
        btn.move(20, self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.hide)

        btn = QPushButton("Далее", self.widget2)
        font = QFont("Arial", 24)
        btn.setFont(font)
        btn.resize(200, 64)
        btn.move(self.width() - 20 - btn.width(), self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.clickContinue1)


    def init_widget1(self):
        self.widget1 = QWidget(self)
        self.widget1.resize(self.size())
        self.widget1.show()

        label = QLabel("Сохранить как схему", self.widget1)
        label.setFont(QFont("Arial", 30))
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2, 10)
        label.show()

        label = QLabel("Характеристики", self.widget1)
        label.setFont(QFont("Arial", 28))
        label.adjustSize()
        label.move(10, 80)
        label.show()

        # Инициализируем верхнюю часть
        label = QLabel("Потребление: ", self.widget1)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.move(25, 130)
        label.show()

        self.voltage_label = QLabel("30МВт", self.widget1)
        self.voltage_label.setFont(QFont("Arial", 22))
        self.voltage_label.adjustSize()
        self.voltage_label.move(25 + label.width() + 10, 130)
        self.voltage_label.show()

        label = QLabel("Потребление без добывающих зданий: ", self.widget1)
        label.setFont(QFont("Arial", 20))
        label.adjustSize()
        label.move(25, 170)
        label.show()

        self.voltage_without_label = QLabel("24МВт", self.widget1)
        self.voltage_without_label.setFont(QFont("Arial", 22))
        self.voltage_without_label.adjustSize()
        self.voltage_without_label.move(25 + label.width() + 10, 170)
        self.voltage_without_label.show()

        # Инициализируем входящие и исходящие потоки
        label = QLabel("Входящие потоки", self.widget1)
        label.setFont(QFont("Arial", 25))
        label.adjustSize()
        label.move(10, 220)
        label.show()

        self.input_label = QLabel("None", self.widget1)
        self.input_label.setFont(QFont("Arial", 28))
        self.input_label.adjustSize()
        self.input_label.move(20, 260)
        self.input_label.show()

        label = QLabel("Исходящие потоки", self.widget1)
        label.setFont(QFont("Arial", 25))
        label.adjustSize()
        label.move(10, 320)
        label.show()

        self.output_label = QLabel("None", self.widget1)
        self.output_label.setFont(QFont("Arial", 28))
        self.output_label.adjustSize()
        self.output_label.move(20, 360)
        self.output_label.show()

        # Инициализируем эдит лайны снизу
        label = QLabel("Кол-во входящих конвейеров", self.widget1)
        label.setFont(QFont("Arial", 22))
        label.adjustSize()
        label.move(20, 440)
        label.show()

        self.count_conv_line_edit = QLineEdit(self.GV.project.name, self.widget1)
        self.count_conv_line_edit.setFont(QFont("Arial", 22))
        self.count_conv_line_edit.resize(240, 45)
        self.count_conv_line_edit.setAlignment(Qt.AlignCenter)
        self.count_conv_line_edit.move(50, 490)
        self.count_conv_line_edit.show()
        self.count_conv_line_edit.editingFinished.connect(self.changeCountInputsConv)

        label = QLabel("Кол-во входящих труб", self.widget1)
        label.setFont(QFont("Arial", 22))
        label.adjustSize()
        label.move(self.width() - label.width() - 20, 440)
        label.show()

        self.count_pipe_line_edit = QLineEdit(self.GV.project.name, self.widget1)
        self.count_pipe_line_edit.setFont(QFont("Arial", 22))
        self.count_pipe_line_edit.resize(240, 45)
        self.count_pipe_line_edit.setAlignment(Qt.AlignCenter)
        self.count_pipe_line_edit.move(self.width() - self.count_pipe_line_edit.width() - 50,
                                       490)
        self.count_pipe_line_edit.show()
        self.count_pipe_line_edit.editingFinished.connect(self.changeCountInputsPipe)


        # Инициализируем кнопки
        btn = QPushButton("Отменить", self.widget1)
        btn.setFont(QFont("Arial", 24))
        btn.resize(200, 64)
        btn.move(20, self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.hide)

        btn = QPushButton("Сохранить", self.widget1)
        font = QFont("Arial", 24)
        btn.setFont(font)
        btn.resize(200, 64)
        btn.move(self.width() - 20 - btn.width(), self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.start_save)



    def init_UI_save_as_scheme(self):
        self.init_widget1()

        self.init_widget2()

        self.init_widget3()

        self.init_widget4()


    def hide(self):
        super().hide()
        self.GV.project.hide()
        self.input_label.setText("None")
        self.input_label.adjustSize()
        self.output_label.setText("None")
        self.output_label.adjustSize()