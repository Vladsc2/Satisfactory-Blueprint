from PySide6.QtGui import QColor
from GF.Recipe import *
from GF.ResourcesDataBase import *
from GF.Constants import *

class DataBase():
    def __init__(self, GV):
        self.GV = GV
        GV.database = self

        self.resource_base = ResourcesDataBase()

        self.data_list = []

        self.load_data_base()

        self.load_custom_schemes()


    def load_custom_schemes(self):
        root = r"CustomSchemes"
        for dir_name in os.listdir(root):
            # Полный путь к текущей папке
            folder_path = os.path.join(root, dir_name)

            if not os.path.isdir(folder_path):
                continue

            with open(os.path.join(folder_path, "data.txt"), "r", encoding="utf-8") as file:
                lines = file.readlines()
                name = lines[0].split("=")[1].strip()
                category = lines[1].split("=")[1].strip()
                energy = Decimal(lines[2].split("=")[1].strip())
                count_input = Decimal(lines[3].split("=")[1].strip())
                count_output = Decimal(lines[4].split("=")[1].strip())
                count_input_liquid = Decimal(lines[5].split("=")[1].strip())
                count_output_liquid = Decimal(lines[6].split("=")[1].strip())
                type = lines[7].split("=")[1].strip()
                lvl = int(lines[8].split("=")[1].strip())

            scheme = os.path.join(folder_path, "scheme.png")
            image = os.path.join(folder_path, "image.png")

            if type == "logistic":

                with open(os.path.join(folder_path, "logistic.txt"), "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    max_value = Decimal(lines[0].split("=")[1].strip())
                    check = lines[1].split("=")[1].strip()
                    is_liquid = get_bool_from_int(lines[1].split("=")[1].strip())
                    q_color_red = Decimal(lines[2].split("=")[1].strip())
                    q_color_green = Decimal(lines[3].split("=")[1].strip())
                    q_color_blue = Decimal(lines[4].split("=")[1].strip())


                dataObject = LogisticObject(self.data_list, name, category,
                                    energy, count_input, count_output,
                                    count_input_liquid, count_output_liquid,
                                    scheme, image, lvl,
                                    max_value, QColor(q_color_red, q_color_green, q_color_blue),
                                    is_liquid)

            else:
                with open(os.path.join(folder_path, "sizes.txt"), "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    scheme_width = Decimal(lines[0].split("=")[1].strip())
                    scheme_height = Decimal(lines[1].split("=")[1].strip())
                    dragging_width = Decimal(lines[2].split("=")[1].strip())
                    dragging_height = Decimal(lines[3].split("=")[1].strip())


                dataObject = DataObject(self.data_list, name, category,
                                    energy, count_input, count_output,
                                    count_input_liquid, count_output_liquid,
                                    scheme, image, lvl)
                dataObject.set_scheme_size(scheme_width, scheme_height)
                dataObject.set_dragging_size(dragging_width, dragging_height)

                self.load_recipe_for_object(dataObject, folder_path)


    def load_data_base(self):
        root = r"DataBase"
        for dir_name in os.listdir(root):
            # Полный путь к текущей папке
            folder_path = os.path.join(root, dir_name)

            if not os.path.isdir(folder_path):
                continue

            with open(os.path.join(folder_path, "data.txt"), "r", encoding="utf-8") as file:
                lines = file.readlines()
                name = lines[0].split("=")[1].strip()
                category = lines[1].split("=")[1].strip()
                energy = Decimal(lines[2].split("=")[1].strip())
                count_input = Decimal(lines[3].split("=")[1].strip())
                count_output = Decimal(lines[4].split("=")[1].strip())
                count_input_liquid = Decimal(lines[5].split("=")[1].strip())
                count_output_liquid = Decimal(lines[6].split("=")[1].strip())
                type = lines[7].split("=")[1].strip()
                lvl = int(lines[8].split("=")[1].strip())

            scheme = os.path.join(folder_path, "scheme.png")
            image = os.path.join(folder_path, "image.png")

            if type == "logistic":

                with open(os.path.join(folder_path, "logistic.txt"), "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    max_value = Decimal(lines[0].split("=")[1].strip())
                    check = lines[1].split("=")[1].strip()
                    is_liquid = get_bool_from_int(lines[1].split("=")[1].strip())
                    q_color_red = Decimal(lines[2].split("=")[1].strip())
                    q_color_green = Decimal(lines[3].split("=")[1].strip())
                    q_color_blue = Decimal(lines[4].split("=")[1].strip())


                dataObject = LogisticObject(self.data_list, name, category,
                                    energy, count_input, count_output,
                                    count_input_liquid, count_output_liquid,
                                    scheme, image, lvl,
                                    max_value, QColor(q_color_red, q_color_green, q_color_blue),
                                    is_liquid)

            else:
                with open(os.path.join(folder_path, "sizes.txt"), "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    scheme_width = int(lines[0].split("=")[1].strip())
                    scheme_height = int(lines[1].split("=")[1].strip())
                    dragging_width = int(lines[2].split("=")[1].strip())
                    dragging_height = int(lines[3].split("=")[1].strip())


                dataObject = DataObject(self.data_list, name, category,
                                    energy, count_input, count_output,
                                    count_input_liquid, count_output_liquid,
                                    scheme, image, lvl)
                dataObject.set_scheme_size(scheme_width, scheme_height)
                dataObject.set_dragging_size(dragging_width, dragging_height)

                self.load_recipe_for_object(dataObject, folder_path)

    def load_recipe_for_object(self, object, folder_path):
        recipes_path = os.path.join(folder_path, "Recipes")
        for file_name in os.listdir(recipes_path):
            if file_name == "00 tooltip.txt":
                continue

            recipe_path = os.path.join(recipes_path, file_name)

            lines = []
            with open(recipe_path, "r", encoding="utf-8") as file:
                lines = file.readlines()


            types_input_list = []
            count_input_list = []
            types_output_list = []
            count_output_list = []
            wait_input_type = True
            wait_count = False


            for line in lines:
                if line == lines[0]:
                    lvl = int(line.split("=")[1])
                    continue
                if line == "\n":
                    continue
                if line[0] == "#" or (line[0] == "/" and line[1] == "/"):
                    continue

                if "===" in line:
                    wait_input_type = False
                    continue

                if wait_input_type:
                    if not wait_count:
                        types_input_list.append(self.resource_base.get_resource(line[:-1]))
                        wait_count = True
                    else:
                        if line[-1] == "\n":
                            line = line[:-1]
                        count_input_list.append(Decimal(line))
                        wait_count = False

                else:
                    if not wait_count:
                        types_output_list.append(self.resource_base.get_resource(line[:-1]))
                        wait_count = True
                    else:
                        if line[-1] == "\n":
                            line = line[:-1]
                        count_output_list.append(Decimal(line))
                        wait_count = False

            object.add_recipe(Recipe(lvl, types_input_list, count_input_list,
                                     types_output_list, count_output_list))



    def get_object_from_name(self, name):
        for object in self.data_list:
            if name == object.name:
                return object
        raise ObjectNotFound(f"По имени {name} не удалось найти объект в базе данных")



class DataObject():
    def __init__(self, data_list, name, category, energy, input_logistic, output_logistic,
                 input_logistic_liquid, output_logistic_liquid, scheme, image, lvl, type="block"):
        data_list.append(self)

        self.name = name
        self.category = category
        self.energy = energy

        # UI
        self.scheme = scheme
        self.image = image

        # Размеры объекта на схеме
        self.scheme_width = 180
        self.scheme_height = 120

        # Размеры картинки при переноске
        self.dragging_width = 230
        self.dragging_height = 165

        self.type = type

        self.input_logistic = input_logistic
        self.output_logistic = output_logistic

        self.input_logistic_liquid = input_logistic_liquid
        self.output_logistic_liquid = output_logistic_liquid

        self.recipes = []

        self.lvl = lvl


    def add_recipe(self, recipe):
        self.recipes.append(recipe)


    def set_scheme_size(self, width, height):
        self.scheme_width = width
        self.scheme_height = height


    def set_dragging_size(self, width, height):
        self.dragging_width = width
        self.dragging_height = height


class LogisticObject(DataObject):
    def __init__(self, data_list, name, category, energy, input_logistic, output_logistic,
                 input_logistic_liquid, output_logistic_liquid, scheme, image, lvl, max_value,
                 q_color, is_liquid):
        super().__init__(data_list, name, category, energy,
            input_logistic, output_logistic,
            input_logistic_liquid, output_logistic_liquid,
                         scheme, image, lvl, "logistic")

        self.max_value = max_value
        self.q_color = q_color
        self.is_liquid = is_liquid


class ObjectNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)  # Вызов конструктора родительского класса