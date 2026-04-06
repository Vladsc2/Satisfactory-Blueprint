from PySide6.QtWidgets import QWidget
from func.Samples.Background import Background

from func.LeftUnderFunctions.RecipesWidget import ObjectRecipesWidget
from func.LeftUnderFunctions.ObjectInfoWidget import ObjectInfoWidget
from func.LeftUnderFunctions.GroupWidget import GroupWidget
from func.LeftUnderFunctions.factory_info_widget import FactoryInfoWidget
from func.LeftUnderFunctions.CommentWidget import CommentWidget

class MainObjectWidget(QWidget):
    def __init__(self, GV, parent):
        self.GV = GV
        GV.main_under_widget = self
        super().__init__(parent)

        self.resize(parent.width(),
                    parent.height())
        self.show()
        background = Background("255, 165, 0", self)

        self.factory_info_widget = FactoryInfoWidget(GV, self)

        self.objectInfoWidget = ObjectInfoWidget(GV, self)

        self.objectRecipesWidget = ObjectRecipesWidget(GV, self)

        self.groupWidget = GroupWidget(GV, self)

        self.commentWidget = CommentWidget(GV, self)


    def selectNone(self):
        self.objectInfoWidget.hide()
        self.objectRecipesWidget.hide()
        self.groupWidget.hide()
        self.commentWidget.hide()

        self.objectInfoWidget.current_scheme = None


    def selectScheme(self, scheme):
        self.objectInfoWidget.show()
        self.objectRecipesWidget.hide()
        self.groupWidget.hide()
        self.commentWidget.hide()

        self.objectInfoWidget.update_object_info_widget(scheme)


    def selectRecipes(self, scheme):
        self.objectInfoWidget.hide()
        self.objectRecipesWidget.show()
        self.groupWidget.hide()
        self.commentWidget.hide()

        self.objectRecipesWidget.start_recipe_widget(scheme)


    def selectGroup(self):
        self.objectInfoWidget.hide()
        self.objectRecipesWidget.hide()
        self.groupWidget.show()
        self.commentWidget.hide()

        group = self.GV.blueprint.selected_group

        self.groupWidget.update_group_widget(group)


    def selectComment(self, comment):
        self.objectInfoWidget.hide()
        self.objectRecipesWidget.hide()
        self.groupWidget.hide()
        self.commentWidget.show()

        self.commentWidget.update_comment_info(comment)