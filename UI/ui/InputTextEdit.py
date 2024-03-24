from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit


class InputTextEdit(QTextEdit):
    def __init__(self,parent=None):
        super().__init__()
        self.setParent(parent)
        self.send_fn = None

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if event.modifiers() & Qt.ShiftModifier:
                # 如果按下 Shift+Enter，插入换行符
                self.insertPlainText('\n')
            else:
                # 如果只按下 Enter，且设置了发送消息的函数，则调用该函数
                if self.send_fn is not None:
                    self.send_fn()
        else:
            super().keyPressEvent(event)

    def set_send_fn(self, fn):
        self.send_fn = fn
