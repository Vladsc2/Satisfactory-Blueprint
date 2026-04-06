from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtCore import Qt, QTimer

class PaintUpperArea(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(parent.size())
        self.move(0, 0)
        self.show()
        self.setAttribute(Qt.WA_TransparentForMouseEvents)



    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Рисуем точки соединения
        if len(self.parent().current_logistic) != 0:
            if self.parent().logistic_object.is_liquid:
                color = QColor(0, 191, 255)
            else:
                color = QColor(255, 127, 80)

            for scheme in self.parent().current_logistic:
                pos_x = scheme.pos().x()
                pos_y = scheme.pos().y()
                pos_x += scheme.width() // 2
                pos_y += scheme.height() // 2

                painter.setPen(QPen(color, 1))
                painter.setBrush(QBrush(color))

                radius = 10*self.GV.scale.k
                center = (pos_x, pos_y)
                painter.drawEllipse(center[0] - radius, center[1] - radius, radius*2, radius*2)