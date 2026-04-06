from PySide6.QtWidgets import QWidget, QLabel
from GF.Constants import *
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt, QTimer
from func.Samples.SchemeLabel import SchemeLabel
from decimal import Decimal
from GF.Constants import get_bool_from_int

class ProductionArea(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.production_area = self
        super().__init__(parent)

        self.resize(parent.size())
        self.move(0, 0)
        self.show()
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.count_schemes = 0
        self.widgets = []

        self.sorted_schemes = []

        config = self.GV.config
        self.isSimpleCraft = config.flag_simple_craft
        self.isPrintCurrent = config.flag_print_current
        self.isPrintTypes = config.flag_print_types
        self.isPrintLogistic = config.flag_print_logistics
        self.isPrintTypesLogistic = config.flag_print_types_logistics

        self.font = QFont("Arial", 20)


    def tick(self):
        # Удаляем старые виджеты
        for widget in self.widgets:
            widget.deleteLater()
        self.widgets.clear()

        if len(self.parent().schemes) == 0:
            return
        if not self.isSimpleCraft and not self.isPrintCurrent and not self.isPrintTypes\
                and not self.isPrintLogistic and not self.isPrintTypesLogistic:
            return

        # Формируем отсортированный по позиции x массив схем
        self.sort_schemes()

        # Запускаем pulse для формирования ресурсов
        self.pulse()

        # Рисуем для логистики кол-во ресурсов
        self.create_logistic_widgets()

        # Рисуем для обычных схем рецепт и кол-во ресурсов
        self.create_new_widgets()



    def create_logistic_widgets(self):
        for scheme in self.sorted_schemes:
            if not scheme.createWidget:
                continue

            # Если не логистика - то мимо
            if scheme.object.category != "logistics" and scheme.object.category != "storage":
                continue
            # Если нет входящего сигнала - то тоже мимо
            if len(scheme.types_resources_input) == 0 and len(scheme.types_resources_input_liquid) == 0:
                continue

            # Формируем надпись
            s = ""
            if self.isPrintLogistic:
                if scheme.object.name == "Соединитель" or scheme.object.name == "Liquid 3->1":
                    max_value = Decimal("0")
                    for i in range(len(scheme.count_resources_input)):
                        count = scheme.count_resources_input[i]
                        count = count.normalize()
                        s += format(count, "f")
                        max_value += scheme.count_resources_input[i]
                        if i != range(len(scheme.count_resources_input))[-1]:
                            s += ", "
                    for i in range(len(scheme.count_resources_input_liquid)):
                        count = scheme.count_resources_input_liquid[i]
                        count = count.normalize()
                        s += format(count, "f")
                        max_value += scheme.count_resources_input_liquid[i]
                        if i != range(len(scheme.count_resources_input_liquid))[-1]:
                            s += ", "

                    s += f" => " + format(max_value.normalize(), 'f')

                elif (scheme.object.name == "Разветвитель" or scheme.object.name == "Liquid 1->3" or
                      scheme.object.name == "Разветвитель 1->5"):
                    if len(scheme.count_resources_input) > 0:
                        value = scheme.count_resources_input[0]
                        count_output = len(scheme.output_schemes) if len(scheme.output_schemes) > 0 else 1
                        del_value = scheme.count_resources_input[0] / count_output
                    else:
                        value = scheme.count_resources_input_liquid[0]
                        count_output = len(scheme.output_schemes_liquid) if len(scheme.output_schemes_liquid) > 0 else 1
                        del_value = scheme.count_resources_input_liquid[0] / count_output
                    value = value.normalize()
                    s += format(value, "f")
                    s += " => "

                    for i in range(len(scheme.output_schemes)):
                        count = del_value
                        count = count.normalize()
                        s += format(count, "f")
                        if i != range(len(scheme.output_schemes))[-1]:
                            s += ", "
                    for i in range(len(scheme.output_schemes_liquid)):
                        count = del_value
                        count = count.normalize()
                        s += format(count, "f")
                        if i != range(len(scheme.output_schemes_liquid))[-1]:
                            s += ", "

                elif scheme.object.category == "storage":
                    for i in range(len(scheme.count_resources_input)):
                        count = scheme.count_resources_input[i]
                        count = count.normalize()
                        s += format(count, "f")
                        if i != range(len(scheme.count_resources_input))[-1]:
                            s += ", "
                    for i in range(len(scheme.count_resources_input_liquid)):
                        count = scheme.count_resources_input_liquid[i]
                        count = count.normalize()
                        s += format(count, "f")
                        if i != range(len(scheme.count_resources_input_liquid))[-1]:
                            s += ", "


            # Создаем виджет
            widget = QWidget(self.parent())

            label = QLabel(s, widget)
            label.setFont(QFont("Arial", 18*self.GV.scale.k))
            label.adjustSize()
            label.move(20, 10)
            label.show()

            plus_height = 0
            width = label.width() + 40
            if self.isPrintTypesLogistic:
                btn_size = 34*self.GV.scale.k
                distans = 15
                border_x = ( width - btn_size*( len(scheme.types_resources_input) + len(scheme.types_resources_input_liquid))
                             - distans*( len(scheme.types_resources_input) + len(scheme.types_resources_input_liquid) - 1) ) // 2
                if border_x < 0:
                    border_x = 0
                offset_x = border_x
                offset_y = 5*self.GV.scale.k
                for i in range(len(scheme.types_resources_input)):
                    image = QLabel(widget)
                    image.resize(btn_size, btn_size)
                    image.move(offset_x, offset_y + label.height() + 10)
                    pixmap = QPixmap(scheme.types_resources_input[i].image)
                    image.setPixmap(pixmap.scaled(image.size()))
                    image.show()

                    offset_x += btn_size + distans

                # Так же проходим по жидкостям
                for i in range(len(scheme.types_resources_input_liquid)):
                    image = QLabel(widget)
                    image.resize(btn_size, btn_size)
                    image.move(offset_x, offset_y + label.height() + 10)
                    pixmap = QPixmap(scheme.types_resources_input_liquid[i].image)
                    image.setPixmap(pixmap.scaled(image.size()))
                    image.show()

                    offset_x += btn_size + distans
                plus_height = btn_size + offset_y*2
                busy_width = ( btn_size*( len(scheme.types_resources_input) + len(scheme.types_resources_input_liquid) )
                + ( len(scheme.types_resources_input) + len(scheme.types_resources_input_liquid) - 1)*distans + 20)
                if busy_width > width:
                    width = busy_width

            widget.resize(width,
                          label.height() + 20*self.GV.scale.k + plus_height)
            widget.move(scheme.pos().x() + scheme.width() // 2 - widget.width() // 2,
                        scheme.pos().y() - widget.height() - int(5*self.GV.scale.k))
            widget.setAttribute(Qt.WA_TransparentForMouseEvents)
            widget.show()
            self.widgets.append(widget)


    def craft(self, scheme):
        if len(scheme.input_schemes) == 0 and len(scheme.input_schemes_liquid) == 0:
            return

        recipe = scheme.object.recipes[scheme.current_recipe_index]

        if not self.isSimpleCraft:
            need_types = recipe.types_input_list
            have_types = scheme.types_resources_input + scheme.types_resources_input_liquid
            # Если хотя бы один элемент не в have_types, то попадаем в условие
            if not all(item in have_types for item in need_types):
                return


        if len(recipe.types_input_list) == 0:
            return

        percents = []
        percents_liquid = []
        for i in range(len(scheme.types_resources_input)):
            res = scheme.types_resources_input[i]
            if res in recipe.types_input_list:
                count = scheme.count_resources_input[i]
                index = recipe.types_input_list.index(res)
                percent = Decimal(count) / Decimal(recipe.count_input_list[index]) * 100
                percents.append(percent)
        for i in range(len(scheme.types_resources_input_liquid)):
            res = scheme.types_resources_input_liquid[i]
            if res in recipe.types_input_list:
                count = scheme.count_resources_input_liquid[i]
                index = recipe.types_input_list.index(res)
                percent = Decimal(count) / Decimal(recipe.count_input_list[index]) * 100
                percents_liquid.append(percent)

        if len(percents) == 0 and len(percents_liquid) == 0:
            return

        min_percent = 1000
        for percent in percents:
            if percent < min_percent:
                min_percent = percent
        for percent in percents_liquid:
            if percent < min_percent:
                min_percent = percent

        if min_percent > 100 + Decimal("50")*scheme.count_batteries:
            min_percent = 100 + Decimal("50")*scheme.count_batteries


        for i in range(len(recipe.types_output_list)):
            res_type = recipe.types_output_list[i]
            res_count = recipe.count_output_list[i] * min_percent / Decimal("100")
            isLiquid = get_bool_from_int(res_type.is_liquid)

            if isLiquid:
                scheme.types_resources_output_liquid.append(res_type)
                scheme.count_resources_output_liquid.append(res_count)
            else:
                scheme.types_resources_output.append(res_type)
                scheme.count_resources_output.append(res_count)


    def start_pulse(self, scheme: SchemeLabel):
        # Если нет input schemes, то считаем точкой старта и выдаем ресы
        if len(scheme.input_schemes) == 0 and len(scheme.input_schemes_liquid) == 0:
            for i in range(len(scheme.object.recipes[scheme.current_recipe_index].types_output_list)):
                res = scheme.object.recipes[scheme.current_recipe_index].types_output_list[i]
                count = scheme.object.recipes[scheme.current_recipe_index].count_output_list[i]
                count += ( Decimal(count) / 100 ) * (scheme.count_batteries * 50)
                if res.is_liquid:
                    scheme.types_resources_output_liquid.append(res)
                    scheme.count_resources_output_liquid.append(count)
                else:
                    scheme.types_resources_output.append(res)
                    scheme.count_resources_output.append(count)


        # Объединяем одинаковые ресурсы
        new_types = []
        new_counts = []
        for i in range(len(scheme.types_resources_input)):

            current_type = scheme.types_resources_input[i]

            if current_type in new_types:
                continue

            new_types.append(current_type)
            new_counts.append(scheme.count_resources_input[i])

            for j in range(i+1, len(scheme.types_resources_input)):
                if scheme.types_resources_input[i] == scheme.types_resources_input[j]:
                    new_counts[-1] += scheme.count_resources_input[j]
        scheme.types_resources_input = new_types[:]
        scheme.count_resources_input = new_counts[:]

        # И объединяем одинаковые жидкости
        new_types = []
        new_counts = []
        for i in range(len(scheme.types_resources_input_liquid)):

            current_type = scheme.types_resources_input_liquid[i]

            if current_type in new_types:
                continue

            new_types.append(current_type)
            new_counts.append(scheme.count_resources_input_liquid[i])

            for j in range(i+1, len(scheme.types_resources_input_liquid)):
                if scheme.types_resources_input_liquid[i] == scheme.types_resources_input_liquid[j]:
                    new_counts[-1] += scheme.count_resources_input_liquid[j]
        scheme.types_resources_input_liquid = new_types[:]
        scheme.count_resources_input_liquid = new_counts[:]


        if scheme.object.name == "Очистительный завод":
            print("Это для точки останова")
        self.craft(scheme)


        # Если нет output schemes, то на выход из функции
        if len(scheme.output_schemes) == 0 and len(scheme.output_schemes_liquid) == 0:
            return

        # Если output ресурсов нет, то на выход из функции
        if len(scheme.types_resources_output) == 0 and len(scheme.types_resources_output_liquid) == 0:
            return

        # Передаем ресурсы на все output'ы
        for i in range(len(scheme.count_resources_output)):
            res_count = scheme.count_resources_output[i]
            res_type = scheme.types_resources_output[i]
            divider = len(scheme.output_schemes) if len(scheme.output_schemes) > 0 else 1
            divide_resource = res_count / divider
            for i in range(len(scheme.output_schemes)):
                scheme.output_schemes[i].types_resources_input.append(res_type)
                if scheme.output_objects[i].max_value < divide_resource:
                    scheme.output_schemes[i].count_resources_input.append(scheme.output_objects[i].max_value)
                    continue
                scheme.output_schemes[i].count_resources_input.append(divide_resource)


        # Так же передаем все жидкости
        for i in range(len(scheme.count_resources_output_liquid)):
            res_count = scheme.count_resources_output_liquid[i]
            res_type = scheme.types_resources_output_liquid[i]
            divider = len(scheme.output_schemes_liquid) if len(scheme.output_schemes_liquid) > 0 else 1
            divide_resource = res_count / divider
            for i in range(len(scheme.output_schemes_liquid)):
                scheme.output_schemes_liquid[i].types_resources_input_liquid.append(res_type)
                if scheme.output_objects_liquid[i].max_value < divide_resource:
                    scheme.output_schemes_liquid[i].count_resources_input_liquid.append(scheme.output_objects_liquid[i].max_value)
                    continue
                scheme.output_schemes_liquid[i].count_resources_input_liquid.append(divide_resource)



    def start_logistic_pulse(self, scheme: SchemeLabel):
        if (scheme.object.name == "Соединитель" or scheme.object.category == "storage"
                or scheme.object.name == "Liquid 3->1"):

            # Объединяем одинаковые ресурсы
            new_types = []
            new_counts = []
            for i in range(len(scheme.types_resources_input)):

                current_type = scheme.types_resources_input[i]

                if current_type in new_types:
                    continue

                new_types.append(current_type)
                new_counts.append(scheme.count_resources_input[i])

                for j in range(i+1, len(scheme.types_resources_input)):
                    if scheme.types_resources_input[i] == scheme.types_resources_input[j]:
                        new_counts[-1] += scheme.count_resources_input[j]
            scheme.types_resources_input = new_types[:]
            scheme.count_resources_input = new_counts[:]


            # Объединяем одинаковые жидкости
            new_types = []
            new_counts = []
            for i in range(len(scheme.types_resources_input_liquid)):

                current_type = scheme.types_resources_input_liquid[i]

                if current_type in new_types:
                    continue

                new_types.append(current_type)
                new_counts.append(scheme.count_resources_input_liquid[i])

                for j in range(i+1, len(scheme.types_resources_input_liquid)):
                    if scheme.types_resources_input_liquid[i] == scheme.types_resources_input_liquid[j]:
                        new_counts[-1] += scheme.count_resources_input_liquid[j]
            scheme.types_resources_input_liquid = new_types[:]
            scheme.count_resources_input_liquid = new_counts[:]

        # Передаем ресурсы из input в output
        scheme.types_resources_output = scheme.types_resources_input[:]
        scheme.count_resources_output = scheme.count_resources_input[:]

        scheme.types_resources_output_liquid = scheme.types_resources_input_liquid[:]
        scheme.count_resources_output_liquid = scheme.count_resources_input_liquid[:]

        # Если нет output schemes, то на выход из функции
        if len(scheme.output_schemes) == 0 and len(scheme.output_schemes_liquid) == 0:
            return

        # Если output ресурсов нет, то на выход из функции
        if len(scheme.types_resources_output) == 0 and len(scheme.types_resources_output_liquid) == 0:
            return

        # Передаем ресурсы на все output'ы
        for i in range(len(scheme.count_resources_output)):
            res_count = scheme.count_resources_output[i]
            res_type = scheme.types_resources_output[i]
            divide_resource = res_count / len(scheme.output_schemes)
            for i in range(len(scheme.output_schemes)):
                scheme.output_schemes[i].types_resources_input.append(res_type)
                if scheme.output_objects[i].max_value < divide_resource:
                    scheme.output_schemes[i].count_resources_input.append(scheme.output_objects[i].max_value)
                    continue
                scheme.output_schemes[i].count_resources_input.append(divide_resource)


        # Так же передаем жидкости
        for i in range(len(scheme.count_resources_output_liquid)):
            res_count = scheme.count_resources_output_liquid[i]
            res_type = scheme.types_resources_output_liquid[i]
            divide_resource = res_count / len(scheme.output_schemes_liquid)
            for i in range(len(scheme.output_schemes_liquid)):
                scheme.output_schemes_liquid[i].types_resources_input_liquid.append(res_type)
                if scheme.output_objects_liquid[i].max_value < divide_resource:
                    scheme.output_schemes_liquid[i].count_resources_input_liquid.append(scheme.output_objects_liquid[i].max_value)
                    continue
                scheme.output_schemes_liquid[i].count_resources_input_liquid.append(divide_resource)



    def pulse(self):
        for scheme in self.sorted_schemes:
            # Подготовка: Очищаем ресурсы
            scheme.types_resources_input.clear()
            scheme.count_resources_input.clear()
            scheme.types_resources_output.clear()
            scheme.count_resources_output.clear()

            scheme.types_resources_input_liquid.clear()
            scheme.count_resources_input_liquid.clear()
            scheme.types_resources_output_liquid.clear()
            scheme.count_resources_output_liquid.clear()

        for scheme in self.sorted_schemes:

            if scheme.object.category == "logistics" or scheme.object.category == "storage":
                self.start_logistic_pulse(scheme)
                continue

            # Если в схеме нет рецепта и она не логистик и не storage, то игнорируем
            if scheme.current_recipe_index is None:
                continue

            # Запускаем пульс для схемы
            self.start_pulse(scheme)


    def sort_schemes(self):
        self.sorted_schemes.clear()
        self.sorted_schemes = sorted(self.parent().schemes[:], key=get_pos_x)



    def create_new_widgets(self):
        for scheme in self.sorted_schemes:
            if not scheme.createWidget:
                continue

            # Отсеиваем без рецептов и логистику
            if scheme.current_recipe_index is None:
                continue
            recipe = scheme.object.recipes[scheme.current_recipe_index]

            # Формируем надпись
            s = ""
            if self.isPrintCurrent:
                if len(scheme.input_schemes) == 0 and len(scheme.input_schemes_liquid) == 0:
                    # res1 = recipe.count_output_list[0]
                    # res2 = Decimal(recipe.count_output_list[0])/100*scheme.count_batteries*50
                    # res = res1 + res2
                    # res = res.normalize()
                    # s += f"=>{format(res, 'f')}"
                    s += "=>"
                    output_resources_count = scheme.count_resources_output + scheme.count_resources_output_liquid
                    for i in range(len(output_resources_count)):
                        count = output_resources_count[i]
                        count = count.normalize()
                        s += f"{format(count, 'f')}"
                        if i != range(len(output_resources_count))[-1]:
                            s += ", "

                else:
                    for i in range(len(recipe.types_input_list)):

                        have_resource = Decimal("0")
                        need_resource = (recipe.count_input_list[i] +
                                         Decimal(recipe.count_input_list[i])/100 * (scheme.count_batteries * 50) )

                        if recipe.types_input_list[i] in scheme.types_resources_input:
                            index_type = scheme.types_resources_input.index(recipe.types_input_list[i])
                            have_resource = scheme.count_resources_input[index_type]
                        elif recipe.types_input_list[i] in scheme.types_resources_input_liquid:
                            index_type = scheme.types_resources_input_liquid.index(recipe.types_input_list[i])
                            have_resource = scheme.count_resources_input_liquid[index_type]

                        have_resource = have_resource.normalize()
                        need_resource = need_resource.normalize()

                        s += f"{format(have_resource, 'f')}/{format(need_resource, 'f')}"

                        if not i == range(len(recipe.types_input_list))[-1]:
                            s += ", "

                    s += "=>"
                    output_resources_count = scheme.count_resources_output + scheme.count_resources_output_liquid
                    for i in range(len(output_resources_count)):
                        count = output_resources_count[i]
                        count = count.normalize()
                        s += f"{format(count, 'f')}"
                        if i != range(len(output_resources_count))[-1]:
                            s += ", "


            # Создаем виджет
            widget = QWidget(self.parent())

            label = QLabel(s, widget)
            label.setFont(QFont("Arial", 18*self.GV.scale.k))
            label.adjustSize()
            label.move(20, 10)
            label.show()

            plus_height = 0
            width = label.width() + 40
            if self.isPrintTypes:
                btn_size = 34*self.GV.scale.k
                distans = 15

                eq_label = QLabel("=>", widget)
                eq_label.setFont(QFont("Arial", 20*self.GV.scale.k))
                eq_label.adjustSize()
                eq_label.show()

                if not (len(scheme.input_schemes) == 0 and len(scheme.input_schemes_liquid) == 0):
                    border_x = ( width - btn_size*(len(scheme.object.recipes[scheme.current_recipe_index].types_input_list)
                                +len(scheme.object.recipes[scheme.current_recipe_index].types_output_list))
                                 - distans*(len(scheme.object.recipes[scheme.current_recipe_index].types_input_list)
                                +len(scheme.object.recipes[scheme.current_recipe_index].types_output_list)-1) -
                                 eq_label.width()) // 2
                else:
                    border_x = 10
                if border_x < 0:
                    border_x = 0
                offset_x = border_x
                offset_y = 5*self.GV.scale.k
                if not (len(scheme.input_schemes) == 0 and len(scheme.input_schemes_liquid) == 0):
                    for i in range(len(scheme.object.recipes[scheme.current_recipe_index].types_input_list)):
                        image = QLabel(widget)
                        image.resize(btn_size, btn_size)
                        image.move(offset_x, offset_y + label.height() + 10)
                        pixmap = QPixmap(scheme.object.recipes[scheme.current_recipe_index].types_input_list[i].image)
                        image.setPixmap(pixmap.scaled(image.size()))
                        image.show()

                        offset_x += btn_size + distans


                eq_label.move(offset_x, offset_y + label.height() + 17)

                offset_x += eq_label.width() + distans

                for i in range(len(scheme.object.recipes[scheme.current_recipe_index].types_output_list)):
                    image = QLabel(widget)
                    image.resize(btn_size, btn_size)
                    image.move(offset_x, offset_y + label.height() + 10)
                    pixmap = QPixmap(scheme.object.recipes[scheme.current_recipe_index].types_output_list[i].image)
                    image.setPixmap(pixmap.scaled(image.size()))
                    image.show()

                    offset_x += btn_size + distans

                plus_height = btn_size + offset_y*2
                busy_width = ( btn_size*(len(scheme.object.recipes[scheme.current_recipe_index].types_output_list)
                            +len(scheme.object.recipes[scheme.current_recipe_index].types_input_list)) +
                        distans*(len(scheme.object.recipes[scheme.current_recipe_index].types_output_list)
                            +len(scheme.object.recipes[scheme.current_recipe_index].types_input_list))) + 20 + eq_label.width()
                if busy_width > width:
                    width = busy_width


            widget.resize(width, label.height() + 20*self.GV.scale.k + plus_height)
            widget.move(scheme.pos().x() + scheme.width() // 2 - widget.width() // 2,
                        scheme.pos().y() - widget.height() - 5*self.GV.scale.k)
            widget.setAttribute(Qt.WA_TransparentForMouseEvents)
            widget.show()
            self.widgets.append(widget)
