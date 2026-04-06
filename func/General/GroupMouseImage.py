from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtCore import QTimer, Qt, QPoint

class GroupMouseImage(QLabel):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.group_mouse_image = self
        self.parent = parent
        super().__init__(parent)

        self.resize(300, 200)
        pixmap = QPixmap(r"assets/General/group_mouse_image.jpg")
        self.setPixmap(pixmap.scaled(self.size()))

        # Таймер для обновления картинки
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pos_group)
        self.timer.setInterval(1000//self.GV.config.hz_mouse_image)

        self.index_group = None


    def update_hz_group_image(self):
        if self.timer.isActive():
            self.timer.stop()
        self.timer.setInterval(1000//self.GV.config.hz_mouse_image)


    def update_pos_group(self):
        mouse_x = QCursor.pos().x()
        mouse_y = QCursor.pos().y()
        self.move(mouse_x - self.width() // 2,
                  mouse_y - self.height() // 2)



    def mousePressEvent(self, event):
        self.GV.blueprint.current_comment = None
        if event.button() == Qt.LeftButton:
            image_pos = self.pos()
            x = image_pos.x() + self.width() // 2
            y = image_pos.y() + self.height() // 2
            image_pos_inside = image_pos + QPoint(-self.GV.lw.width(), 0)

            # Проверяем пересечение с Blueprint
            rw_pos = self.GV.rw.pos()
            cell_blueprint_pos = self.GV.cell_blueprint.pos()
            cell_blueprint_pos += QPoint(rw_pos.x(), 0)

            x_intersection = False
            y_intersection = False
            if x > cell_blueprint_pos.x() and x < cell_blueprint_pos.x() + self.GV.cell_blueprint.width():
                x_intersection = True
            if y > cell_blueprint_pos.y() and y < cell_blueprint_pos.y() + self.GV.cell_blueprint.height():
                y_intersection = True

            if x_intersection and y_intersection:
                self.GV.blueprint.paste_group(self.index_group)
                self.GV.historyManager.notSave()

            if not (event.modifiers() == Qt.ShiftModifier):
                self.stop_group_image()

        elif event.button() == Qt.RightButton:
            self.stop_group_image()
        super().mousePressEvent(event)
        self.index_group = None


    def start_group_image(self):
        self.timer.start()
        self.show()


    def stop_group_image(self):
        self.timer.stop()
        self.hide()