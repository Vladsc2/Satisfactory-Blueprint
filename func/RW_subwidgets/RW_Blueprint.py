from func.Samples.DragWidget import DragWidget
from func.Samples.Background import Background
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QMouseEvent, QCursor
from PySide6.QtCore import Qt, QPoint, QRect
from func.Samples.SchemeLabel import SchemeLabel
from func.RW_subwidgets.PaintArea import PaintArea
from func.RW_subwidgets.PaintUpperArea import PaintUpperArea
from func.RW_subwidgets.ProductionArea import ProductionArea
from GF.DataBase import *


class Blueprint(DragWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.blueprint = self
        super().__init__(parent)
        self.parent = parent

        self.init_UI()

        self.schemes = []

        self.logistics_points = 0
        self.logistic_object = None
        self.current_logistic = []

        self.paint_area = PaintArea(GV, self)

        self.paint_upper_area = PaintUpperArea(GV, self)

        self.production_area = ProductionArea(GV, self)

        # Переменные для выделения
        self.start_point = None
        self.end_point = None
        self.is_selecting = False
        self.selected_group = []

        self.current_scheme = None
        self.current_comment = None

        self.free_index_object = 0

        # Для ctrl+C /ctrl+V
        self.buffer = []

        # Для работы групп
        self.index_hotkey = None

        # Для комментариев
        self.comments = []


    def update_size_from_config_and_zoom(self):
        k = self.GV.scale.k
        width = int(self.GV.config.blueprint_width * k)
        height = int(self.GV.config.blueprint_height * k)
        self.resize(width, height)


    def get_scheme_from_id(self, id):
        for scheme in self.schemes:
            if scheme.id == id:
                return scheme


    def paste_from_hotkey(self, index_hotkey):
        group = self.GV.hotkeys.frames[self.GV.hotkeys.current_index_frames][index_hotkey].group
        for data_scheme in group:
            cursor_pos_in_widget = self.mapFromGlobal(QCursor.pos())
            object = self.GV.database.get_object_from_name(data_scheme.object_name)

            scheme = SchemeLabel(self.GV, object, self.free_index_object, self)
            scheme.resize(object.scheme_width*self.GV.scale.k, object.scheme_height*self.GV.scale.k)
            scheme.move(cursor_pos_in_widget.x() + int(data_scheme.relative_x)*self.GV.scale.k,
                       cursor_pos_in_widget.y() + int(data_scheme.relative_y)*self.GV.scale.k)
            scheme.show()

            pixmap = QPixmap(object.scheme)
            scheme.setPixmap(pixmap.scaled(scheme.size()))


            scheme.count_batteries = data_scheme.count_batteries
            scheme.current_recipe_index = data_scheme.current_recipe_index

            scheme.createWidget = data_scheme.createWidget

            self.schemes.append(scheme)

            self.free_index_object += 1

            self.selected_group.append(scheme)

        self.GV.main_under_widget.selectGroup()
        self.paint_upper_area.raise_()
        self.production_area.tick()


    def paste_group(self, index_hotkey):
        self.selected_group.clear()
        if not index_hotkey is None:
            self.paste_from_hotkey(index_hotkey)
            return

        for data_scheme in self.buffer:
            cursor_pos_in_widget = self.mapFromGlobal(QCursor.pos())
            object = self.GV.database.get_object_from_name(data_scheme.object_name)

            scheme = SchemeLabel(self.GV, object, self.free_index_object, self)
            scheme.resize(object.scheme_width*self.GV.scale.k, object.scheme_height*self.GV.scale.k)
            scheme.move( cursor_pos_in_widget.x() + int(data_scheme.relative_x)*self.GV.scale.k,
                       cursor_pos_in_widget.y() + int(data_scheme.relative_y)*self.GV.scale.k )
            scheme.show()

            pixmap = QPixmap(object.scheme)
            scheme.setPixmap(pixmap.scaled(scheme.size()))


            scheme.count_batteries = data_scheme.count_batteries
            scheme.current_recipe_index = data_scheme.current_recipe_index

            scheme.createWidget = data_scheme.createWidget

            self.schemes.append(scheme)

            self.free_index_object += 1

            self.selected_group.append(scheme)

        self.GV.main_under_widget.selectGroup()
        self.paint_upper_area.raise_()
        self.GV.production_area.tick()


    def start_past_scheme(self):
        if len(self.buffer) == 0:
            return

        # Если объект один
        if len(self.buffer) == 1:
            scheme_data = self.buffer[0]
            object = self.GV.database.get_object_from_name(scheme_data.object_name)

            self.GV.window.mouse_image.isPaste = True
            self.GV.window.mouse_image.start_image(object)
            return

        self.GV.window.group_mouse_image.start_group_image()
        self.GV.historyManager.notSave()



    def copy_schemes(self):
        buffer = []
        if not self.current_scheme is None:
            buffer.append(self.current_scheme.get_scheme_data())
        for scheme in self.selected_group:
            buffer.append(scheme.get_scheme_data())
        if len(buffer) == 0:
            return

        # Очищаем и добавляем схемы в буфер
        self.buffer.clear()

        # Устанавливаем в blueprint.buffer значение в буфере
        self.buffer = buffer[:]

        k = self.GV.scale.k
        point = QPoint(self.buffer[0].x, self.buffer[0].y)
        # Считаем центральную точку если группа
        if len(self.selected_group) > 0:
            max_x = self.buffer[0].x
            max_y = self.buffer[0].y
            min_x = self.buffer[0].x
            min_y = self.buffer[0].y
            for scheme in self.selected_group:
                pos_x = scheme.pos().x()
                pos_y = scheme.pos().y()
                if pos_x < min_x:
                    min_x = pos_x
                if pos_y < min_y:
                    min_y = pos_y
                if pos_x + scheme.width() > max_x:
                    max_x = pos_x + scheme.width()
                if pos_y + scheme.height() > max_y:
                    max_y = pos_y + scheme.height()
            point = ( QPoint(max_x, max_y) + QPoint(min_x, min_y) ) / 2


        # Считаем относительно расстояние всех объектов относительно этой точки
        for scheme_data in self.buffer:
            scheme_data.set_relative_pos(self.GV, point)



    def del_selected_objects(self):
        # Если выбрана группа
        for scheme in self.selected_group:
            self.schemes.remove(scheme)
            scheme.delete_scheme()
        self.selected_group.clear()

        # Если выбран один виджет
        if not self.current_scheme is None:
            self.schemes.remove(self.current_scheme)
            self.current_scheme.delete_scheme()
            self.current_scheme = None

        # Если выбран комментарий
        if not self.current_comment is None:
            self.comments.remove(self.current_comment)
            self.current_comment.delete_comment()
            self.current_comment = None

        self.GV.production_area.tick()
        self.GV.main_under_widget.selectNone()
        self.GV.historyManager.notSave()


    def del_all_inputs(self, schemeLabel: SchemeLabel, shiftPressed):
        for scheme in schemeLabel.input_schemes:
            index = scheme.output_schemes.index(schemeLabel)
            scheme.output_objects.pop(index)

            scheme.output_schemes.remove(schemeLabel)
            scheme.free_output += 1

            schemeLabel.free_input += 1

        for scheme in schemeLabel.input_schemes_liquid:
            index = scheme.output_schemes_liquid.index(schemeLabel)
            scheme.output_objects.pop(index)

            scheme.output_schemes_liquid.remove(schemeLabel)
            scheme.free_output_liquid += 1

            schemeLabel.free_input_liquid += 1

        schemeLabel.input_schemes.clear()
        schemeLabel.input_schemes_liquid.clear()

        if not shiftPressed:
            self.GV.window.change_cursor_to_del_logistic_input(False)

        self.GV.production_area.tick()
        self.GV.historyManager.notSave()

    def del_all_output(self, schemeLabel: SchemeLabel, shiftPressed):
        count_outputs = 0
        for scheme in schemeLabel.output_schemes:
            scheme.input_schemes.remove(schemeLabel)
            scheme.free_input += 1

            schemeLabel.free_output += 1

        for scheme in schemeLabel.output_schemes_liquid:
            scheme.input_schemes_liquid.remove(schemeLabel)
            scheme.free_input_liquid += 1

            schemeLabel.free_output_liquid += 1

        schemeLabel.output_objects.clear()
        schemeLabel.output_schemes.clear()

        schemeLabel.output_objects_liquid.clear()
        schemeLabel.output_schemes_liquid.clear()

        if not shiftPressed:
            self.GV.window.change_cursor_to_del_logistic(False)

        self.GV.production_area.tick()
        self.GV.historyManager.notSave()



    def tie_liquid_points(self, schemeLabel, shiftPressed):
        # Если это output точка
        if self.logistics_points == 2 and schemeLabel.free_output_liquid == 0:
            return
        # Если это input точка
        if self.logistics_points == 1 and schemeLabel.free_input_liquid == 0:
            return

        self.current_logistic.append(schemeLabel)
        self.logistics_points -= 1
        if self.logistics_points == 0:
            self.current_logistic[0].free_output_liquid -= 1
            self.current_logistic[0].output_objects_liquid.append(self.logistic_object)

            self.current_logistic[1].free_input_liquid -= 1

            self.current_logistic[0].output_schemes_liquid.append(self.current_logistic[1])
            self.current_logistic[1].input_schemes_liquid.append(self.current_logistic[0])

            if not shiftPressed or self.current_logistic[0].free_output == 0:
                self.logistics_points = 2
                self.current_logistic.clear()
            else:
                self.logistics_points = 1
                self.current_logistic.pop(1)
                # self.GV.window.change_cursor_to_logistic(False)
                # self.logistic_object = None
            self.GV.production_area.tick()
            self.GV.historyManager.notSave()


    def tie_points(self, schemeLabel, shiftPressed):
        if len(self.current_logistic) == 1 and self.current_logistic[0] == schemeLabel:
            return

        if self.logistic_object.is_liquid:
            self.tie_liquid_points(schemeLabel, shiftPressed)
            return

        # Если это output точка
        if self.logistics_points == 2 and schemeLabel.free_output == 0:
            return

        # Если это input точка
        if self.logistics_points == 1 and schemeLabel.free_input == 0:
            return

        self.current_logistic.append(schemeLabel)
        self.logistics_points -= 1
        if self.logistics_points == 0:
            self.current_logistic[0].free_output -= 1
            self.current_logistic[0].output_objects.append(self.logistic_object)

            self.current_logistic[1].free_input -= 1

            self.current_logistic[0].output_schemes.append(self.current_logistic[1])
            self.current_logistic[1].input_schemes.append(self.current_logistic[0])


            if not shiftPressed or self.current_logistic[0].free_output == 0:
                self.logistics_points = 2
                self.current_logistic.clear()
            else:
                self.logistics_points = 1
                self.current_logistic.pop(1)
                # self.GV.window.change_cursor_to_logistic(False)
                # self.logistic_object = None
            self.GV.production_area.tick()
            self.GV.historyManager.notSave()


    def mousePressEvent(self, event: QMouseEvent):
        self.current_comment = None

        self.setFocus()
        # Отмена выделения объекта
        if event.button() == Qt.RightButton:
            self.current_scheme = None
            self.selected_group.clear()
            self.GV.main_under_widget.selectNone()
        # Отмены
        if event.button() == Qt.RightButton and self.logistics_points > 0:
            self.logistics_points = 0
            self.logistic_max_value = 0
            self.current_logistic.clear()
            self.GV.window.change_cursor_to_logistic(False)
        if event.button() == Qt.RightButton and self.GV.window.isDelLogisticCursor:
            self.GV.window.change_cursor_to_del_logistic(False)
        if event.button() == Qt.RightButton and self.GV.window.isDelLogisticCursorIn:
            self.GV.window.change_cursor_to_del_logistic_input(False)

        # Выделение области
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.is_selecting = True

        super().mousePressEvent(event)


    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_selecting:
            self.end_point = event.pos()
        super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.selectGroup()

        super().mouseReleaseEvent(event)


    def selectGroup(self):
        if self.start_point is None or self.end_point is None:
            self.is_selecting = False
            self.end_point = None
            self.start_point = None
            return

        # Очищаем группу
        self.selected_group.clear()
        # Создаем прямоугольник по 2м точкам
        rect = QRect(self.start_point, self.end_point)
        # Считаем новую группу
        for scheme in self.schemes:
            scheme_rect = scheme.geometry()
            if rect.intersects(scheme_rect):
                self.selected_group.append(scheme)
        # Если в группе 1 схема, то перенаправляем на соло
        if len(self.selected_group) == 1:
            self.current_scheme = self.selected_group[0]
            self.GV.main_under_widget.selectNone()
            self.GV.main_under_widget.selectScheme(self.current_scheme)
            self.selected_group.clear()
        elif len(self.selected_group) == 0:
            self.GV.main_under_widget.selectNone()
            self.current_scheme = None
        else:
            self.GV.main_under_widget.selectNone()
            self.current_scheme = None
            self.GV.main_under_widget.selectGroup()

        self.GV.schemes_group_scroll_area.set_schemes_btns(self.selected_group)
        # Сбрасываем переменные
        self.is_selecting = False
        self.end_point = None
        self.start_point = None


    def create_object(self, object: DataObject, pos_cursor_in_cell, isPaste=False):
        pos_cursor = pos_cursor_in_cell - self.pos()
        x = pos_cursor.x()
        y = pos_cursor.y()

        scheme = SchemeLabel(self.GV, object, self.free_index_object, self)
        scheme.resize(int(object.scheme_width)*self.GV.scale.k, int(object.scheme_height)*self.GV.scale.k)
        scheme.move(pos_cursor.x() - int(object.scheme_width)*self.GV.scale.k//2,
                   pos_cursor.y() - int(object.scheme_height)*self.GV.scale.k//2)
        scheme.show()

        pixmap = QPixmap(object.scheme)
        scheme.setPixmap(pixmap.scaled(scheme.size()))

        if len(object.recipes) == 1:
            scheme.current_recipe_index = 0

        if isPaste:
            scheme_data = self.buffer[0]
            count_batteries = scheme_data.count_batteries
            current_recipe_index = scheme_data.current_recipe_index

            scheme.count_batteries = count_batteries
            scheme.current_recipe_index = current_recipe_index

            scheme.createWidget = scheme_data.createWidget

        if not self.index_hotkey is None:
            scheme_data = self.GV.hotkeys.frames[self.GV.hotkeys.current_index_frames][self.index_hotkey].group[0]
            count_batteries = scheme_data.count_batteries
            current_recipe_index = scheme_data.current_recipe_index

            scheme.count_batteries = count_batteries
            scheme.current_recipe_index = current_recipe_index

            scheme.createWidget = scheme_data.createWidget

            self.index_hotkey = None


        self.schemes.append(scheme)

        self.free_index_object += 1

        self.GV.main_under_widget.selectScheme(scheme)

        self.paint_upper_area.raise_()

        self.GV.production_area.tick()



    def resize(self, w, h, firstStart=False):
        super().resize(w, h)
        if firstStart:
            return
        self.background.resize(w, h)
        self.back_cells.resize(w, h)
        self.back_cells.setPixmap(self.pixmap.scaled(self.size()))

        self.paint_area.resize(self.size())
        self.paint_upper_area.resize(self.size())
        self.production_area.resize(self.size())


    def lower_backs(self):
        self.back_cells.lower()
        self.background.lower()


    def init_UI(self):
        self.resize(self.GV.config.blueprint_width, self.GV.config.blueprint_height, True)
        self.move(- self.width() // 2 + self.parent.width() // 2,
                  - self.height() // 2 + self.parent.height() // 2)
        self.show()
        self.background = Background("255, 255, 250", self)

        cb = self.GV.control_bar
        cb.blueprint_width_line_edit.setText(str(self.width())+"px")
        cb.blueprint_height_line_edit.setText(str(self.height())+"px")

        self.back_cells = QLabel(self)
        self.back_cells.resize(self.size())
        self.pixmap = QPixmap(r"assets/Blueprint/cells.png")
        self.back_cells.setPixmap(self.pixmap.scaled(self.size()))
        self.back_cells.show()