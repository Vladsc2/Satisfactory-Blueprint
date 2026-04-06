"""
    PySide6-6.5.3 PySide6-Addons-6.5.3 PySide6-Essentials-6.5.3 shiboken6-6.5.3 (pip install PySide6)
    screeninfo-0.8.1 (pip install screeninfo)
    Pillow
"""

import sys
from PySide6.QtWidgets import QApplication
from decimal import getcontext


def main():
    # Точность - до 2х знаков после запятой
    getcontext().prec = 3

    app = QApplication(sys.argv)
    from func.Project.Project import Project
    from GF.Config import Config
    from GF.GlobalVariables import GlobalVariables

    from GF.DataBase import DataBase

    from func.General.MainWindow import MainWindow

    # Инициализируем классы из GF
    GV = GlobalVariables()
    config = Config(GV)

    # Инициализируем базу данных
    database = DataBase(GV)

    window = MainWindow(GV)

    # Инициализируем проект
    project = Project(GV, window)

    # Загружаем хоткеи
    GV.hotkeys.load_hotkeys("Hotkeys")

    window.setFocus()

    sys.exit(app.exec())



if __name__ == "__main__":
    main()