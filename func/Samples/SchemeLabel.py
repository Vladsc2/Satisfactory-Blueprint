from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QPoint
from GF.SchemeData import SchemeData

class SchemeLabel(QLabel):
    def __init__(self, GV, object, id, parent):
        super().__init__(parent)
        self.parent = parent

        self.GV = GV

        self.object = object
        self.id = id
        self.count_batteries = 0
        self.current_recipe_index = None
        self.createWidget = GV.config.default_flag_create_widget

        # Для реализации перетаскивания
        self.canDragging = True
        self.dragging = False
        self.offset = QPoint(0, 0)
        self.old_pos = QPoint(0, 0)

        # Для перетаскивания родительского виджета
        self.parent_dragging = False
        self.offset_parent = QPoint(0, 0)


        self.free_output = object.output_logistic
        self.free_input = object.input_logistic

        # Ресурсы внутри схемы
        self.types_resources_input = []
        self.count_resources_input = []
        self.types_resources_output = []
        self.count_resources_output = []

        # Для реализации логистики
        self.output_objects = []

        self.output_schemes = []
        self.input_schemes = []


        # Для логистики жидкостей
        self.free_output_liquid = object.output_logistic_liquid
        self.free_input_liquid = object.input_logistic_liquid

        self.output_objects_liquid = []

        self.output_schemes_liquid = []
        self.input_schemes_liquid = []

        # Жидкости внутри схемы
        self.types_resources_input_liquid = []
        self.count_resources_input_liquid = []
        self.types_resources_output_liquid = []
        self.count_resources_output_liquid = []


    def get_scheme_data(self):
        scheme_data = SchemeData(self.id, self.object.name, self.count_batteries,
                                 self.current_recipe_index, self.createWidget)
        scheme_data.set_absolute_pos(self.pos())
        return scheme_data


    def get_scheme_data_save(self):
        scheme_data = SchemeData(self.id, self.object.name, self.count_batteries,
                                 self.current_recipe_index, self.createWidget)
        scheme_data.set_absolute_pos(self.pos())
        scheme_data.set_output_objects_names(self.output_objects)
        scheme_data.set_inputs_outputs_ids(self.input_schemes, self.output_schemes)
        scheme_data.set_output_objects_names_liquid(self.output_objects_liquid)
        scheme_data.set_inputs_outputs_ids_liquid(self.input_schemes_liquid,
                                                  self.output_schemes_liquid)
        return scheme_data


    def delete_scheme(self):
        for scheme in self.output_schemes:
            scheme.free_input += 1
            scheme.input_schemes.remove(self)

        for scheme in self.output_schemes_liquid:
            scheme.free_input_liquid += 1
            scheme.input_schemes_liquid.remove(self)

        for scheme in self.input_schemes:
            index = scheme.output_schemes.index(self)
            scheme.output_objects.pop(index)

            scheme.free_output += 1
            scheme.output_schemes.remove(self)

        for scheme in self.input_schemes_liquid:
            index = scheme.output_schemes_liquid.index(self)
            scheme.output_objects_liquid.pop(index)

            scheme.free_output_liquid += 1
            scheme.output_schemes_liquid.remove(self)


        self.deleteLater()


    # Реализация перетаскивания
    def mousePressEvent(self, event):
        self.parent.current_comment = None

        if not self in self.parent.selected_group:
            self.parent.selected_group.clear()
        if event.button() == Qt.RightButton:
            self.GV.blueprint.current_scheme = None
            self.GV.blueprint.selected_group.clear()
            self.GV.main_under_widget.selectNone()

        if event.button() == Qt.LeftButton:
            if not self in self.parent.selected_group:
                self.parent.current_scheme = self
                self.GV.main_under_widget.selectScheme(self)
        if event.button() == Qt.LeftButton and self.GV.window.isLogisticCursor:
            self.GV.blueprint.tie_points(self, event.modifiers() == Qt.ShiftModifier)
            return
        if event.button() == Qt.RightButton and self.GV.window.isLogisticCursor:
            self.GV.blueprint.logistics_points = 0
            self.GV.blueprint.logistic_max_value = 0
            self.GV.blueprint.current_logistic.clear()
            self.GV.window.change_cursor_to_logistic(False)
            return
        if event.button() == Qt.LeftButton and self.GV.window.isDelLogisticCursor:
            self.GV.blueprint.del_all_output(self, event.modifiers() == Qt.ShiftModifier)
            return
        if event.button() == Qt.LeftButton and self.GV.window.isDelLogisticCursorIn:
            self.GV.blueprint.del_all_inputs(self, event.modifiers() == Qt.ShiftModifier)
            return
        if event.button() == Qt.RightButton and self.GV.window.isDelLogisticCursor:
            self.GV.window.change_cursor_to_del_logistic(False)
        if event.button() == Qt.RightButton and self.GV.window.isDelLogisticCursorIn:
            self.GV.window.change_cursor_to_del_logistic_input(False)

        if event.button() == Qt.LeftButton and self.canDragging:
            self.dragging = True
            self.offset = event.pos()  # Сохраняем смещение курсора относительно виджета
            self.raise_()
            self.parent.paint_upper_area.raise_()
            self.old_pos = self.pos()

        if event.button() == Qt.MiddleButton or event.button() == Qt.XButton2:
            self.parent_dragging = True
            self.offset_parent = event.pos() + self.pos()



    def mouseMoveEvent(self, event):
        if self.parent_dragging:
            self.parent.moveFromChild(self.pos() + event.pos(), self.offset_parent)


        if self.dragging:
            if self in self.parent.selected_group:
                for scheme in self.parent.selected_group:
                    scheme.move(scheme.pos() + event.pos() - self.offset )

                    x = scheme.pos().x()
                    y = scheme.pos().y()
                    if x < 0:
                        scheme.move(0, y)
                    if x > scheme.parent.width() - scheme.width():
                        scheme.move(scheme.parent.width() - scheme.width(), y)
                    x = scheme.pos().x()

                    if y < 0 :
                        scheme.move(x, 0)
                    if y > scheme.parent.height() - scheme.height():
                        scheme.move(x, scheme.parent.height() - scheme.height())

                return
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


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            self.GV.production_area.tick()
            if self.old_pos != self.pos():
                self.GV.historyManager.notSave()

        if event.button() == Qt.MiddleButton or event.button() == Qt.XButton2:
            self.parent_dragging = False