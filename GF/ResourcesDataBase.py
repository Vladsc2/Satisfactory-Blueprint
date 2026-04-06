import os
from decimal import Decimal

ORE_IRON = "ore_iron"
ORE_COPPER = "ore_copper"

INGOT_IRON = "ingot_iron"
INGOT_COPPER = "ingot_copper"

class ResourcesDataBase():
    def __init__(self):

        self.resources = []

        self.load_all_data()

        self.create_tooltip_file()


    def load_all_data(self):
        root = r"DataBaseResources"
        for dir_name in os.listdir(root):
            # Полный путь к текущей папке
            folder_path = os.path.join(root, dir_name)

            with open(os.path.join(folder_path, "resource.txt"), "r", encoding="utf-8") as file:
                lines = file.readlines()
                name = lines[0].split("=")[1].strip()
                is_liquid = Decimal(lines[1].split("=")[1].strip())

            image = os.path.join(folder_path, "image.png")

            resource = Resource(name, image, is_liquid)

            self.resources.append(resource)



    def create_tooltip_file(self):
        # Формируем строки
        lines = ["Доступные ресурсы:\n"]
        index = 0
        s = ""
        for resource in self.resources:
            s += resource.name + ", "
            index += 1
            if index == 5:
                index = 0
                lines.append(s + "\n")
                s = ""
        lines.append(s + "\n")

        # Записываем в файлы рецептов всех схем
        root = r"DataBase"
        for file_name in os.listdir(root):
            # Полный путь к текущей папке
            folder_path = os.path.join(root, file_name)

            if not os.path.isdir(folder_path):
                continue
            if os.path.exists(os.path.join(folder_path, "logistic.txt")):
                continue

            with open(os.path.join(folder_path, os.path.join("Recipes", "00 tooltip.txt")),
                      "w", encoding="utf-8") as file:
                file.writelines(lines)





    def get_resource(self, resource_name):
        for resource in self.resources:
            if resource.name == resource_name:
                return resource
        raise ResourceNotFound(f"Не удалось найти ресурс {resource_name} в базе ресурсов")



class Resource():
    def __init__(self, name, image, is_liquid):
        self.name = name
        self.image = image
        self.is_liquid = is_liquid



class ResourceNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)  # Вызов конструктора родительского класса