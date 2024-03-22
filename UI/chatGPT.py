import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton, QScrollArea

from ui.Message import Message

class ChatGPTInterface(QMainWindow):

    def __init__(self, gpt=None):
        super().__init__()
        self.list = []
        self.gpt = gpt
        self.setWindowTitle("ChatGPT Interface")
        self.setGeometry(100, 100, 1200, 927)
        # self.setFixedSize(self.size())
        self.setStyleSheet("QMainWindow {padding: 0px; margin: 0px; border: none;background-color:rgb(255, 33, 33);border-radius:20px;}")
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # 创建主窗口布局
        layout = QVBoxLayout()
        # head_widget = HeadWidget(self)
        # head_widget.setObjectName("HeadWidget")
        #
        # layout.addWidget(head_widget)

        # 创建对话记录显示区域
        self.chat_area = QScrollArea()
        self.chat_area.setStyleSheet("background-color:rgb(33, 33, 33);border:none")
        self.chat_widget = QWidget()  # 创建一个QWidget来作为QScrollArea的子部件
        self.chat_area.setWidget(self.chat_widget)  # 设置QScrollArea的子部件为QWidget
        self.chat_widget_layout = QVBoxLayout(self.chat_widget)  # 用QVBoxLayout布局对话记录
        self.chat_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条
        self.chat_area.setWidgetResizable(True)  # 设置QScrollArea调整子部件的大小

        self.input_area = QWidget()
        self.input_area.setFixedHeight(100)

        # 创建文本输入框
        self.input_text = QTextEdit(self.input_area)

        self.input_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用垂直滚动条
        self.input_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条
        self.input_text.verticalScrollBar().setValue(self.input_text.verticalScrollBar().maximum())
        layout.addWidget(self.chat_area)

        # 创建发送按钮

        send_button = QPushButton("Send")
        send_button.setParent(self.input_area)
        send_button.raise_()
        send_button.setGeometry(self.size().width() - 120, 8, 85, 80)
        send_button.setStyleSheet(
            "QPushButton {"
            "outline: 1px solid #0000ff;"
            "background-color: rgb(48, 48, 48);"
            "color: rgb(158, 158, 158);"
            "border-radius:20px;"
            "padding: 2px;"
            "}"
            "QPushButton:hover{"
            "outline: 1px solid #0000ff;"
            "background-color: rgb(180, 180, 180);"
            "color: rgb(0, 0, 0);"
            "border-radius:20px;"
            "padding: 2px;"
            "}"
        )
        self.btn = send_button
        self.input_text.setGeometry(0, 0, self.size().width() - 26, 100)
        self.input_text.setStyleSheet(
            "font-family:微软雅黑;letter-spacing:3px;color:rgb(200, 200, 200);font-size:25px;padding-left:20px;padding-right:110px;padding-top:10px;border-radius: 30px;background-color:rgb(33, 33, 33);border: 1px solid rgb(68, 68, 68)")
        send_button.clicked.connect(self.send_message)

        # input_layout.addWidget(send_button)
        layout.addWidget(self.input_area)

        # 创建主窗口部件
        central_widget = QWidget()
        central_widget.setLayout(layout)
        central_widget.setObjectName("centralwidget")
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("QWidget#centralwidget{background-color:rgb(33, 33, 33);border-radius:20px;border-color:rgb(255, 0,0);}")
        self.chat_widget.setStyleSheet("background-color:rgb(33, 33, 33)")
        self.chat_area.verticalScrollBar().rangeChanged.connect(
            self.scroll_to_bottom,
        )

        self.chat_area.verticalScrollBar().setStyleSheet(
            "QScrollBar:vertical {"
            "    border: none;"
            "    background: transparent;"
            "    width: 10px;"  # 设置滚动条宽度
            "    margin: 0px 0px 0px 0px;"
            "}"
            "QScrollBar::handle:vertical {"
            "    background: #888888;"  # 设置滚动条滑块颜色
            "    min-height: 20px;"  # 设置滑块最小高度
            "}"
            "QScrollBar::add-line:vertical {"
            "    height: 0px;"  # 隐藏下箭头
            "}"
            "QScrollBar::sub-line:vertical {"
            "    height: 0px;"  # 隐藏上箭头
            "}"
        )

        # head_widget.setStyleSheet("QWidget{background-color: rgb(70, 70, 70) ;border-color:red}")

    def display_message(self, message):
        message.setParent(self.chat_widget)
        self.chat_widget.setFixedWidth(self.chat_area.width())
        # 将消息添加到对话记录显示区域
        self.chat_widget_layout.addWidget(message)
        self.chat_widget_layout.setAlignment(Qt.AlignTop)  # 保证新消息总是在顶部可见

    def scroll_to_bottom(self):
        self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()
        )

    def send_message(self):

        self.chat_widget.setFixedWidth(self.chat_area.width())
        # 获取用户输入
        user_input = self.input_text.toPlainText().strip()

        # 如果用户输入为空，则不处理
        if not user_input:
            return

        # 创建消息
        msg = Message("img/avatar.jpg", user_input, parent=self.chat_widget)
        msg.setText(user_input)
        self.display_message(msg)
        # 清空输入框
        self.input_text.clear()

        # 回复
        reply = "Unknown"*100
        if gpt is not None:
            reply = gpt(user_input)
        reply_msg = Message("img/chatGPT.png", reply, "ChatGPT", parent=self.chat_widget)
        self.display_message(reply_msg)

        self.list.append(msg)
        self.list.append(reply_msg)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.chat_widget.setFixedWidth(self.chat_area.width())
        self.btn.setGeometry(self.size().width() - 120, 8, 85, 80)
        self.input_text.setGeometry(0, 0, self.size().width() - 26, 100)
        for i in self.list:
            i.update_size()


# 获取回复
def gpt(msg):
    return "Unknown!"*100


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatGPTInterface(gpt)
    window.show()
    sys.exit(app.exec_())
