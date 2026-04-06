from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QFont, QKeyEvent
from PySide6.QtCore import Qt
from func.Samples.Background import Background
import os
import json

class Widget_save_as(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(parent.size())
        self.hide()
        background = Background("135, 206, 235", self)
        
        self.isExitSave = False
        self.isLoadSave = False
        self.isNewProjectSave = False

        self.init_UI()


    def show(self):
        self.name_line_edit.setText(self.GV.project.name)
        super().show()


    def hide(self):
        self.isExitSave = False
        self.isLoadSave = False
        self.isNewProjectSave = False
        super().hide()


    def start_save_project(self):
        # Функция проверяет не пустое ли имя, устанавливает его в проект, и существует ли сейв с таким названием
        name = self.name_line_edit.text().strip()
        name = self.validName(name)
        if name == "":
            return
        self.GV.project.name = name
        working_directory = self.GV.project.working_directory

        if not os.path.exists(working_directory.strip()):
            print(f"Ошибка сохранения, не удалось найти папку с сохранениями по пути\n{working_directory}")
            return

        # Получаем путь к файлу сохранения и файлу head
        save_path = os.path.join(working_directory, name)

        # Если папки сохранения не существует, то создаем ее
        if not os.path.exists(save_path):
            os.mkdir(save_path)
            self.save_project()

            if self.isLoadSave:
                self.GV.project.widget_load_project.load()
                return

            if self.isExitSave:
                self.GV.exit_application()
                return

            if self.isNewProjectSave:
                self.GV.widget_new_project.create_new_project()
                return

        else:
            if self.isLoadSave:
                self.save_project()
                self.GV.project.widget_load_project.load()
                return

            if self.isExitSave:
                self.save_project()
                self.GV.exit_application()
                return

            if self.isNewProjectSave:
                self.save_project()
                self.GV.widget_new_project.create_new_project()
                return

            self.check_save_widget.show()


    def validName(self, name):
        wrong_symbols = r'<>:"/\\|?*'
        new_name = ""
        for char in name:
            if char in wrong_symbols:
                new_name += "@"
                continue
            new_name += char
        return new_name

    def save_project(self):
        self.check_save_widget.hide()

        name = self.name_line_edit.text().strip()
        name = self.validName(name)
        working_directory = self.GV.project.working_directory

        # Получаем путь к файлу сохранения и файлу head
        save_path = os.path.join(working_directory, name)
        head_file_path = os.path.join(save_path, r"head.txt")

        # Вызываем сохранение биндов камер
        self.GV.cameraSystem.save_binds(save_path)

        # Записываем в файл head название проекта
        lines = [
            f"Название = {name}\n",

            f"blueprint width = {self.GV.config.blueprint_width}\n",
            f"blueprint height = {self.GV.config.blueprint_height}\n",

            f"hz lines = {self.GV.config.hz_conv_lines}\n",
            f"hz images = {self.GV.config.hz_mouse_image}\n",

            f"flag Simple Craft = {self.GV.production_area.isSimpleCraft}\n",
            f"flag Print Current = {self.GV.production_area.isPrintCurrent}\n",
            f"flag Print Types = {self.GV.production_area.isPrintTypes}\n",
            f"flag Print Logistic = {self.GV.production_area.isPrintLogistic}\n",
            f"flag Print Types Logistic = {self.GV.production_area.isPrintTypesLogistic}\n",

            f"flag Show Hotkeys = {self.GV.config.show_hotkeys}\n"
            
            f"Current Scale Percent = {self.GV.scale.current_scale_percent}\n"
                ]
        with open(head_file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)

        # Если не существует папки со схемами, создаем ее
        scheme_dir = os.path.join(save_path, "schemes")
        if not os.path.exists(scheme_dir):
            os.mkdir(scheme_dir)

        # На всякий случай удаляем все файлы
        for file_name in os.listdir(scheme_dir):
            file_path = os.path.join(scheme_dir, file_name)
            os.remove(file_path)

        # Проходим по всем схемам и превращаем их в файлы
        for scheme in self.GV.blueprint.schemes:
            data_scheme = scheme.get_scheme_data_save()

            dict_scheme = data_scheme.__dict__

            with open(os.path.join(scheme_dir, f"{scheme.id}.json"), "w", encoding="utf-8") as file:
                json.dump(dict_scheme, file, indent=4, ensure_ascii=False)


        # Если не существует папки с комментариями, создаем ее
        comm_dir = os.path.join(save_path, "comments")
        if not os.path.exists(comm_dir):
            os.mkdir(comm_dir)

        # На всякий случай удаляем все файлы
        for file_name in os.listdir(comm_dir):
            file_path = os.path.join(comm_dir, file_name)
            os.remove(file_path)

        # Проходим по всем комментариям и сохраняем их
        index = 0
        for comment in self.GV.blueprint.comments:
            commentData = comment.get_comment_data()

            commentDataDict = commentData.__dict__

            with open(os.path.join(comm_dir, f"{index}.json"), "w", encoding="utf-8") as file:
                json.dump(commentDataDict, file, indent=4, ensure_ascii=False)
            index += 1


        self.GV.project.hide()

        self.GV.project.isSaved = True

        # Меняем временную метку
        os.rename(os.path.join(save_path, "head.txt"), os.path.join(save_path, "renamed.txt"))
        os.rename(os.path.join(save_path, "renamed.txt"), os.path.join(save_path, "head.txt"))


    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if not self.check_save_widget.isVisible():
                self.start_save_project()
                return
            self.save_project()
        if event.key() == Qt.Key_Escape:
            if self.check_save_widget.isVisible():
                self.check_save_widget.hide()
                return
            self.GV.project.hide()


    def init_UI(self):
        label = QLabel("Сохранение проекта", self)
        font = QFont("Arial", 30)
        label.setFont(font)
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2, 10)
        label.show()

        label = QLabel("Название:", self)
        font = QFont("Arial", 26)
        label.setFont(font)
        label.adjustSize()
        label.move(40, 100)
        label.show()

        self.name_line_edit = QLineEdit(self.GV.project.name, self)
        font = QFont("Arial", 28)
        self.name_line_edit.setFont(font)
        self.name_line_edit.setStyleSheet("padding-left: 10px;")
        self.name_line_edit.resize(self.width() - 120, 60)
        self.name_line_edit.move(60, 170)
        self.name_line_edit.show()


        btn = QPushButton("Отменить", self)
        font = QFont("Arial", 24)
        btn.setFont(font)
        btn.resize(200, 64)
        btn.move(20, self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.GV.project.hide)

        btn = QPushButton("Сохранить", self)
        font = QFont("Arial", 24)
        btn.setFont(font)
        btn.resize(200, 64)
        btn.move(self.width() - 20 - btn.width(), self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.start_save_project)

        # Создаем дочерний виджет, который будет спрашивать перезапись сохранения
        self.check_save_widget = QWidget(self)
        self.check_save_widget.resize(self.size())
        self.check_save_widget.hide()
        background = Background("255, 192, 203", self.check_save_widget)

        label = QLabel("Файл с таким названием уже существует", self.check_save_widget)
        label.setFont(QFont("Arial", 27))
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2, 15)
        label.show()

        label = QLabel("Вы уверенны что хотите перезаписать его?", self.check_save_widget)
        label.setFont(QFont("Arial", 24))
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2, 50)
        label.show()

        btn = QPushButton("Отменить", self.check_save_widget)
        font = QFont("Arial", 24)
        btn.setFont(font)
        btn.resize(200, 64)
        btn.move(25, self.height() - 15 - btn.height())
        btn.show()
        btn.clicked.connect(self.check_save_widget.hide)

        btn = QPushButton("Сохранить", self.check_save_widget)
        font = QFont("Arial", 24)
        btn.setFont(font)
        btn.resize(200, 64)
        btn.move(self.width() - 25 - btn.width(), self.height() - 15 - btn.height())
        btn.show()
        btn.clicked.connect(self.save_project)