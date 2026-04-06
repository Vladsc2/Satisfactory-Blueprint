from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtCore import QTimer, Qt, QPoint

class MouseImage(QLabel):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.mouse_image = self
        self.parent = parent
        super().__init__(parent)

        self.resize(300, 200)

        # Таймер для обновления картинки
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pos)
        self.timer.setInterval(1000//self.GV.config.hz_mouse_image)

        self.object = None

        self.isPaste = False
        self.isHotkey = False
        self.index_hotkey = 0


    def update_hz_mouse_image(self):
        if self.timer.isActive():
            self.timer.stop()
        self.timer.setInterval(1000//self.GV.config.hz_mouse_image)


    def update_pos(self):
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
            image_pos_inside = image_pos + QPoint(-self.GV.lw.width(), 0) + QPoint(self.width()//2, self.height()//2)

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
                if self.isHotkey:
                    self.GV.blueprint.index_hotkey = self.index_hotkey
                    self.index_hotkey = 0
                    self.isHotkey = False
                self.GV.blueprint.create_object(self.object, image_pos_inside, self.isPaste)
                self.GV.historyManager.notSave()

            if not (event.modifiers() == Qt.ShiftModifier):
                self.stop_image()

        elif event.button() == Qt.RightButton:
            self.stop_image()

        self.isPaste = False

        super().mousePressEvent(event)


    def start_image(self, object):
        pixmap = QPixmap(object.image)
        self.resize(object.dragging_width, object.dragging_height)
        self.setPixmap(pixmap.scaled(self.size()))
        self.timer.start()
        self.show()
        self.object = object

    def set_hotkey_value(self, index_hotkey):
        self.index_hotkey = index_hotkey
        self.isHotkey = True


    def stop_image(self):
        self.timer.stop()
        self.hide()
        self.object = None