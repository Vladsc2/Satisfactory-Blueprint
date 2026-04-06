import json

class Config():
    def __init__(self, GV):
        self.GV = GV
        GV.config = self

        self.save_directory = "Projects"

        self.blueprint_width = 1920
        self.blueprint_height = 1080

        self.hz_conv_lines = 100
        self.hz_mouse_image = 200

        self.flag_simple_craft = False
        self.flag_print_current = True
        self.flag_print_types = True
        self.flag_print_logistics = False
        self.flag_print_types_logistics = True

        self.show_hotkeys = True

        self.current_lvl = 9

        self.comment_standard_layout = "left"   # left, center, right
        self.comment_standard_text_color = "rgb(240, 240, 240)"
        self.comment_standard_head_color = "rgba(240, 72, 0, 1)"
        self.comment_standard_body_color = "rgba(255, 165, 0, 0.8)"
        self.comment_standard_point_color = "rgb(255, 0, 0)"

        self.use_undo_system = True
        self.undo_limit = 50

        self.save_before_restart = True

        self.default_flag_create_widget = True

        self.auto_load_last_project = True

        self.load_config()


    def save_config(self):
        production_area = self.GV.production_area
        self.flag_simple_craft = production_area.isSimpleCraft
        self.flag_print_current = production_area.isPrintCurrent
        self.flag_print_types = production_area.isPrintTypes
        self.flag_print_logistics = production_area.isPrintLogistic
        self.flag_print_types_logistics = production_area.isPrintTypesLogistic

        self_dict = self.__dict__.copy()
        self_dict.pop("GV")

        with open("config.json", "w", encoding="utf-8") as file:
            json.dump(self_dict, file, indent=4, ensure_ascii=False)


    def load_config(self):
        with open("config.json", 'r', encoding="utf-8") as file:
            dict_data = json.load(file)

        for key, value in dict_data.items():
            setattr(self, key, value)