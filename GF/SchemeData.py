from PySide6.QtCore import QPoint
from decimal import Decimal

class SchemeData():
    def __init__(self, original_id, object_name, count_batteries, current_recipe_index, CW):
        self.original_id = original_id
        self.object_name = object_name

        self.count_batteries = count_batteries
        self.current_recipe_index = current_recipe_index

        self.createWidget = CW

        self.output_objects_names = []

        self.input_schemes_ids = []
        self.output_schemes_ids = []

        self.output_objects_names_liquid = []

        self.input_schemes_ids_liquid = []
        self.output_schemes_ids_liquid = []

        self.x = 0
        self.y = 0

        self.relative_x = 0
        self.relative_y = 0


    def get_object(self, GV):
        object = GV.database.get_object_from_name(self.object_name)
        return object


    def load_from_dict(self, data_dict):
        for key, value in data_dict.items():
            setattr(self, key, value)


    def set_relative_pos(self, GV, point: QPoint):
        k = GV.scale.k
        x = point.x() / k
        y = point.y() / k
        self.relative_x = self.x / k - x
        self.relative_y = self.y / k - y


    def set_absolute_pos(self, point: QPoint):
        self.x = point.x()
        self.y = point.y()


    def set_output_objects_names(self, output_objects):
        self.output_objects_names.clear()
        for object in output_objects:
            self.output_objects_names.append(object.name)


    def set_inputs_outputs_ids(self, input_schemes, output_schemes):
        self.input_schemes_ids.clear()
        for scheme in input_schemes:
            self.input_schemes_ids.append(scheme.id)

        self.output_schemes_ids.clear()
        for scheme in output_schemes:
            self.output_schemes_ids.append(scheme.id)


    def set_output_objects_names_liquid(self, output_objects):
        self.output_objects_names_liquid.clear()
        for object in output_objects:
            self.output_objects_names_liquid.append(object.name)


    def set_inputs_outputs_ids_liquid(self, input_schemes, output_schemes):
        self.input_schemes_ids_liquid.clear()
        for scheme in input_schemes:
            self.input_schemes_ids_liquid.append(scheme.id)

        self.output_schemes_ids_liquid.clear()
        for scheme in output_schemes:
            self.output_schemes_ids_liquid.append(scheme.id)