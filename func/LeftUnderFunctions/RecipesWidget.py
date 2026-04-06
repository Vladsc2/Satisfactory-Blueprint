from PySide6.QtWidgets import QWidget, QScrollArea, QLineEdit
from PySide6.QtGui import QFont
from func.Samples.Background import Background
from func.Samples.IButton import IButton
from GF.Constants import *
from func.Samples.RecipeBtn import RecipeBtn
from PySide6.QtCore import Qt, QSize

class ObjectRecipesWidget(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        super().__init__(parent)

        self.resize(parent.width(),
                    parent.height())
        self.hide()
        self.background = Background("0, 255, 255", self)

        self.current_sample = ""
        self.last_name_scheme = ""

        self.scroll_area = QScrollArea(self)
        self.scroll_area.resize(self.size() + QSize(0, -55))
        self.scroll_area.move(0, 55)
        self.scroll_area.setAttribute(Qt.WA_TransparentForMouseEvents, False)  # Обработка событий мыши
        self.scroll_area.show()

        self.content_widget = QWidget()
        self.content_widget.resize(self.scroll_area.size() + QSize(-19, 0))
        self.content_widget.show()

        self.scroll_area.setWidget(self.content_widget)

        self.btns = []

        self.init_recipe_widget_ui()


    def select_recipe(self, scheme, index):
        scheme.current_recipe_index = index
        self.GV.main_under_widget.selectScheme(scheme)
        self.GV.production_area.tick()
        self.GV.historyManager.notSave()


    def show_all_btns(self):
        offset_x = 20
        offset_y = 5
        distans = 5

        for btn in self.btns:
            btn.show()
            btn.move(offset_x, offset_y)

            offset_y += btn.height() + distans

        self.content_widget.resize(self.content_widget.width(),
                                   offset_y + 50)


    def search_from_sample(self, text: str):
        self.current_sample = text.strip().lower()

        if self.current_sample == "":
            self.show_all_btns()

        offset_x = 20
        offset_y = 5
        distans = 5

        # Сначала скрываем все кнопки
        for btn in self.btns:
            btn.hide()

        for btn in self.btns:
            if btn.index_recipe is None:
                continue
            find_flag = False
            for res_name in btn.object.recipes[btn.index_recipe].types_input_list:
                if self.current_sample in res_name.name.lower():
                    find_flag = True
            for res_name in btn.object.recipes[btn.index_recipe].types_output_list:
                if self.current_sample in res_name.name.lower():
                    find_flag = True

            if find_flag:
                btn.show()
                btn.move(offset_x, offset_y)
                offset_y += btn.height() + distans


        self.content_widget.resize(self.content_widget.width(),
                                   offset_y + 50)


    def start_recipe_widget(self, scheme):
        new_scheme_flag = True
        if scheme.object.name == self.last_name_scheme:
            new_scheme_flag = False
        self.last_name_scheme = scheme.object.name

        if new_scheme_flag:
            self.current_sample = ""
            self.recipe_search.setText("")

        self.start_new_scheme(scheme)
        self.search_from_sample(self.current_sample)


    def start_new_scheme(self, scheme):
        # Удаляем старые кнопки
        for btn in self.btns:
            btn.deleteLater()
        self.btns.clear()

        btn_width = self.width() - 59
        btn_height = 80
        offset_x = 20
        offset_y = 5
        distans = 5

        # Создаем кнопку выбранного рецепта
        btn = RecipeBtn(self.GV, self.content_widget)
        btn.resize(btn_width, btn_height)
        btn.move(offset_x, offset_y)
        btn.set_recipe(scheme, scheme.current_recipe_index)
        btn.clicked.connect(lambda checked=False, s=scheme, index=scheme.current_recipe_index:
                                self.select_recipe(s, index))
        btn.forming_ui()
        self.btns.append(btn)

        offset_y += btn_height + distans

        if not scheme.current_recipe_index is None:
            btn = RecipeBtn(self.GV, self.content_widget)
            btn.resize(btn_width, btn_height)
            btn.move(offset_x, offset_y)
            btn.set_recipe(scheme, None)
            btn.clicked.connect(lambda checked=False, s=scheme, index=None: self.select_recipe(s, index))
            btn.forming_ui()
            self.btns.append(btn)

            offset_y += btn_height + distans


        # Создаем новые кнопки
        for i in range(len(scheme.object.recipes)):
            if not scheme.current_recipe_index is None:
                if scheme.object.recipes[i] == scheme.object.recipes[scheme.current_recipe_index]:
                    continue

            recipe = scheme.object.recipes[i]
            if recipe.lvl > self.GV.config.current_lvl:
                continue

            btn = RecipeBtn(self.GV, self.content_widget)
            btn.resize(btn_width, btn_height)
            btn.move(offset_x, offset_y)
            btn.set_recipe(scheme, i)
            btn.forming_ui()
            self.btns.append(btn)

            offset_y += btn_height + distans

            btn.clicked.connect(lambda checked=False, s=scheme, index=i: self.select_recipe(s, index))

        self.content_widget.resize(self.content_widget.width(),
                                   offset_y + 50)


    def hide(self):
        self.GV.main_under_widget.factory_info_widget.update_factory_info_widget()
        super().hide()

    def init_recipe_widget_ui(self):
        btn_width = self.width() - 59

        # Создаем поиск
        self.recipe_search = QLineEdit(self)
        self.recipe_search.resize(self.width(), 55)
        self.recipe_search.setFont(QFont("Arial", 30))
        self.recipe_search.setAlignment(Qt.AlignCenter)
        self.recipe_search.show()
        self.recipe_search.textChanged.connect(self.search_from_sample)