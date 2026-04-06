from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QScrollArea
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt, QSize
from func.Samples.Background import Background
from GF.Constants import *
import os
import json
import time
from GF.SchemeData import SchemeData
from func.Samples.SchemeLabel import SchemeLabel
from func.Comment.Comment import Comment
from send2trash import send2trash

class Widget_load_project(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(800, 600)
        self.move(parent.width() // 2 - self.width() // 2,
                  parent.height() // 2 - self.height() // 2)
        self.hide()
        background = Background("255, 127, 80", self)

        self.current_file = None

        self.btns = []

        self.init_UI_load()

        self.sample = ""


    def load(self):
        if self.current_file is None:
            return
        if not self.GV.project.isSaved:
            self.GV.project.show_widget_if_not_save_before_load()
            return

        self.GV.scale.k = 1
        self.GV.scale.current_scale_percent = 100

        # Удаляем старые схемы и комментарии
        blueprint = self.GV.blueprint
        for scheme in blueprint.schemes:
            scheme.deleteLater()
        blueprint.schemes.clear()
        for comment in blueprint.comments:
            comment.deleteLater()
        blueprint.comments.clear()

        working_directory = self.GV.project.working_directory
        save_path = os.path.join(working_directory, self.current_file)

        scheme_dir = os.path.join(save_path, "schemes")

        # Загружаем файл head
        with open(os.path.join(save_path, "head.txt"), "r", encoding="utf-8") as file:
            lines = file.readlines()

            name = lines[0].split("=")[1].strip()
            self.GV.project.name = name
            self.GV.project.widget_save_as.name_line_edit.setText(name)

            control_bar = self.GV.control_bar

            config = self.GV.config

            self.GV.scale.current_scale_percent = int(lines[11].split("=")[1].strip())
            self.GV.scale.update_view()

            config.blueprint_width = int(lines[1].split("=")[1].strip())
            config.blueprint_height = int(lines[2].split("=")[1].strip())
            control_bar.blueprint_width_line_edit.setText(str(config.blueprint_width) + "px")
            control_bar.blueprint_height_line_edit.setText(str(config.blueprint_height) + "px")
            self.GV.blueprint.update_size_from_config_and_zoom()


            hz = int(lines[3].split("=")[1].strip())
            control_bar.hz_conv_line_edit.setText(str(hz))
            self.GV.config.hz_conv_lines = hz

            hz = int(lines[4].split("=")[1].strip())
            control_bar.hz_mouse_image_line_edit.setText(str(hz))
            self.GV.config.hz_mouse_image = hz


            self.GV.blueprint.paint_area.update_hz_lines()
            self.GV.mouse_image.update_hz_mouse_image()
            self.GV.group_mouse_image.update_hz_group_image()


            flag = bool_from_str(lines[5].split("=")[1].strip())
            control_bar.btns[0].setChecked(flag)
            self.GV.production_area.isSimpleCraft = flag

            flag = bool_from_str(lines[6].split("=")[1].strip())
            control_bar.btns[1].setChecked(flag)
            self.GV.production_area.isPrintCurrent = flag

            flag = bool_from_str(lines[7].split("=")[1].strip())
            control_bar.btns[2].setChecked(flag)
            self.GV.production_area.isPrintTypes = flag

            flag = bool_from_str(lines[8].split("=")[1].strip())
            control_bar.btns[3].setChecked(flag)
            self.GV.production_area.isPrintLogistic = flag

            flag = bool_from_str(lines[9].split("=")[1].strip())
            control_bar.btns[4].setChecked(flag)
            self.GV.production_area.isPrintTypesLogistic = flag

            flag = bool_from_str(lines[10].split("=")[1].strip())
            control_bar.btns[5].setChecked(flag)
            self.GV.config.show_hotkeys = flag
            self.GV.hotkeys.show_hide_from_config()


        # Проходим по всем схемам и загружаем их
        max_id = 0
        data_schemes = []
        for file_name in os.listdir(scheme_dir):
            file_path = os.path.join(scheme_dir, file_name)

            # Преобразуем json файл к словарю
            with open(file_path, 'r', encoding="utf-8") as file:
                dict_data = json.load(file)

            # Загружаем данные в scheme_data
            data_scheme = SchemeData(0, "None", 0, None, True)
            data_scheme.load_from_dict(dict_data)
            data_schemes.append(data_scheme)

            # Проверяем id
            if data_scheme.original_id > max_id:
                max_id = data_scheme.original_id

            # Получаем объект из data_scheme

            object = data_scheme.get_object(self.GV)

            # Создаем схему на blueprint
            scheme = SchemeLabel(self.GV, object, data_scheme.original_id, blueprint)
            scheme.resize(int(object.scheme_width)*self.GV.scale.k,
                          int(object.scheme_height)*self.GV.scale.k)
            scheme.move(data_scheme.x,
                       data_scheme.y)
            scheme.show()

            pixmap = QPixmap(object.scheme)
            scheme.setPixmap(pixmap.scaled(scheme.size()))

            scheme.count_batteries = data_scheme.count_batteries
            scheme.current_recipe_index = data_scheme.current_recipe_index

            scheme.createWidget = data_scheme.createWidget

            blueprint.schemes.append(scheme)

            # Устанавливаем output_objects
            for object_name in data_scheme.output_objects_names:
                output_object = self.GV.database.get_object_from_name(object_name)
                scheme.output_objects.append(output_object)

            for object_name in data_scheme.output_objects_names_liquid:
                output_object = self.GV.database.get_object_from_name(object_name)
                scheme.output_objects_liquid.append(output_object)

        blueprint.free_index_object = max_id + 1

        # Проходим по всем схемам в blueprint и устанавливаем связи
        for i in range(len(data_schemes)):
            for id in data_schemes[i].output_schemes_ids:
                scheme = blueprint.schemes[i]
                output_scheme = blueprint.get_scheme_from_id(id)

                scheme.output_schemes.append(output_scheme)
                output_scheme.input_schemes.append(scheme)

            for id in data_schemes[i].output_schemes_ids_liquid:
                scheme = blueprint.schemes[i]
                output_scheme = blueprint.get_scheme_from_id(id)

                scheme.output_schemes_liquid.append(output_scheme)
                output_scheme.input_schemes_liquid.append(scheme)

        # Загружаем комментарии
        comm_dir = os.path.join(save_path, "comments")
        for file_name in os.listdir(comm_dir):
            file_path = os.path.join(comm_dir, file_name)

            # Преобразуем json файл к словарю
            with open(file_path, 'r', encoding="utf-8") as file:
                dict_data = json.load(file)

            # Создаем схему на blueprint
            comment = Comment(self.GV, blueprint)
            comment.text_layout = dict_data.get("text_layout")

            comment.setLower = dict_data.get("setLower")
            comment.set_Z_from_flag()

            comment.resize(dict_data.get("width"),
                          dict_data.get("height"))

            comment.move(dict_data.get("x"),
                       dict_data.get("y"))

            comment.show()

            comment.text.setText(dict_data.get("text"))
            comment.text_color = dict_data["text_color"]
            comment.head_color = dict_data["head_color"]
            comment.body_color = dict_data["body_color"]
            comment.point_color = dict_data["point_color"]

            comment.update_style_sheet()

            comment.resize_subwidgets()
            comment.set_pos_text_from_layout()

            blueprint.comments.append(comment)

        self.hide()
        self.GV.blueprint.paint_upper_area.raise_()

        self.GV.project.isSaved = True

        self.GV.production_area.tick()

        self.GV.main_under_widget.factory_info_widget.update_factory_info_widget()

        self.GV.historyManager.clear_arrays()

        # Загружаем так же и бинды
        self.GV.cameraSystem.load_binds(save_path)

        # Меняем временную метку
        os.rename(os.path.join(save_path, "head.txt"), os.path.join(save_path, "renamed.txt"))
        os.rename(os.path.join(save_path, "renamed.txt"), os.path.join(save_path, "head.txt"))



    def load_last_project(self):
        working_directory = self.GV.project.working_directory
        array = sorted(os.listdir(working_directory), key=self.sort_functions)
        if len(array) == 0:
            return
        array.reverse()
        self.set_current_file(array[0])
        self.load()


    def set_current_file(self, filename):
        self.current_file = filename


    def sort_functions(self, x):
        path = os.path.join(self.GV.project.working_directory, x)
        return os.path.getmtime(path)


    def search_loads(self):
        for btn in self.btns:
            btn.deleteLater()
        self.btns.clear()

        working_directory = self.GV.project.working_directory
        offset_x = 20
        offset_y = 5
        times = []
        array = sorted(os.listdir(working_directory), key=self.sort_functions)
        array.reverse()
        for project_name in array:
            if not self.sample in project_name:
                continue

            btn = QPushButton(self.contentWidget)
            btn.resize(self.contentWidget.width() - 40, 60)
            btn.move(offset_x, offset_y)
            btn.clicked.connect(lambda clicked=False, save_file=project_name: self.set_current_file(save_file))
            btn.show()

            self.btns.append(btn)

            label = QLabel(project_name, btn)
            label.setFont(QFont("Arial", 22))
            label.adjustSize()
            label.move(10, btn.height() // 2 - label.height() // 2)
            label.show()

            path = os.path.join(working_directory, project_name)
            last_modified_time = os.path.getmtime(path)
            # Преобразуем временную метку в читаемый формат
            time_struct = time.localtime(last_modified_time)
            formatted_time = time.strftime("%H:%M %d:%m:%Y", time_struct)

            times.append(last_modified_time)

            label = QLabel(formatted_time, btn)
            label.setFont(QFont("Arial", 16))
            label.adjustSize()
            label.move(btn.width() - label.width() - 10,
                       btn.height() // 2 - label.height() // 2)
            label.show()

            offset_y += btn.height()
        self.contentWidget.resize(self.contentWidget.width(), offset_y + 15)



    def show(self):
        self.sample = ""
        self.current_file = None

        self.search_loads()

        super().show()


    def hide(self):
        super().hide()
        self.GV.project.hide()


    def remove_save_file(self):
        if self.current_file is None:
            return
        path = os.path.join(self.GV.project.working_directory, self.current_file)
        send2trash(path)
        self.show()
        self.current_file = None
        self.setFocus()


    def search_load_from_sample(self, text):
        sample = text.strip()
        self.sample = sample
        self.search_loads()


    def hotkey_select(self, index):
        try:
            self.btns[index].click()
            self.load()
        except:
            pass


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.load()
        elif event.key() == Qt.Key_Escape:
            self.hide()
        elif event.key() == Qt.Key_Delete:
            self.remove_save_file()
        elif event.key() == Qt.Key_1:
            self.hotkey_select(0)
        elif event.key() == Qt.Key_2:
            self.hotkey_select(1)
        elif event.key() == Qt.Key_3:
            self.hotkey_select(2)
        elif event.key() == Qt.Key_4:
            self.hotkey_select(3)
        elif event.key() == Qt.Key_5:
            self.hotkey_select(4)
        elif event.key() == Qt.Key_6:
            self.hotkey_select(5)
        elif event.key() == Qt.Key_7:
            self.hotkey_select(6)
        elif event.key() == Qt.Key_8:
            self.hotkey_select(7)
        elif event.key() == Qt.Key_9:
            self.hotkey_select(8)
        elif event.key() == Qt.Key_0:
            self.hotkey_select(9)



    def init_UI_load(self):
        label = QLabel("Загрузить", self)
        label.setFont(QFont("Arial", 30))
        label.adjustSize()
        label.move(self.width() // 2 - label.width() // 2, 10)
        label.show()

        self.load_sample_line_edit = QLineEdit(self)
        self.load_sample_line_edit.resize(self.width() - 40, 40)
        self.load_sample_line_edit.move(20, 10 + label.height() + 3)
        self.load_sample_line_edit.setFont(QFont("Arial", 22))
        self.load_sample_line_edit.setAlignment(Qt.AlignCenter)
        self.load_sample_line_edit.show()
        self.load_sample_line_edit.textChanged.connect(self.search_load_from_sample)

        scroll_area = QScrollArea(self)
        scroll_area.resize(self.width() - 20,
                    self.height() - 180)
        scroll_area.move(10, 100)
        scroll_area.setAttribute(Qt.WA_TransparentForMouseEvents, False)  # Обработка событий мыши
        scroll_area.show()


        self.contentWidget = QWidget()
        self.contentWidget.resize(scroll_area.size() + QSize(-19, 0))
        self.contentWidget.show()

        scroll_area.setWidget(self.contentWidget)

        btn = QPushButton("Отменить", self)
        btn.setFont(QFont("Arial", 24))
        btn.resize(200, 64)
        btn.move(20, self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.hide)

        btn = QPushButton("Удалить", self)
        btn.setFont(QFont("Arial", 24))
        btn.resize(200, 64)
        btn.move(self.width() // 2 - btn.width() // 2, self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.remove_save_file)
        btn.setStyleSheet("background-color: rgb(230, 40, 40);")

        btn = QPushButton("Загрузить", self)
        font = QFont("Arial", 24)
        btn.setFont(font)
        btn.resize(200, 64)
        btn.move(self.width() - 20 - btn.width(), self.height() - 10 - btn.height())
        btn.show()
        btn.clicked.connect(self.load)