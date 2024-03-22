from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


class HeadWidget(QWidget):
    def __init__(self, parent=None, mainWindow=None):
        super().__init__()
        self.setParent(parent)
        self.setWindowTitle('')
        self.mainWindow = mainWindow

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.mainWindow.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.mainWindow.move(event.globalPos() - self.drag_pos)
            event.accept()
