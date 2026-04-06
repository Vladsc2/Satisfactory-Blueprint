from PySide6.QtWidgets import QApplication
from decimal import Decimal

def get_voltage(standard_voltage, count_batteries):
    hz = Decimal(100 + (count_batteries * 50))
    new_voltage = standard_voltage * Decimal(hz/100)**Decimal(1.32)
    return new_voltage

def bool_from_str(bool_var):
    if bool_var == "True":
        return True
    else:
        return False


def get_screen_size():
    screens = QApplication.screens()
    if len(screens) > 0:
        screen = screens[0]
        return screen.size().width(), screen.size().height()
    return 0, 0


def get_bool_from_int(int_var):
    int_var = int(int_var)
    if int_var <= 0:
        return False
    else:
        return True

def get_pos_x(label):
    return label.pos().x()


MONITOR_WIDTH, MONITOR_HEIGHT = get_screen_size()
