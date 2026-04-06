import shutil

from PySide6.QtWidgets import QWidget, QLabel, QPushButton
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt, QPoint
from func.Samples.Background import Background
import os
import json
from GF.SchemeData import SchemeData
from func.Samples.IButton import IButton


class Hotkeys(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.hotkeys = self
        super().__init__(parent)

        self.current_index_frames = 0

        self.resize(90*10+10*9+10*2 + 60, 100)
        self.move(parent.right_widget.pos().x() + parent.right_widget.width() // 2 - self.width() // 2,
                  parent.height() - self.height() - 100)
        self.show()
        background = Background("255, 100, 75", self)

        self.init_frames()

        self.init_hotkeys_ui()

        self.show_hide_from_config()



    def show_frames_from_lvl(self):
        for frame_lvl in self.frames:
            for frame in frame_lvl:
                if frame.isVisible():
                    frame.hide()

        for frame in self.frames[self.current_index_frames]:
            frame.show()


    def load_hotkeys(self, save_path):
        hotkey_path = os.path.join(save_path, "hotkeys")

        if not os.path.exists(hotkey_path):
            return

        lvl_index = 0
        frame_index = 0
        for lvl_name in os.listdir(hotkey_path):
            frame_index = 0
            lvl_path = os.path.join(hotkey_path, lvl_name)

            for frame_name in os.listdir(lvl_path):
                frame_path = os.path.join(lvl_path, frame_name)

                with open(os.path.join(frame_path, "flag.txt"), "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    flag_name = lines[0].split("=")[1].strip()
                    self.frames[lvl_index][frame_index].set_flag_from_name(flag_name)

                for file_name in os.listdir(frame_path):
                    if file_name == "flag.txt":
                        continue

                    if file_name.split(".")[-1] == "txt":
                        with open(os.path.join(frame_path, file_name), "r", encoding="utf-8") as file:
                            lines = file.readlines()
                            name = lines[0].split("=")[1].strip()
                            object = self.GV.database.get_object_from_name(name)
                            self.frames[lvl_index][frame_index].group.append(object)

                    elif file_name .split(".")[-1] == "json":
                        with open(os.path.join(frame_path, file_name), "r", encoding="utf-8") as file:
                            dict_data = json.load(file)

                            # Загружаем данные в scheme_data
                            data_scheme = SchemeData(0, "None", 0, None, True)
                            data_scheme.load_from_dict(dict_data)

                            self.frames[lvl_index][frame_index].group.append(data_scheme)

                self.frames[lvl_index][frame_index].update_image()
                frame_index += 1

            lvl_index += 1



    def save_hotkeys(self, dir_path):
        hotkey_path = os.path.join(dir_path, "hotkeys")
        if os.path.exists(hotkey_path):
            shutil.rmtree(hotkey_path)
        os.mkdir(hotkey_path)

        for i in range(10):
            path = os.path.join(hotkey_path, f"{i}")
            os.mkdir(path)
            for j in range(10):
                sub_path = os.path.join(path, f"{j}")
                os.mkdir(sub_path)


        lvl_index = 0
        frame_index = 0
        id = 0
        for frame_lvl in self.frames:
            frame_index = 0
            lvl_path = os.path.join(hotkey_path, str(lvl_index))

            for frame in frame_lvl:

                frame_path = os.path.join(lvl_path, str(frame_index))

                with open(os.path.join(frame_path, "flag.txt"), "w", encoding="utf-8") as file:
                    file.writelines([f"Установленный флаг = {frame.get_current_flag()}\n"])

                for some_object in frame.group:

                    if isinstance(some_object, SchemeData):
                        dict_scheme = some_object.__dict__

                        with open(os.path.join(frame_path, f"{id}.json"), "w", encoding="utf-8") as file:
                            json.dump(dict_scheme, file, indent=4, ensure_ascii=False)
                    else:
                        name = some_object.name
                        with open(os.path.join(frame_path, f"{id}.txt"), "w", encoding="utf-8") as file:
                            file.writelines([f"Имя объекта = {name}\n"])

                    id += 1

                frame_index += 1

            lvl_index += 1


    def show_hide_from_config(self):
        flag = self.GV.config.show_hotkeys
        if flag:
            self.show()
        else:
            self.hide()


    def select_lvl_hotkeys(self, number):
        index = number - 1
        if number == 0:
            index = 9

        self.current_index_frames = index
        self.show_frames_from_lvl()

        # Обновляем картинку
        self.current_lvl_label.setText(f"{number}")
        self.current_lvl_label.adjustSize()



    def paste_hotkey(self, number):
        index = number - 1
        if number == 0:
            index = 9

        self.frames[self.current_index_frames][index].paste_from_hotkey()


    def add_hotkey(self, number):
        index = number - 1
        if number == 0:
            index = 9

        self.frames[self.current_index_frames][index].set_frame_hotkey()


    def init_frames(self):
        self.frames = []

        offset_y = 5
        for i in range(10):
            lvl_frames = []
            offset_x = 10
            for i in range(10):
                frame = Frame(i, self.GV, self)
                frame.move(offset_x, offset_y)
                lvl_frames.append(frame)

                offset_x += frame.width() + 10

            self.frames.append(lvl_frames)

        self.show_frames_from_lvl()


    def up_frame_lvl(self):
        number = self.current_index_frames + 1
        number += 1

        if number == 10:
            number = 0

        if number == 11:
            number = 1

        self.select_lvl_hotkeys(number)


    def down_frame_lvl(self):
        number = self.current_index_frames + 1
        number -= 1

        self.select_lvl_hotkeys(number)


    def init_hotkeys_ui(self):
        btn = IButton(self)
        btn.resize(46, 20)
        btn.move(self.width() - 7 - btn.width(), 8)
        btn.setPathsToImages(r"assets/Hotkeys/up/image.png",
                             r"assets/Hotkeys/up/image_pressed.png",
                             r"assets/Hotkeys/hover.png")
        btn.clicked.connect(self.up_frame_lvl)

        self.current_lvl_label = QLabel("1", self)
        self.current_lvl_label.setFont(QFont("Arial", 30))
        self.current_lvl_label.adjustSize()
        self.current_lvl_label.move(self.width() - self.current_lvl_label.width() - 19,
                                    btn.pos().y() + btn.height() + 3)
        self.current_lvl_label.show()

        btn = IButton(self)
        btn.resize(46, 20)
        btn.move(self.width() - 7 - btn.width(), self.height() - btn.height() - 8)
        btn.setPathsToImages(r"assets/Hotkeys/down/image.png",
                             r"assets/Hotkeys/down/image_pressed.png",
                             r"assets/Hotkeys/hover.png")
        btn.clicked.connect(self.down_frame_lvl)


class Frame(QLabel):
    def __init__(self, index, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.index = index

        self.init_frame_ui(index)

        self.isNewScheme = False
        self.isLogistic = False
        self.isExistScheme = False
        self.isExistGroup = False

        self.group = []


    def set_flag_from_name(self, flag_name):
        if flag_name == "isNewScheme":
            self.isNewScheme = True
        elif flag_name == "isLogistic":
            self.isLogistic = True
        elif flag_name == "isExistScheme":
            self.isExistScheme = True
        elif flag_name == "isExistGroup":
            self.isExistGroup = True


    def get_current_flag(self):
        if self.isNewScheme:
            return "isNewScheme"
        elif self.isLogistic:
            return "isLogistic"
        elif self.isExistScheme:
            return "isExistScheme"
        elif self.isExistGroup:
            return "isExistGroup"
        else:
            return "None"


    def set_new_schemes(self):
        if self.GV.window.isLogisticCursor:
            self.isLogistic = True
            self.group.append(self.GV.blueprint.logistic_object)
            return

        self.isNewScheme = True
        self.group.append(self.GV.mouse_image.object)


    def set_exist_schemes(self):
        blueprint = self.GV.blueprint

        buffer = []
        if not blueprint.current_scheme is None:
            buffer.append(blueprint.current_scheme.get_scheme_data())
        for scheme in blueprint.selected_group:
            buffer.append(scheme.get_scheme_data())

        # Устанавливаем в группу значение в буфере
        self.group = buffer[:]

        if len(self.group) == 1:
            self.isExistScheme = True
            return

        point = QPoint(self.group[0].x, self.group[0].y)
        # Считаем центральную точку если группа
        selected_group = blueprint.selected_group
        if len(selected_group) > 0:
            max_x = self.group[0].x
            max_y = self.group[0].y
            min_x = self.group[0].x
            min_y = self.group[0].y
            for scheme in selected_group:
                pos_x = scheme.pos().x()
                pos_y = scheme.pos().y()
                if pos_x < min_x:
                    min_x = pos_x
                if pos_y < min_y:
                    min_y = pos_y
                if pos_x + scheme.width() > max_x:
                    max_x = pos_x + scheme.width()
                if pos_y + scheme.height() > max_y:
                    max_y = pos_y + scheme.height()
            point = ( QPoint(max_x, max_y) + QPoint(min_x, min_y) ) / 2


        # Считаем относительно расстояние всех объектов относительно этой точки
        for scheme_data in self.group:
            scheme_data.set_relative_pos(self.GV, point)
        self.isExistGroup = True


    def update_image(self):
        self.image.hide()
        self.count_label.hide()

        if not self.isNewScheme and not self.isLogistic and not self.isExistScheme and not self.isExistGroup:
            return
        if self.isNewScheme or self.isLogistic:
            object = self.group[0]
        elif self.isExistScheme:
            scheme_data = self.group[0]
            object = self.GV.database.get_object_from_name(scheme_data.object_name)
        else:
            object = None

        if object:
            pixmap = QPixmap(object.image)
        else:
            pixmap = QPixmap(r"assets\General\group_mouse_image.jpg")

        self.image.setPixmap(pixmap.scaled(self.image.size()))
        self.image.show()

        if self.isExistScheme or self.isExistGroup or self.isLogistic:
            if self.isLogistic:
                value = object.max_value
            else:
                value = len(self.group)
            self.count_label.setText(str(value))
            self.count_label.adjustSize()
            self.count_label.move(self.width() - self.count_label.width() - 10,
                                  self.height() - self.count_label.height() - 3)
            self.count_label.show()



    def set_frame_hotkey(self):
        blueprint = self.GV.blueprint
        if not self.GV.mouse_image.isVisible() and (blueprint.current_scheme is None and
            len(blueprint.selected_group) == 0) and not self.GV.window.isLogisticCursor:
            return

        self.group.clear()
        self.isNewScheme = False
        self.isLogistic = False
        self.isExistScheme = False
        self.isExistGroup = False

        if self.GV.mouse_image.isVisible() or self.GV.window.isLogisticCursor:
            self.set_new_schemes()

        elif blueprint.current_scheme or len(blueprint.selected_group) > 0:
            self.set_exist_schemes()

        self.update_image()


    def paste_from_hotkey(self):
        if self.isNewScheme:
            self.GV.mouse_image.start_image(self.group[0])
        elif self.isLogistic:
            # Если включен, то сначала отключаем
            if self.GV.window.isLogisticCursor:
                self.GV.blueprint.logistics_points = 0
                self.GV.blueprint.logistic_max_value = 0
                self.GV.blueprint.current_logistic.clear()
                self.GV.window.change_cursor_to_logistic(False)
            # Включаем
            self.GV.blueprint.logistic_object = self.group[0]
            self.GV.blueprint.logistics_points = 2
            self.GV.window.change_cursor_to_logistic(True)
        elif self.isExistScheme:
            self.GV.mouse_image.set_hotkey_value(self.index)

            scheme_data = self.group[0]
            object = self.GV.database.get_object_from_name(scheme_data.object_name)

            self.GV.mouse_image.start_image(object)
        elif self.isExistGroup:
            self.GV.group_mouse_image.index_group = self.index
            self.GV.group_mouse_image.start_group_image()


    def init_frame_ui(self, index):
        side = 90
        self.resize(side, side)
        pixmap = QPixmap(r"assets\Hotkeys\frame.png")
        self.setPixmap(pixmap.scaled(self.size()))
        self.show()

        index += 1
        if index == 10:
            index = 0
        index_label = QLabel(f"{index}", self)
        index_label.setFont(QFont("Arial", 12))
        index_label.adjustSize()
        index_label.move(6, 6)
        index_label.show()

        self.image = QLabel(self)
        self.image.resize(60, 54)
        self.image.move(15, 18)
        self.image.show()

        # pixmap = QPixmap(r"DataBase\01 Конструктор\image.png")
        # self.image.setPixmap(pixmap.scaled(self.image.size()))

        self.count_label = QLabel(f"", self)
        self.count_label.setFont(QFont("Arial", 10))
        self.count_label.adjustSize()
        self.count_label.move(self.width() - self.count_label.width() - 10,
                              self.height() - self.count_label.height() - 3)
        self.count_label.show()

        btn = QPushButton(self)
        btn.resize(self.size())
        btn.setStyleSheet("background-color: transparent; border: none;")
        btn.show()
        btn.clicked.connect(self.paste_from_hotkey)
