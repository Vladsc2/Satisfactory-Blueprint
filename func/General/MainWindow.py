from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtGui import QIcon, QCursor, QKeyEvent
from PySide6.QtCore import Qt
from GF.Constants import *

from func.General.LWidget import LeftWidget
from func.General.RWidget import RightWidget
from func.General.MouseImage import MouseImage
from func.General.GroupMouseImage import GroupMouseImage
from func.Hotkeys.Hotkeys import Hotkeys
from func.RW_subwidgets.Scale import Scale
from func.SystemCameraBinds.System import CameraBindSystem
from func.Comment.Comment import Comment
from func.HistoryManager.HistoryManager import HistoryManager
from func.OtherHotkeys.OtherHotkeys import OtherHotkeys

import GF.Constants as constants


class MainWindow(QMainWindow):
    def __init__(self, GV):
        super().__init__()
        constants.MONITOR_WIDTH, constants.MONITOR_HEIGHT = self.screen().size().width(), self.screen().size().height()

        self.GV = GV
        GV.window = self

        self.setWindowTitle("Satisfactory Blueprints")
        self.setWindowIcon(QIcon(r"assets/General/icon.png"))

        self.resize(1600, 900)
        self.move(MONITOR_WIDTH // 2 - self.width() // 2,
                  MONITOR_HEIGHT // 2 - self.height() // 2 - 50)
        self.show()

        self.scale = Scale(GV)

        self.left_widget = LeftWidget(GV, self)
        self.right_widget = RightWidget(GV, self)

        self.showFullScreen()

        # Инициализируем картинку, привязанную к мыши
        self.mouse_image = MouseImage(GV, self)

        self.group_mouse_image = GroupMouseImage(GV, self)

        self.isLogisticCursor = False
        self.isDelLogisticCursor = False
        self.isDelLogisticCursorIn = False

        self.grey_mask = QLabel(self)
        self.grey_mask.resize(self.size())
        self.grey_mask.setStyleSheet(f"background-color: rgba(0, 0, 0, 0.1);")
        self.grey_mask.hide()

        self.hotkeys = Hotkeys(GV, self)

        self.cameraSystem = CameraBindSystem(GV)

        self.historyManager = HistoryManager(GV)

        self.others_hotkeys = OtherHotkeys(GV)


    def start_grey_mask(self):
        self.grey_mask.show()

    def stop_grey_mask(self):
        self.grey_mask.hide()


    def keyPressEvent(self, event: QKeyEvent):
        self.paste_hotkey(event)
        self.check_set_hotkey(event)
        self.select_hotkeys_lvl(event)

        self.cameraSystem.add_camera_bind(event)
        self.cameraSystem.set_camera_pos(event)

        self.historyManager.check_undo_redo(event)

        self.GV.control_project.check_control_projects_hotkeys(event)

        self.others_hotkeys.check_key(event)

        if event.key() == Qt.Key_C and event.modifiers() & Qt.ShiftModifier:
            Comment.create_comment(self.GV)

        if event.key() == Qt.Key_Delete:
            self.GV.blueprint.del_selected_objects()

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_C:
            print("Вызов функции копирования")
            self.GV.blueprint.copy_schemes()
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_V:
            print("Вызов функции вставки")
            self.GV.blueprint.start_past_scheme()


        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_H:
            print("Сохранение хоткеев по умолчанию")
            self.GV.hotkeys.save_hotkeys("Hotkeys")
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_P:
            print("Функция сохранения конфига")
            self.GV.config.save_config()

        if event.key() == Qt.Key_Equal:
            print("Zoom In")
            self.GV.scale.zoom_in()
        if event.key() == Qt.Key_Minus:
            print("Zoom Out")
            self.GV.scale.zoom_out()

        elif event.key() == Qt.Key_Escape:
            self.GV.exit_application()


    def select_hotkeys_lvl(self, event: QKeyEvent):
        if not event.modifiers() == Qt.ShiftModifier:
            return
        if event.key() == Qt.Key_Exclam:
            self.GV.hotkeys.select_lvl_hotkeys(1)
        elif event.key() == Qt.Key_QuoteDbl or event.key() == Qt.Key_At:
            self.GV.hotkeys.select_lvl_hotkeys(2)
        elif event.text() == "#" or event.text() == "№":
            self.GV.hotkeys.select_lvl_hotkeys(3)
        elif event.key() == Qt.Key_Dollar or event.key() == Qt.Key_Semicolon:
            self.GV.hotkeys.select_lvl_hotkeys(4)
        elif event.key() == Qt.Key_Percent:
            self.GV.hotkeys.select_lvl_hotkeys(5)
        elif event.key() == Qt.Key_Colon or event.key() == Qt.Key_AsciiCircum:
            self.GV.hotkeys.select_lvl_hotkeys(6)
        elif event.key() == Qt.Key_Ampersand or event.key() == Qt.Key_Question:
            self.GV.hotkeys.select_lvl_hotkeys(7)
        elif event.key() == Qt.Key_Asterisk:
            self.GV.hotkeys.select_lvl_hotkeys(8)
        elif event.key() == Qt.Key_ParenLeft:
            self.GV.hotkeys.select_lvl_hotkeys(9)
        elif event.key() == Qt.Key_ParenRight:
            self.GV.hotkeys.select_lvl_hotkeys(0)


    def paste_hotkey(self, event: QKeyEvent):
        if event.modifiers() == Qt.ControlModifier or event.modifiers() == Qt.ShiftModifier:
            return
        if event.key() == Qt.Key_1:
            self.GV.hotkeys.paste_hotkey(1)
        elif event.key() == Qt.Key_2:
            self.GV.hotkeys.paste_hotkey(2)
        elif event.key() == Qt.Key_3:
            self.GV.hotkeys.paste_hotkey(3)
        elif event.key() == Qt.Key_4:
            self.GV.hotkeys.paste_hotkey(4)
        elif event.key() == Qt.Key_5:
            self.GV.hotkeys.paste_hotkey(5)
        elif event.key() == Qt.Key_6:
            self.GV.hotkeys.paste_hotkey(6)
        elif event.key() == Qt.Key_7:
            self.GV.hotkeys.paste_hotkey(7)
        elif event.key() == Qt.Key_8:
            self.GV.hotkeys.paste_hotkey(8)
        elif event.key() == Qt.Key_9:
            self.GV.hotkeys.paste_hotkey(9)
        elif event.key() == Qt.Key_0:
            self.GV.hotkeys.paste_hotkey(0)


    def check_set_hotkey(self, event: QKeyEvent):
        if not event.modifiers() == Qt.ControlModifier:
            return
        if event.key() == Qt.Key_1:
            self.GV.hotkeys.add_hotkey(1)
        elif event.key() == Qt.Key_2:
            self.GV.hotkeys.add_hotkey(2)
        elif event.key() == Qt.Key_3:
            self.GV.hotkeys.add_hotkey(3)
        elif event.key() == Qt.Key_4:
            self.GV.hotkeys.add_hotkey(4)
        elif event.key() == Qt.Key_5:
            self.GV.hotkeys.add_hotkey(5)
        elif event.key() == Qt.Key_6:
            self.GV.hotkeys.add_hotkey(6)
        elif event.key() == Qt.Key_7:
            self.GV.hotkeys.add_hotkey(7)
        elif event.key() == Qt.Key_8:
            self.GV.hotkeys.add_hotkey(8)
        elif event.key() == Qt.Key_9:
            self.GV.hotkeys.add_hotkey(9)
        elif event.key() == Qt.Key_0:
            self.GV.hotkeys.add_hotkey(0)



    def reset_all_flags(self):
        self.isLogisticCursor = False
        self.isDelLogisticCursorIn = False
        self.isDelLogisticCursor = False


    def change_cursor_to_logistic(self, toLogistic):
        self.reset_all_flags()
        if toLogistic:
            self.setCursor(QCursor(Qt.PointingHandCursor))
            self.isLogisticCursor = True
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))
            self.isLogisticCursor = False


    def change_cursor_to_del_logistic_input(self, toDelLogistic):
        self.reset_all_flags()
        if toDelLogistic:
            self.setCursor(QCursor(Qt.ForbiddenCursor))
            self.isDelLogisticCursorIn = True
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))
            self.isDelLogisticCursorIn = False


    def change_cursor_to_del_logistic(self, toDelLogistic):
        self.reset_all_flags()
        if toDelLogistic:
            self.setCursor(QCursor(Qt.ForbiddenCursor))
            self.isDelLogisticCursor = True
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))
            self.isDelLogisticCursor = False



    def closeEvent(self, event):
        self.GV.exit_application()