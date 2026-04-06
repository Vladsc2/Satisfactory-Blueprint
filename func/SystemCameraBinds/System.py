from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QKeyEvent
from decimal import Decimal
import os
from GF.Constants import bool_from_str

class CameraBindSystem():
    def __init__(self, GV):
        self.GV = GV
        GV.cameraSystem = self

        self.f_keys = []
        self.init_keys_array()

        self.binds = []
        self.init_binds(12)


    def set_camera_pos(self, event: QKeyEvent):
        if event.modifiers() & Qt.ShiftModifier:
            return
        if not (event.key() in self.f_keys):
            return

        index = self.get_index_from_key(event.key())

        if not self.binds[index].isActivate:
            return

        pos = self.binds[index].getPos(self.GV)

        self.GV.blueprint.move(pos)


    def add_camera_bind(self, event: QKeyEvent):
        if not (event.modifiers() & (Qt.ShiftModifier | Qt.ControlModifier)):
            return
        if not (event.key() in self.f_keys):
            return


        index = self.get_index_from_key(event.key())
        pos = self.GV.blueprint.pos()

        self.binds[index].setNewPos(pos, self.GV)


    def get_index_from_key(self, key):
        if key == Qt.Key_F1:
            return 0
        elif key == Qt.Key_F2:
            return 1
        elif key == Qt.Key_F3:
            return 2
        elif key == Qt.Key_F4:
            return 3
        elif key == Qt.Key_F5:
            return 4
        elif key == Qt.Key_F6:
            return 5
        elif key == Qt.Key_F7:
            return 6
        elif key == Qt.Key_F8:
            return 7
        elif key == Qt.Key_F9:
            return 8
        elif key == Qt.Key_F10:
            return 9
        elif key == Qt.Key_F11:
            return 10
        elif key == Qt.Key_F12:
            return 11


    def load_binds(self, save_path):
        # Получаем путь к папке с сохранением настроек камеры
        camera_binds_dir = os.path.join(save_path, "camera")

        # Если папки не существует, то выходим
        if not os.path.exists(camera_binds_dir):
            return

        # Читаем файлик биндов
        lines = []
        binds_file = os.path.join(camera_binds_dir, "binds.txt")
        with open(binds_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Записываем данные в бинды
        index = 0
        for line in lines:
            if line == "\n":
                break

            line = line.split(",")

            activate = line[2].strip()
            activate = bool_from_str(activate)
            if not activate:
                index += 1
                continue

            x = line[0].strip()
            y = line[1].strip()
            self.binds[index].setNewPos( QPoint(int(x), int(y)) , self.GV)

            index += 1



    def save_binds(self, save_path):
        # Получаем путь к папке с сохранением настроек камеры
        camera_binds_dir = os.path.join(save_path, "camera")

        # Если папки не существует, то создаем
        if not os.path.exists(camera_binds_dir):
            os.mkdir(camera_binds_dir)

        # На всякий случай удаляем все файлы
        for file_name in os.listdir(camera_binds_dir):
            file_path = os.path.join(camera_binds_dir, file_name)
            os.remove(file_path)

        # В файлик binds.txt записываем данные биндов
        lines = []
        for bind in self.binds:
            s = str(int(bind.x)) + " , " + str(int(bind.y)) + " , " + str(bind.isActivate) + "\n"
            lines.append(s)
        binds_file = os.path.join(camera_binds_dir, "binds.txt")
        with open(binds_file, "w", encoding="utf-8") as file:
            file.writelines(lines)


    def init_keys_array(self):
        self.f_keys.append(Qt.Key_F1)
        self.f_keys.append(Qt.Key_F2)
        self.f_keys.append(Qt.Key_F3)
        self.f_keys.append(Qt.Key_F4)
        self.f_keys.append(Qt.Key_F5)
        self.f_keys.append(Qt.Key_F6)
        self.f_keys.append(Qt.Key_F7)
        self.f_keys.append(Qt.Key_F8)
        self.f_keys.append(Qt.Key_F9)
        self.f_keys.append(Qt.Key_F10)
        self.f_keys.append(Qt.Key_F11)
        self.f_keys.append(Qt.Key_F12)



    def init_binds(self, count_binds: int):
        for i in range(count_binds):
            self.binds.append(BindCamera())


class BindCamera():
    def __init__(self):
        self.isActivate = False
        self.x = Decimal("0")
        self.y = Decimal("0")

    def setNewPos(self, pos, GV):
        self.isActivate = True
        self.x = pos.x() / GV.scale.k
        self.y = pos.y() / GV.scale.k


    def getPos(self, GV):
        x = int(  Decimal(self.x) * Decimal(GV.scale.k)  )
        y = int(  Decimal(self.y) * Decimal(GV.scale.k)  )
        return QPoint(x, y)