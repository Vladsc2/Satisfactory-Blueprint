import os
import sys
from PySide6.QtCore import QProcess, Qt
from PySide6.QtGui import QKeyEvent

class OtherHotkeys():
    def __init__(self, GV):
        self.GV = GV


    def check_key(self, event: QKeyEvent):
        if event.key() == Qt.Key_D and event.modifiers() & Qt.ControlModifier:
            self.open_folder()
        if event.key() == Qt.Key_M:
            self.open_folder()
        elif event.key() == Qt.Key_BracketRight:
            self.restart_program()



    def restart_program(self):
        if self.GV.config.save_before_restart:
            self.GV.project.widget_save_as.save_project()

        exe_name = "SF Blueprints.exe"
        if os.path.exists(exe_name):
            process = QProcess()
            process.startDetached(exe_name)

        self.GV.exit_application(True)


    def open_folder(self):
        folder_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        process = QProcess()
        process.startDetached('explorer', [folder_path])