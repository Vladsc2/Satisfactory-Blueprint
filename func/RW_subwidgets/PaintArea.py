from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QTimer, QPoint, QRect

class PaintArea(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(parent.size())
        self.move(0, 0)
        self.show()
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Таймер для отрисовки линий конвейеров
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(1000//self.GV.config.hz_conv_lines)
        self.timer.start()


    def update_hz_lines(self):
        self.timer.stop()
        self.timer.setInterval(1000//self.GV.config.hz_conv_lines)
        self.timer.start()


    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for scheme in self.parent().schemes:
            if len(scheme.output_schemes) == 0 and len(scheme.output_schemes_liquid) == 0:
                continue

            index = 0
            for out_scheme in scheme.output_schemes:
                pen = QPen(scheme.output_objects[index].q_color, 4*self.GV.scale.k)
                painter.setPen(pen)


                pos1 = scheme.pos() + QPoint(scheme.width() - scheme.width() // 5,
                        scheme.height() // 2 + self.get_offset(len(scheme.output_schemes
                                                + scheme.output_schemes_liquid),index, scheme))



                pos2 = out_scheme.pos() + QPoint(out_scheme.width() // 5,
                    out_scheme.height() // 2 + self.get_offset(len(out_scheme.input_schemes
                                                + scheme.input_schemes_liquid), index, out_scheme))

                index += 1

                painter.drawLine(pos1, pos2)


            # Для жидкостей
            index = 0
            for out_scheme in scheme.output_schemes_liquid:
                pen = QPen(scheme.output_objects_liquid[index].q_color, 6)
                painter.setPen(pen)


                pos1 = scheme.pos() + QPoint(scheme.width() - scheme.width() // 5,
                        scheme.height() // 2 + self.get_offset(len(scheme.output_schemes
                                                + scheme.output_schemes_liquid), index, scheme))



                pos2 = out_scheme.pos() + QPoint(out_scheme.width() // 5,
                    out_scheme.height() // 2 + self.get_offset(len(out_scheme.input_schemes
                                                + scheme.input_schemes_liquid), index, out_scheme))

                index += 1

                painter.drawLine(pos1, pos2)


        # Рисование выделения
        if self.parent().start_point and self.parent().end_point:
            painter.setPen(QPen(QColor(255, 140, 0), 2, Qt.DashLine))
            rect = QRect(self.parent().start_point, self.parent().end_point)
            painter.drawRect(rect.normalized())  # Рисуем выделенный прямоугольник







    def get_offset(self, len_, index, scheme):
        # Считаем смещение для точки исходя из: длинны массива и индекса элемента массива
        offset = 0
        delta = scheme.height() // 20
        if len_ == 2:
            if index == 0:
                offset = -delta
            elif index == 1:
                offset = delta


        elif len_ == 3:
            if index == 0:
                offset = -delta
            elif index == 1:
                offset = 0
            elif index == 2:
                offset = delta


        elif len_ == 4:
            if index == 0:
                offset = -delta*2
            elif index == 1:
                offset = -delta
            elif index == 2:
                offset = delta
            elif index == 3:
                offset = delta*2


        elif len_ == 5:
            if index == 0:
                offset = -delta*2
            elif index == 1:
                offset = -delta
            elif index == 2:
                offset = 0
            elif index == 3:
                offset = delta
            elif index == 4:
                offset = delta*2


        elif len_ == 6:
            if index == 0:
                offset = -delta*3
            elif index == 1:
                offset = -delta*2
            elif index == 2:
                offset = -delta
            elif index == 3:
                offset = delta
            elif index == 4:
                offset = delta*2
            elif index == 5:
                offset = delta*3


        elif len_ == 7:
            if index == 0:
                offset = -delta*3
            elif index == 1:
                offset = -delta*2
            elif index == 2:
                offset = -delta
            elif index == 3:
                offset = 0
            elif index == 4:
                offset = delta
            elif index == 5:
                offset = delta*2
            elif index == 6:
                offset = delta*3


        return offset