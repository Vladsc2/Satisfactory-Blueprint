import sys
import os
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QProcess

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Открыть Проводник")
        self.setGeometry(100, 100, 300, 100)

        layout = QVBoxLayout()

        self.button = QPushButton("Открыть Проводник")
        self.button.clicked.connect(self.open_explorer)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def open_explorer(self):
        # Получаем путь к директории, где находится исполняемый файл
        folder_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        # Создаем QProcess и запускаем проводник
        process = QProcess()
        process.startDetached('explorer', [folder_path])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())