from PySide6.QtWidgets import QWidget, QScrollArea
from PySide6.QtCore import QSize, Qt
from func.Samples.AddObjectBtn import *

class ComponentsWidget(QScrollArea):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.components_widget = self
        super().__init__(parent)

        self.resize(parent.width(), parent.height() - 60)
        self.move(0, 60)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)  # Обработка событий мыши
        self.hide()

        self.inside_widget = QWidget()
        self.inside_widget.resize(self.size() + QSize(-19, 0))
        self.inside_widget.show()

        self.add_btns = []
        self.border_x = 5
        self.border_y = 5
        self.btn_height = 80
        self.init_btns()

        # Для осуществления поиска
        self.current_samples = []
        self.current_category = ""
        self.current_energy = 0
        self.energy_modify = "="


    def init_btns(self):
        width = self.inside_widget.width() - self.border_x*2

        offset_y = self.border_y

        for dataObject in self.GV.database.data_list:
            btn = AddObjectBtn(self.inside_widget)
            btn.show()

            btn.resize(width, self.btn_height)
            btn.move(self.border_x, offset_y)
            offset_y += self.btn_height

            btn.set_category(dataObject.category)
            btn.set_object(dataObject)
            btn.set_name_scheme_image(dataObject.name, dataObject.scheme, dataObject.image)
            btn.set_energy(dataObject.energy)

            btn.clicked.connect(lambda clicked=False, b=btn: self.start_add_component(b))

            self.add_btns.append(btn)

        self.inside_widget.resize(self.inside_widget.width(),
                                  len(self.GV.database.data_list)*self.btn_height + self.border_y*2)

        self.setWidget(self.inside_widget)


    def start_add_component(self, btn):
        if btn.object.type == "logistic":
            self.GV.blueprint.logistic_object = btn.object
            self.GV.blueprint.logistics_points = 2
            self.GV.window.change_cursor_to_logistic(True)
            return
        self.GV.window.mouse_image.start_image(btn.object)


    def show_btns_from_samples(self):
        # Сначала скрываем все кнопки
        for btn in self.add_btns:
            btn.hide()

        # Теперь показываем кнопки если подходят по шаблону
        show_btns_counter = 0
        offset_y = self.border_y
        current_lvl = self.GV.config.current_lvl
        for btn in self.add_btns:
            if btn.object.lvl > current_lvl:
                continue

            # Проверяем на наличие в шаблоне
            for sample in self.current_samples:
                if sample in btn.name.lower():
                    btn.move(self.border_x, offset_y)
                    btn.show()
                    offset_y += self.btn_height

            if btn.isVisible():
                show_btns_counter += 1
                continue

            # Добавляем категорию
            if self.current_category == btn.category:
                btn.move(self.border_x, offset_y)
                btn.show()
                offset_y += self.btn_height

            if btn.isVisible():
                show_btns_counter += 1
                continue

            # Добавляем по энергии
            if not self.current_energy <= 0:
                if self.energy_modify == "=" and btn.energy == self.current_energy:
                    btn.move(self.border_x, offset_y)
                    btn.show()
                    offset_y += self.btn_height

                elif self.energy_modify == "+" and btn.energy >= self.current_energy:
                    btn.move(self.border_x, offset_y)
                    btn.show()
                    offset_y += self.btn_height

                elif self.energy_modify == "-" and btn.energy <= self.current_energy:
                    btn.move(self.border_x, offset_y)
                    btn.show()
                    offset_y += self.btn_height

            if btn.isVisible():
                show_btns_counter += 1
                continue

        # Изменяем размер виджета
        self.inside_widget.resize(self.inside_widget.width(),
                                  show_btns_counter*self.btn_height + self.border_y*2)



    def click_clear_btn(self):
        self.hide()
        self.GV.categories_widget.show()
        self.GV.search.clear_lineEdit_btn.hide()
        self.GV.search.lineEdit.blockSignals(True)
        self.GV.search.lineEdit.setText("")
        self.GV.search.lineEdit.blockSignals(False)
        self.GV.blueprint.setFocus()



    def show_all_btns(self):
        offset_y = self.border_y
        for btn in self.add_btns:
            object_name = btn.object.name
            if btn.object.lvl > self.GV.config.current_lvl:
                continue
            btn.move(self.border_x, offset_y)
            btn.show()
            offset_y += self.btn_height

        self.inside_widget.resize(self.inside_widget.width(),
                                  offset_y + self.border_y*2)


    def search_from_text(self, text, clicked=False):
        samples = text.split(" ")
        # Скрываем все кнопки
        for btn in self.add_btns:
            btn.hide()

        # Сбрасываем на значения по умолчанию
        self.current_samples.clear()
        self.current_category = ""
        self.current_energy = 0
        self.energy_modify = "="

        # Показываем кнопку и меняем виджеты
        self.show()
        self.GV.categories_widget.hide()
        self.GV.search.clear_lineEdit_btn.show()

        if text.strip() == "":
            self.show_all_btns()
            return

        for sample in samples:
            if len(sample) == 0:
                continue

            sample = sample.lower()

            if sample[0] == "#":
                self.check_category(sample)

            elif sample[0] == "$":
                self.check_energy(sample)

            else:
                self.current_samples.append(sample)

        self.show_btns_from_samples()



    def check_energy(self, sample):
        # Определяем модификатор
        self.current_energy = 0
        self.energy_modify = "="
        if sample[-1] == "+":
            self.energy_modify = "+"
            sample = sample[:-1]
        elif sample[-1] == "-":
            self.energy_modify = "-"
            sample = sample[:-1]

        sample = sample[1:]
        if not sample.isdigit():
            return
        sample = int(sample)
        self.current_energy = sample


    def check_category(self, sample):
        if sample in "#изготовители":
            self.current_category = C_CREATORS
        elif sample in "#плавильни":
            self.current_category = C_SMELTERS
        elif sample in "#буры":
            self.current_category = C_BOERS
        elif sample in "#экстракторы":
            self.current_category = C_EXTRACTORS
        elif sample in "#энергия":
            self.current_category = C_ENERGY
        elif sample in "#логистика":
            self.current_category = C_LOGISTICS
        elif sample in "#хранилища":
            self.current_category = C_STORAGE
        elif sample in "#custom":
            self.current_category = C_CUSTOM
        else:
            self.current_category = ""