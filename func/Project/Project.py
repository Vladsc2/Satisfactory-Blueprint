from PySide6.QtWidgets import QWidget
from func.Samples.Background import Background
from func.Project.Widget_save_as import Widget_save_as
from func.Project.Widget_load_project import Widget_load_project
from func.Project.Widget_save_as_scheme import Widget_save_as_scheme
from func.Project.Widget_if_not_save import Widget_if_not_save
from func.Project.Widget_if_not_save_before_load import Widget_if_not_save_before_load
from func.Project.Widget_new_project import Widget_new_project


class Project(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.project = self
        super().__init__(parent)

        self.working_directory = GV.config.save_directory

        self.name = "Завод"

        self.isSaved = True

        self.init_UI()

        self.GV.control_project.init_btns()

        self.start_Load_Project()

    def start_Load_Project(self):
        if self.GV.config.auto_load_last_project:
            self.widget_load_project.load_last_project()


    def hide_all_subwidgets(self):
        self.widget_save_as.hide()
        self.widget_load_project.hide()
        self.widget_save_as_scheme.hide()
        self.widget_if_not_save.hide()
        self.widget_if_not_save_before_load.hide()
        self.widget_new_project.hide()


    def show_widget_new_project(self):
        # Скрываем свои subwidgets
        self.hide_all_subwidgets()

        # Показываем серый экран
        self.GV.window.start_grey_mask()
        self.show()

        # Включаем правильный подвиджет и устанавливаем на нем фокус
        self.widget_new_project.show()
        self.widget_new_project.setFocus()


    def show_widget_if_not_save_before_load(self):
        # Запоминаем файл
        file_name = self.widget_load_project.current_file

        # Скрываем свои subwidgets
        self.hide_all_subwidgets()

        # Показываем серый экран
        self.GV.window.start_grey_mask()
        self.show()

        # Включаем правильный подвиджет и устанавливаем на нем фокус
        self.widget_if_not_save_before_load.show()
        self.widget_if_not_save_before_load.setFocus()

        self.widget_load_project.current_file = file_name


    def show_widget_if_not_save(self):
        # Скрываем свои subwidgets
        self.hide_all_subwidgets()

        # Показываем серый экран
        self.GV.window.start_grey_mask()
        self.show()

        # Включаем правильный подвиджет и устанавливаем на нем фокус
        self.widget_if_not_save.show()
        self.widget_if_not_save.setFocus()


    def show_widget_save_as_scheme(self):
        # Скрываем свои subwidgets
        self.hide_all_subwidgets()

        # Показываем серый экран
        self.GV.window.start_grey_mask()

        # Включаем правильный подвиджет и устанавливаем на нем фокус
        self.widget_save_as_scheme.show()
        self.widget_save_as_scheme.setFocus()


    def show_widget_load_project(self):
        # Скрываем свои subwidgets
        self.hide_all_subwidgets()

        # Показываем серый экран
        self.GV.window.start_grey_mask()

        # Включаем правильный подвиджет и устанавливаем на нем фокус
        self.widget_load_project.show()
        self.widget_load_project.setFocus()


    def show_widget_save_as(self, isExitSave=False, isLoadSave=False, isNewProjectSave=False):
        # Скрываем свои subwidgets
        self.hide_all_subwidgets()

        # Показываем себя
        self.GV.window.start_grey_mask()
        self.show()

        if isExitSave:
            self.widget_save_as.isExitSave = True
        if isLoadSave:
            self.widget_save_as.isLoadSave = True
        if isNewProjectSave:
            self.widget_save_as.isNewProjectSave = True

        # Включаем правильный подвиджет и устанавливаем на нем фокус
        self.widget_save_as.show()
        self.widget_save_as.setFocus()


    def init_UI(self):
        self.resize(800, 400)
        self.move(self.parent().width() // 2 - self.width() // 2,
                  self.parent().height() // 2 - self.height() // 2 - 60)
        self.hide()

        background = Background("221, 160, 221", self)

        self.widget_save_as = Widget_save_as(self.GV, self)

        self.widget_load_project = Widget_load_project(self.GV, self.GV.window)

        self.widget_save_as_scheme = Widget_save_as_scheme(self.GV, self.GV.window)

        self.widget_if_not_save = Widget_if_not_save(self.GV, self)

        self.widget_if_not_save_before_load = Widget_if_not_save_before_load(self.GV, self)

        self.widget_new_project = Widget_new_project(self.GV, self)


    def hide(self):
        self.GV.window.stop_grey_mask()
        super().hide()