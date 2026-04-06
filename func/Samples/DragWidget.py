from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint

class DragWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.show()

        self.dragging = False
        self.offset = QPoint(0, 0)

        self.border = 700


    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton or event.button() == Qt.XButton2:
            self.dragging = True
            self.offset = event.pos()  # Сохраняем смещение курсора относительно виджета


    def mouseMoveEvent(self, event):
        if self.dragging:
            # Перемещаем виджет, добавляя смещение
            self.move(self.pos() + event.pos() - self.offset )

            border_distans = self.border
            x = self.pos().x()
            y = self.pos().y()
            if x > 0 + border_distans:
                self.move(border_distans, y)
            if x < - self.width() + self.parent.width() - border_distans:
                self.move(- self.width() + self.parent.width() - border_distans, y)
            x = self.pos().x()

            if y > 0 + border_distans:
                self.move(x, border_distans)
            if y < - self.height() + self.parent.height() - border_distans:
                self.move(x, - self.height() + self.parent.height() - border_distans)


    def moveFromChild(self, pos, offset):
        self.move( self.pos() + pos - offset )

        # Проверки на пересечения барьера
        border_distans = self.border
        x = self.pos().x()
        y = self.pos().y()
        if x > 0 + border_distans:
            self.move(border_distans, y)
        if x < - self.width() + self.parent.width() - border_distans:
            self.move(- self.width() + self.parent.width() - border_distans, y)
        x = self.pos().x()

        if y > 0 + border_distans:
            self.move(x, border_distans)
        if y < - self.height() + self.parent.height() - border_distans:
            self.move(x, - self.height() + self.parent.height() - border_distans)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton or event.button() == Qt.XButton2:
            self.dragging = False