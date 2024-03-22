import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.main import Ui_MainWindow
from ui.Message import Message
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton


class MainWindow(QMainWindow):

    input_signal = pyqtSignal(str)
    def __init__(self,role="You",gpt_slot=None):
        super().__init__()
        self.btn = None
        self.role = role
        self.gpt_slot = gpt_slot
        self.widget_list = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, list)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("MainWindow{background-color:rgb(33,33,33);} ")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui.chat_area.setStyleSheet("")
        send_button = QPushButton("Send")
        send_button.setParent(self.ui.input_area)
        send_button.setObjectName("send_button")
        send_button.raise_()
        send_button.setGeometry(self.size().width() - 120, 8, 85, 80)
        send_button.setStyleSheet(
            "QPushButton {"
            "outline: 1px solid #0000ff;"
            "background-color: rgb(48, 48, 48);"
            "color: rgb(158, 158, 158);"
            "border-radius:20px;"
            "padding: 2px;"
            "margin-bottom:20px;"
            "}"
            "QPushButton:hover{"
            "outline: 1px solid #0000ff;"
            "background-color: rgb(180, 180, 180);"
            "color: rgb(0, 0, 0);"
            "border-radius:20px;"
            "padding: 2px;"
            "margin-bottom:20px;"
            "}"
        )
        self.btn = send_button
        self.ui.textEdit.setGeometry(20, 0, self.width() - 20, 100)
        self.ui.textEdit.setStyleSheet(
            "font-family:微软雅黑;letter-spacing:3px;color:rgb(200, 200, "
            "200);font-size:25px;padding-left:20px;padding-right:110px;padding-top:10px;margin-bottom:20px;border"
            "-radius:"
            "30px;background-color:rgb(33, 33, 33);border: 1px solid rgb(68, 68, 68)")
        send_button.clicked.connect(self.send_message)

        self.ui.head_widget.setStyleSheet("background-color: rgb(50,50,50); border: 1px solid")

        self.ui.chat_area.verticalScrollBar().rangeChanged.connect(
            self.scroll_to_bottom,
        )
        self.ui.chat_area.setAutoFillBackground(False)

        # 连接input信号和gpt槽
        self.input_signal.connect(self.gpt_slot)

    def resizeEvent(self, event):
        # super().resizeEvent(a0)
        self.ui.up_size()
        self.btn.setGeometry(self.width() - 120, 8, 85, 80)
        self.ui.textEdit.setGeometry(20, 0, self.width() - 40, 100)
        for i in self.widget_list:
            i.update_size()

    def display_message(self, message, role):
        msg = Message(message, role, parent=self.ui.chat_widget)
        msg.setParent(self.ui.chat_widget)
        self.ui.chat_widget.setFixedWidth(self.ui.chat_area.width())
        # 将消息添加到对话记录显示区域
        self.ui.chat_widget_layout.addWidget(msg)
        self.ui.chat_widget_layout.setAlignment(Qt.AlignTop)  # 保证新消息总是在顶部可见

    def scroll_to_bottom(self):
        self.ui.chat_area.verticalScrollBar().setValue(
            self.ui.chat_area.verticalScrollBar().maximum()
        )

    def send_message(self):

        self.ui.chat_widget.setFixedWidth(self.ui.chat_area.width())
        # 获取用户输入
        user_input = self.ui.textEdit.toPlainText().strip()

        # 如果用户输入为空，则不处理
        if not user_input:
            return

        self.input_signal.emit(user_input)


        self.display_message(user_input,self.role)
        # 清空输入框
        self.ui.textEdit.clear()


    def show(self):
        super().show()
        self.ui.chat_widget.setFixedWidth(self.ui.chat_area.width())



def gpt_slot(user_input):
    print("is a slot ")
    print(user_input)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("You",gpt_fn)
    window.show()

    sys.exit(app.exec_())
