

class CommentData():
    def __init__(self, text, layout, lowerFlag):
        self.text = text
        self.text_layout = layout
        self.setLower = lowerFlag

        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

        self.text_color = ""
        self.head_color = ""
        self.body_color = ""
        self.point_color = ""


    def set_size(self, size):
        self.width = size.width()
        self.height = size.height()

    def set_pos(self, pos):
        self.x = pos.x()
        self.y = pos.y()