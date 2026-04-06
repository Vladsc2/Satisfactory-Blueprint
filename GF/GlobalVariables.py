from sys import exit

class GlobalVariables():
    def __init__(self):
        self.project = None
        self.config = None
        self.database = None

        self.window = None

        self.lw = None
        self.rw = None

        self.mouse_image = None
        self.group_mouse_image = None

        self.control_project = None
        self.widget_new_project = None

        self.search = None
        self.components_widget = None
        self.categories_widget = None

        self.main_under_widget = None
        self.schemes_group_scroll_area = None

        self.control_bar = None

        self.cell_blueprint = None
        self.blueprint = None

        self.production_area = None

        self.hotkeys = None

        self.scale = None

        self.cameraSystem = None

        self.historyManager = None


    def exit_application(self, hard_exit=False):
        if not self.project.isSaved and not hard_exit:
            self.project.show_widget_if_not_save()
            return

        self.blueprint.paint_area.timer.stop()
        exit(0)