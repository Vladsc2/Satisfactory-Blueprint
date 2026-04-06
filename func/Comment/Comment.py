from PySide6.QtWidgets import QLabel, QWidget, QPushButton
from PySide6.QtCore import QPoint, Qt, QSize
from PySide6.QtGui import QCursor, QFont
from func.Comment.CommentData import CommentData

class Comment(QLabel):
    def __init__(self, GV, parent):
        super().__init__(parent)
        self.parent = parent
        self.GV = GV
        k = self.GV.scale.k

        self.setLower = True

        conf = GV.config
        self.text_layout = conf.comment_standard_layout
        self.text_color = conf.comment_standard_text_color
        self.head_color = conf.comment_standard_head_color
        self.body_color = conf.comment_standard_body_color
        self.point_color = conf.comment_standard_point_color
        self.standard_font_size = 30

        self.resize(int(400 * k), int(200 * k))
        self.show()

        self.min_width = 50
        self.min_height = 80

        # Для конфигурации скейла
        self.scale_point_size = 15

        # Для реализации скейла
        self.is_resizing = False
        self.last_mouse_position = QPoint()
        self.old_size = QSize(0, 0)

        # Для реализации перетаскивания
        self.canDragging = True
        self.dragging = False
        self.offset = QPoint(0, 0)
        self.old_pos = QPoint(0, 0)

        # Для перетаскивания родительского виджета
        self.parent_dragging = False
        self.offset_parent = QPoint(0, 0)

        # Опускаем на самое дно
        self.lower()
        GV.blueprint.lower_backs()

        # Создаем подвиджеты
        self.nameWidget = QWidget(self)
        self.nameWidget.resize(self.width(), 80)
        self.nameWidget.move(0, 0)
        self.nameWidget.setStyleSheet(f"background-color: {self.head_color};")
        self.nameWidget.show()

        self.text = QLabel(self)
        self.text.setFont(QFont("Arial", int(self.standard_font_size * k) ))
        self.text.setText("Комментарий")
        self.text.adjustSize()
        self.set_pos_text_from_layout()
        self.text.setStyleSheet(f"color: {self.text_color}; background-color: rgba(0, 0, 0, 0);")
        self.text.show()

        self.contentSubwidget = QWidget(self)
        self.contentSubwidget.resize(self.width(), self.height() - self.nameWidget.height())
        self.contentSubwidget.move(0, self.nameWidget.height())
        self.contentSubwidget.setStyleSheet(f"background-color: {self.body_color};")
        self.contentSubwidget.show()

        # Точка для скейла
        self.point = QLabel(self)
        self.point.resize(int(self.scale_point_size * k), int(self.scale_point_size * k))
        self.point.setStyleSheet(f"background-color: {self.point_color};")
        self.point.move(self.width() - self.point.width(), self.height() - self.point.height())
        self.point.show()

        self.resize_subwidgets()


    @staticmethod
    def create_comment(GV):
        # Получаем коэффициент размера
        k = GV.scale.k

        # Сразу инициализируем размеры комментария
        width = 400 * k
        height = 200 * k

        # Получаем положение курсора
        screen_pos = QCursor.pos()
        # Получаем позицию blueprint
        blueprint_pos = GV.blueprint.pos()
        # Считаем позицию для создания комментария
        pos = QPoint(
            screen_pos.x() - blueprint_pos.x() - GV.lw.width() - width // 2,
            screen_pos.y() - blueprint_pos.y() - height // 2
        )

        # Создаем комментарий
        comment = Comment(GV, GV.blueprint)
        comment.move(pos)
        GV.blueprint.comments.append(comment)

        GV.historyManager.notSave()


    def get_comment_data(self):
        commentData = CommentData(self.text.text(), self.text_layout, self.setLower)
        commentData.set_pos(self.pos())
        commentData.set_size(self.size())
        commentData.text_color = self.text_color
        commentData.head_color = self.head_color
        commentData.body_color = self.body_color
        commentData.point_color = self.point_color
        return commentData


    def update_style_sheet(self):
        self.text.setStyleSheet(f"color: {self.text_color}; background-color: rgba(0, 0, 0, 0);")
        self.nameWidget.setStyleSheet(f"background-color: {self.head_color};")
        self.contentSubwidget.setStyleSheet(f"background-color: {self.body_color};")
        self.point.setStyleSheet(f"background-color: {self.point_color};")


    def set_pos_text_from_layout(self):
        font = QFont("Arial", int(self.standard_font_size * self.GV.scale.k))
        self.text.setFont(font)
        self.text.adjustSize()

        if self.text_layout == "left":
            self.text.move(int(10 * self.GV.scale.k), self.nameWidget.height() // 2 - self.text.height() // 2)
        elif self.text_layout == "center":
            self.text.move(self.width() // 2 - self.text.width() // 2,
                           self.nameWidget.height() // 2 - self.text.height() // 2)
        elif self.text_layout == "right":
            self.text.move(self.width() - self.text.width() - int(10 * self.GV.scale.k),
                           self.nameWidget.height() // 2 - self.text.height() // 2)


    def resize_subwidgets(self):
        self.nameWidget.resize(self.width(), 80 * self.GV.scale.k)

        self.contentSubwidget.resize(self.width(), self.height() - self.nameWidget.height())
        self.contentSubwidget.move(0, self.nameWidget.height())

        k = self.GV.scale.k
        self.point.resize(int(self.scale_point_size * k), int(self.scale_point_size * k))
        self.point.move(self.width() - self.point.width(), self.height() - self.point.height())


    def delete_comment(self):
        self.deleteLater()


    def set_Z_from_flag(self):
        if self.setLower:
            self.lower()
            self.GV.blueprint.lower_backs()
        else:
            self.raise_()
            self.parent.paint_upper_area.raise_()


    # Те же методы, что и SchemeLabel
    def mousePressEvent(self, event):
        # Очищаем выделение
        if not self in self.parent.selected_group:
            self.parent.selected_group.clear()
        if event.button() == Qt.RightButton:
            self.GV.blueprint.current_scheme = None
            self.GV.blueprint.selected_group.clear()
            self.GV.main_under_widget.selectNone()


        # Очищаем логистику и прочее
        if event.button() == Qt.RightButton and self.GV.window.isLogisticCursor:
            self.GV.blueprint.logistics_points = 0
            self.GV.blueprint.logistic_max_value = 0
            self.GV.blueprint.current_logistic.clear()
            self.GV.window.change_cursor_to_logistic(False)
            return

        if event.button() == Qt.RightButton and self.GV.window.isDelLogisticCursor:
            self.GV.window.change_cursor_to_del_logistic(False)
        if event.button() == Qt.RightButton and self.GV.window.isDelLogisticCursorIn:
            self.GV.window.change_cursor_to_del_logistic_input(False)

        # Само перетаскивание виджета и поля
        if ( event.button() == Qt.LeftButton and self.canDragging and not self.is_under_widget(event.pos()) and not
            self.is_in_resize_area(event.pos()) ):
            # Записываем в current_comment
            self.parent.current_comment = self
            self.GV.main_under_widget.selectComment(self)

            self.dragging = True
            self.offset = event.pos()  # Сохраняем смещение курсора относительно виджета
            self.old_pos = self.pos()
            self.set_Z_from_flag()


        if event.button() == Qt.MiddleButton or event.button() == Qt.XButton2:
            self.parent_dragging = True
            self.offset_parent = event.pos() + self.pos()

        # Для изменения размеров
        if event.button() == Qt.LeftButton and self.is_in_resize_area(event.pos()):
            self.is_resizing = True
            self.last_mouse_position = event.globalPos()  # Сохраняем глобальную позицию мыши
            self.old_size = self.size()

        # Выделение группы
        if not self.is_in_resize_area(event.pos()) and self.is_under_widget(event.pos()) and event.button()==Qt.LeftButton:
            self.GV.blueprint.start_point = event.pos() + self.pos()
            self.GV.blueprint.is_selecting = True



    def mouseMoveEvent(self, event):
        if self.parent_dragging:
            self.parent.moveFromChild(self.pos() + event.pos(), self.offset_parent)


        if self.is_resizing:
            # Вычисляем разницу между текущей и последней позицией мыши
            delta = event.globalPos() - self.last_mouse_position
            new_width = self.width() + delta.x()
            new_height = self.height() + delta.y()

            k = self.GV.scale.k
            if new_width < self.min_width * k:
                new_width = self.min_width * k
            if new_height < self.min_height * k:
                new_height = self.min_height * k

            self.resize(new_width, new_height)  # Устанавливаем новый размер виджета
            self.last_mouse_position = event.globalPos()  # Обновляем последнюю позицию мыши

            self.point.move(self.width() - self.point.width(),
                            self.height() - self.point.height())
            self.resize_subwidgets()


        if self.dragging:
            # Перемещаем виджет, добавляя смещение
            self.move(self.pos() + event.pos() - self.offset )

            x = self.pos().x()
            y = self.pos().y()
            if x < 0:
                self.move(0, y)
            if x > self.parent.width() - self.width():
                self.move(self.parent.width() - self.width(), y)
            x = self.pos().x()

            if y < 0 :
                self.move(x, 0)
            if y > self.parent.height() - self.height():
                self.move(x, self.parent.height() - self.height())

        if self.GV.blueprint.is_selecting:
            self.GV.blueprint.end_point = event.pos() + self.pos()


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            self.GV.production_area.tick()
            if self.old_pos != self.pos():
                self.GV.historyManager.notSave()

        if event.button() == Qt.MiddleButton or event.button() == Qt.XButton2:
            self.parent_dragging = False

        if event.button() == Qt.LeftButton and self.is_resizing:
            self.is_resizing = False
            self.set_pos_text_from_layout()
            if self.size() != self.old_size:
                self.GV.historyManager.notSave()


        if self.GV.blueprint.is_selecting:
            self.GV.blueprint.selectGroup()



    def is_in_resize_area(self, pos):
        # Проверяем, находится ли курсор в правом нижнем углу виджета
        k = self.GV.scale.k
        return pos.x() >= self.width() - self.scale_point_size*k and pos.y() >= self.height() - self.scale_point_size*k


    def is_under_widget(self, pos):
        return pos.y() >= self.nameWidget.height() and not self.is_in_resize_area(pos)