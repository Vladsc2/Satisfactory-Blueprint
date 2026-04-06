from func.HistoryManager.HistoryMask import HistoryMask
from func.Samples.SchemeLabel import SchemeLabel
from PySide6.QtGui import QPixmap, QKeyEvent
from PySide6.QtCore import Qt
from func.Comment.Comment import Comment

class HistoryManager():
    def __init__(self, GV):
        self.GV = GV
        GV.historyManager = self

        self.maximum_undo = 50
        self.undo_array = []
        self.redo_array = []

        self.current_mask = None

        self.isWorking = self.GV.config.use_undo_system

        self.reset()


    def notSave(self):
        self.GV.project.isSaved = False
        self.add_undo_array()


    def load_current_mask(self):
        self.load_mask(self.current_mask)


    def reset(self):
        self.undo_array.clear()
        self.redo_array.clear()
        mask = HistoryMask(self.GV.blueprint)
        self.current_mask = mask


    def check_undo_redo(self, event: QKeyEvent):
        if not event.modifiers() & Qt.ControlModifier:
            return
        if event.key() == Qt.Key_Z:
            self.GV.project.isSaved = False
            self.undo()
        elif event.key() == Qt.Key_Y:
            self.GV.project.isSaved = False
            self.redo()


    def add_undo_array(self):
        if not self.isWorking:
            return

        bp = self.GV.blueprint

        if len(bp.schemes)+len(bp.comments) < 30:
            self.maximum_undo = self.GV.config.undo_limit
        elif len(bp.schemes)+len(bp.comments) < 50:
            self.maximum_undo = self.GV.config.undo_limit // 5 * 3
        elif len(bp.schemes)+len(bp.comments) < 100:
            self.maximum_undo = self.GV.config.undo_limit // 5
        else:
            self.maximum_undo = 5

        for i in range(len(self.undo_array)-self.maximum_undo):
            self.undo_array.pop(0)


        self.redo_array.clear()

        self.undo_array.append(self.current_mask)

        # Делаем слепок состояние
        mask = HistoryMask(bp)
        self.current_mask = mask

        if len(self.undo_array) > self.maximum_undo:
            self.undo_array.pop(0)


    def add_redo_array(self):
        mask = self.current_mask
        self.redo_array.append(mask)


    def clear_arrays(self):
        self.redo_array.clear()
        self.undo_array.clear()


    def redo(self):
        if len(self.redo_array) == 0:
            return

        self.undo_array.append(self.current_mask)

        mask = self.redo_array.pop(-1)
        self.current_mask = mask

        self.load_current_mask()


    def undo(self):
        if len(self.undo_array) == 0:
            return

        self.add_redo_array()

        self.current_mask = self.undo_array.pop(-1)
        self.load_current_mask()


    def load_mask(self, mask=None):
        if mask is None:
            mask = self.current_mask
        if mask is None:
            return


        bp = self.GV.blueprint

        # Удаляем старые схемы и комментарии
        for scheme in bp.schemes:
            scheme.deleteLater()
        bp.schemes.clear()
        for comment in bp.comments:
            comment.deleteLater()
        bp.comments.clear()

        # Очищаем все буферы
        self.GV.main_under_widget.selectNone()
        bp.current_scheme = None
        bp.current_comment = None
        bp.buffer.clear()


        # загружаем схемы
        max_id = 0
        for dataScheme in mask.saved_schemes:
            # Проверяем id
            if dataScheme.original_id > max_id:
                max_id = dataScheme.original_id

            # Получаем объект из data_scheme
            object = dataScheme.get_object(self.GV)

            # Создаем схему на blueprint
            scheme = SchemeLabel(self.GV, object, dataScheme.original_id, bp)
            scheme.resize(int(object.scheme_width)*self.GV.scale.k,
                          int(object.scheme_height)*self.GV.scale.k)
            scheme.move(dataScheme.x,
                       dataScheme.y)
            scheme.show()

            pixmap = QPixmap(object.scheme)
            scheme.setPixmap(pixmap.scaled(scheme.size()))

            scheme.count_batteries = dataScheme.count_batteries
            scheme.current_recipe_index = dataScheme.current_recipe_index

            scheme.createWidget = dataScheme.createWidget

            bp.schemes.append(scheme)

            # Устанавливаем output_objects
            for object_name in dataScheme.output_objects_names:
                output_object = self.GV.database.get_object_from_name(object_name)
                scheme.output_objects.append(output_object)

            for object_name in dataScheme.output_objects_names_liquid:
                output_object = self.GV.database.get_object_from_name(object_name)
                scheme.output_objects_liquid.append(output_object)

        bp.free_index_object = max_id + 1

        # Проходим по всем схемам в blueprint и устанавливаем связи
        data_schemes = mask.saved_schemes
        for i in range(len(data_schemes)):
            for id in data_schemes[i].output_schemes_ids:
                scheme = bp.schemes[i]
                output_scheme = bp.get_scheme_from_id(id)

                scheme.output_schemes.append(output_scheme)
                output_scheme.input_schemes.append(scheme)

            for id in data_schemes[i].output_schemes_ids_liquid:
                scheme = bp.schemes[i]
                output_scheme = bp.get_scheme_from_id(id)

                scheme.output_schemes_liquid.append(output_scheme)
                output_scheme.input_schemes_liquid.append(scheme)


        # Загружаем комментарии
        for dataComment in mask.saved_comments:
            # Создаем схему на blueprint
            comment = Comment(self.GV, bp)
            comment.text_layout = dataComment.text_layout

            comment.setLower = dataComment.setLower
            comment.set_Z_from_flag()

            comment.resize(dataComment.width, dataComment.height)
            comment.move(dataComment.x, dataComment.y)
            comment.show()

            comment.text.setText(dataComment.text)
            comment.text_color = dataComment.text_color
            comment.head_color = dataComment.head_color
            comment.body_color = dataComment.body_color
            comment.point_color = dataComment.point_color

            comment.resize_subwidgets()
            comment.set_pos_text_from_layout()

            bp.comments.append(comment)


        self.GV.blueprint.paint_upper_area.raise_()
        self.GV.production_area.tick()
        self.GV.main_under_widget.factory_info_widget.update_factory_info_widget()