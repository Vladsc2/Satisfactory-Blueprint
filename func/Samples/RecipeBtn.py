from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtGui import QFont, QPixmap

class RecipeBtn(QPushButton):
    def __init__(self, GV, parent):
        self.GV = GV

        super().__init__(parent)

        self.show()

        self.scheme = None
        self.object = None
        self.index_recipe = None

    def set_recipe(self, scheme, index):
        self.scheme = scheme
        self.object = scheme.object
        self.index_recipe = index


    def forming_ui(self):
        if self.object is None:
            return

        # Удаляем старые дочерние объекты
        for child in self.children():
            if child is not self:  # Чтобы не удалить сам виджет
                child.deleteLater()  # Запланировать удаление объекта

        # Если индекс is None, пишем что рецепт не установлен
        if self.index_recipe is None:
            label = QLabel("None", self)
            label.setFont(QFont("Arial", self.height() // 2))
            label.adjustSize()
            label.move(self.width() // 2 - label.width() // 2, self.height() // 2 - label.height() // 2)
            label.show()
            return
        recipe = self.object.recipes[self.index_recipe]

        # Вызывать после resize

        # Считаем border_x
        busy_width = 0
        image_width = 0
        distans = 10

        count_input_items = len(recipe.types_input_list)

        count_output_items = len(recipe.types_output_list)

        max_value = count_input_items + count_output_items

        if max_value == 1:
            font = QFont("Arial", self.height()//3)
            image_width = (  self.width() - (distans*max_value - 1)) // (max_value*2 + 1) - self.width() // 8
        elif max_value == 2:
            font = QFont("Arial", self.height()//4)
            image_width = (  self.width() - (distans*max_value - 1)) // (max_value*2 + 1)
        elif max_value == 3:
            font = QFont("Arial", self.height()//5)
            image_width = ( ( self.width() - (distans*max_value - 1)) // (max_value*2 + 1) )
        else:
            font = QFont("Arial", self.height()//6)
            image_width = ( ( self.width() - (distans*max_value - 1)) // (max_value*2 + 1) ) - self.width() // 30

        calc_label = QLabel("=>", self)
        calc_label.setFont(font)

        calc_label.adjustSize()

        # Считаем все тексты
        busy_width = calc_label.width()

        for i in range(count_input_items):
            number = recipe.count_input_list[i]
            calc_label.setText(str(number))
            calc_label.adjustSize()
            busy_width += calc_label.width()

        for i in range(count_output_items):
            number = recipe.count_output_list[i]
            calc_label.setText(str(number))
            calc_label.adjustSize()
            busy_width += calc_label.width()

        # Считаем сколько места занимают кнопки
        busy_width += image_width*max_value

        # Считаем дистанцию
        busy_width += distans * (max_value-1+3)

        calc_label.deleteLater()

        # Считаем свободное расстояние и border_x
        free_distans = self.width() - busy_width
        border_x = free_distans // 2

        offset_x = border_x - self.width() // 50
        offset_y = (self.height() - image_width) // 2
        for i in range(len(recipe.types_input_list)):
            image = QLabel(self)
            image.resize(image_width, image_width)
            image.move(offset_x, offset_y)
            image.show()
            pixmap = QPixmap(recipe.types_input_list[i].image)
            image.setPixmap(pixmap.scaled(image.size()))

            offset_x += image_width + distans

            value = recipe.count_input_list[i].normalize()
            label = QLabel(format(value, "f"), self)
            label.setFont(font)
            label.adjustSize()
            label.move(offset_x, self.height() // 2 - label.height() // 2)
            label.show()

            offset_x += label.width() + distans


        label = QLabel("=>", self)
        label.setFont(font)
        label.adjustSize()
        label.move(offset_x, self.height() // 2 - label.height() // 2)
        label.show()

        offset_x += label.width() + distans + distans


        for i in range(len(recipe.types_output_list)):
            image = QLabel(self)
            image.resize(image_width, image_width)
            image.move(offset_x, offset_y)
            image.show()
            pixmap = QPixmap(recipe.types_output_list[i].image)
            image.setPixmap(pixmap.scaled(image.size()))

            offset_x += image_width + distans

            value = recipe.count_output_list[i].normalize()
            label = QLabel(format(value, "f"), self)
            label.setFont(font)
            label.adjustSize()
            label.move(offset_x, self.height() // 2 - label.height() // 2)
            label.show()

            offset_x += label.width() + distans


