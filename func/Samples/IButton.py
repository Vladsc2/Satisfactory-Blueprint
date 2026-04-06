from PySide6.QtWidgets import QPushButton, QLabel, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from func.Samples.Background import Background
from GF.Constants import *

class IButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.show()
        self.parent = parent

        self.standardImage = QLabel(self)
        self.pressedImage = QLabel(self)
        self.hoverImage = QLabel(self)

        self.standardImage.show()
        self.pressedImage.hide()
        self.hoverImage.hide()

        self.standardPath = None
        self.pressedPath = None
        self.hoverPath = None

        self.standardImage.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.pressedImage.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.hoverImage.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.onBtnPos = False

        self.isTooltip = False

        # Виджет для подсказки
        self.tooltipWidget = QWidget(parent)
        self.tooltipBackground = Background("255, 255, 255", self.tooltipWidget)
        self.tooltipLabel = QLabel(self.tooltipWidget)
        self.tooltipWidget.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.setStyleSheet("background-color: transparent; border: none;")


    def setPathsToImages(self, standardImage, pressedImage, hoverImage):
        self.standardPath = standardImage
        self.pressedPath = pressedImage
        self.hoverPath = hoverImage

        pixmap = QPixmap(standardImage)
        self.standardImage.setPixmap(pixmap.scaled(self.size()))
        pixmap = QPixmap(pressedImage)
        self.pressedImage.setPixmap(pixmap.scaled(self.size()))
        pixmap = QPixmap(hoverImage)
        self.hoverImage.setPixmap(pixmap.scaled(self.size()))


    def setTooltip(self, tooltip):
        self.isTooltip = True

        # Перенос текста
        s = ""
        counter = 0
        for char in tooltip:
            s += char
            counter += 1
            if counter == 30:
                counter = 0
                s += "\n"


        self.tooltipLabel.setText(s)
        self.tooltipLabel.adjustSize()
        self.tooltipLabel.move(3, 1)

        self.tooltipWidget.resize(self.tooltipLabel.size() + QSize(6, 2))
        self.tooltipBackground.resize(self.tooltipLabel.size() + QSize(6, 2))

        self.tooltipWidget.move(self.pos().x() - (self.tooltipLabel.width() // 2 - self.width() // 2),
                                self.pos().y() + self.height() // 2)


        # Обработка выхода за экран
        x = self.tooltipWidget.pos().x()
        if x < 0:
            self.tooltipWidget.move(0, self.pos().y() + self.height() + 5)
        if x + self.tooltipWidget.width() > self.parent.width():
            self.tooltipWidget.move(self.parent.width() - self.tooltipWidget.width(),
                                    self.pos().y() + self.height() + 5)

        y = self.tooltipWidget.pos().y()
        if y + self.tooltipWidget.height() > self.parent.height():
            self.tooltipWidget.move(self.tooltipWidget.pos().x(),
                                    self.pos().y() - self.tooltipWidget.height() - 5)


    def resize(self, w, h):
        super().resize(w, h)

        self.standardImage.resize(w, h)
        self.pressedImage.resize(w, h)
        self.hoverImage.resize(w, h)

        if self.standardPath == None:
            return
        pixmap = QPixmap(self.standardPath)
        self.standardImage.setPixmap(pixmap.scaled(self.size()))
        pixmap = QPixmap(self.pressedPath)
        self.pressedImage.setPixmap(pixmap.scaled(self.size()))
        pixmap = QPixmap(self.hoverPath)
        self.hoverImage.setPixmap(pixmap.scaled(self.size()))


    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.pressedImage.show()
        self.standardImage.hide()
        self.hoverImage.hide()



    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.pressedImage.hide()
        self.standardImage.show()
        if self.onBtnPos:
            self.hoverImage.show()


    def enterEvent(self, event):
        self.hoverImage.show()
        self.onBtnPos = True
        super().enterEvent(event)

        # Показываем подсказку
        if not self.isTooltip:
            return
        self.tooltipWidget.show()

    def leaveEvent(self, event):
        self.hoverImage.hide()
        self.onBtnPos = False
        super().leaveEvent(event)

        # Скрываем подсказку
        if not self.isTooltip:
            return
        self.tooltipWidget.hide()