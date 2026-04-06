from decimal import Decimal
from time import sleep
from GF.GlobalVariables import GlobalVariables
from PySide6.QtGui import QPixmap

class Scale():
    def __init__(self, GV):
        self.GV = GV
        GV.scale = self

        self.max_scale_percent = Decimal("200")
        self.min_scale_percent = Decimal("25")

        self.current_scale_percent = Decimal("100")
        self.k = 1


    def update_view(self):
        old_k = self.k          # Старое значение k
        self.k = self.current_scale_percent / 100   # Новое k

        blueprint = self.GV.blueprint

        blueprint.update_size_from_config_and_zoom()

        blueprint.move(0 - blueprint.width() // 2 + blueprint.parent.width() // 2,
                       0 - blueprint.height() // 2 + blueprint.parent.height() // 2)

        for scheme in blueprint.schemes:
            standard_width = int(scheme.width()/old_k)
            standard_height = int(scheme.height()/old_k)

            scheme.resize(int(standard_width*self.k), int(standard_height*self.k))
            scheme.setPixmap(QPixmap(scheme.object.scheme).scaled(scheme.size()))


            standard_x = int(scheme.pos().x() / old_k)
            standard_y = int(scheme.pos().y() / old_k)

            scheme.move(int(standard_x*self.k), int(standard_y*self.k))


        for comment in blueprint.comments:
            standard_width_c = int(comment.width()/old_k)
            standard_height_c = int(comment.height()/old_k)

            comment.resize(int(standard_width_c * self.k), int(standard_height_c * self.k))
            comment.resize_subwidgets()
            comment.set_pos_text_from_layout()

            standard_x_c = int(comment.pos().x() / old_k)
            standard_y_c = int(comment.pos().y() / old_k)

            comment.move(int(standard_x_c*self.k), int(standard_y_c*self.k))


        self.GV.production_area.tick()

        self.GV.control_bar.current_scale_label.setText(str(self.current_scale_percent)+"%")
        self.GV.control_bar.current_scale_label.adjustSize()


    def zoom_in(self):
        if self.current_scale_percent >= 100:
            step = Decimal("50")
        elif self.current_scale_percent >= 25:
            step = Decimal("25")
        else:
            step = Decimal("12.5")

        if self.current_scale_percent + step > self.max_scale_percent:
            return

        self.current_scale_percent += step
        self.update_view()


    def zoom_out(self):
        if self.current_scale_percent <= 25:
            step = Decimal("12.5")
        elif self.current_scale_percent <= 100:
            step = Decimal("25")
        else:
            step = Decimal("50")

        if self.current_scale_percent - step < self.min_scale_percent:
            return

        self.current_scale_percent -= step
        self.update_view()
