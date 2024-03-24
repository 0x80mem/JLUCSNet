import sys
from time import sleep

import ui.TestDocument
from ui.FLWindow import FLWindow
from PyQt5.QtWidgets import QApplication
from ui.main import Ui_MainWindow
from ui.Message import Message
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import QPushButton
import ui.StyleSheet as qss


class AIThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, gpt_slot, input):
        super().__init__()
        self.gpt_slot = gpt_slot
        self.input = input

    def run(self):
        result = self.gpt_slot(self.input)
        self.finished.emit(result)


class MainWindow(FLWindow):
    input_signal = pyqtSignal(str)

    def __init__(self, role="User", gpt_slot=None):
        super().__init__()

        self.wait_reply = False
        self.setMouseTracking(True)
        self.restore = 0
        self.btn = None
        self.role = role
        self.gpt_slot = gpt_slot
        self.widget_list = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_ui()

    def setup_ui(self):
        self.init_edge()
        self.setMouseTracking(True)  # 启用鼠标跟踪
        self.setWindowFlag(Qt.FramelessWindowHint)

        # 发送按钮
        send_button = QPushButton("Send")
        send_button.setParent(self.ui.input_area)
        send_button.setObjectName("send_button")
        send_button.raise_()
        self.btn = send_button

        # 输入区定位
        send_button.setGeometry(self.size().width() - 120, 8, 85, 80)
        self.ui.textEdit.setGeometry(20, 0, self.width() - 20, 100)

        # 设置样式表
        self.ui.textEdit.setStyleSheet(qss.input_edit)
        self.setStyleSheet(qss.mainWindow)
        self.ui.head_widget.setStyleSheet(qss.head_widget)
        send_button.setStyleSheet(qss.send_button)

        # 连接input信号和gpt槽
        self.input_signal.connect(self.gpt_slot)
        # 连接发送按钮和发送
        send_button.clicked.connect(self.send_message)
        # 滚动区内容新增-->滚动至底部
        self.ui.chat_area.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom, )

    def resizeEvent(self, event):
        # 更新边界信息
        if self.l_press is False:
            self.update_edge_data()

        # 更新显示区size
        self.ui.chat_widget.setFixedWidth(self.ui.chat_area.width())
        # 更新输入区定位
        self.btn.setGeometry(self.width() - 120, 8, 85, 80)
        self.ui.textEdit.setGeometry(20, 0, self.width() - 40, 100)
        self.ui.head_widget.setFixedWidth(self.width())
        # 更新所有Message布局
        for i in self.widget_list:
            i.update_size()

    def display_message(self, message, role):
        """
        :param message: 显示的信息
        :param role: 消息来源（角色）
        """
        msg = Message(message, role, parent=self.ui.chat_widget)
        msg.setParent(self.ui.chat_widget)
        self.setFixedWidth(self.width())
        # 存入msg组件列表
        self.widget_list.append(msg)
        # 将消息添加到对话记录显示区域
        self.ui.chat_widget_layout.addWidget(msg)
        # 保证消息从最上方开始放置
        self.ui.chat_widget_layout.setAlignment(Qt.AlignTop)
        self.ui.chat_widget.setFixedWidth(self.ui.chat_area.width())

    def scroll_to_bottom(self):
        self.ui.chat_area.verticalScrollBar().setValue(
            self.ui.chat_area.verticalScrollBar().maximum()
        )


    def send_message(self):

        # 固定主窗口size 避免子组件对主窗口size造成影响
        self.ui.chat_widget.setFixedWidth(self.ui.chat_area.width())

        # 获取用户输入
        user_input = self.ui.textEdit.toPlainText().strip()

        # 如果用户输入为空，则不处理
        if not user_input or self.wait_reply:
            return
        # user_input = "```\n"+user_input+"\n```"

        ai_thread = AIThread(self.gpt_slot, user_input)
        ai_thread.setParent(self)
        ai_thread.finished.connect(self.get_reply)
        ai_thread.start()
        self.wait_reply = True
        self.display_message(user_input, self.role)
        # 清空输入框
        self.ui.textEdit.clear()

    def change_restore(self):
        if self.restore == 0:
            self.showFullScreen()
            self.restore = 1
        else:
            self.showNormal()
            self.restore = 0

    def show(self):
        super().show()
        self.ui.chat_widget.setFixedWidth(self.ui.chat_area.width())
        self.ui.textEdit.set_send_fn(self.send_message)
        self.ui.restore_btn.clicked.connect(self.change_restore)

    def get_reply(self, result):
        self.display_message(result[0][0], result[0][1])
        self.display_message(result[1][0], result[1][1])
        self.wait_reply = False


class TestAI:
    def __init__(self):
        self.mainWindow = None

    def gpt_slot(self, user_input):
        print("is a slot ")
        print("process input: ", user_input)
        sleep(2)
        # 返回元组 (reply1,role1),(reply2,role2)
        return (ui.TestDocument.Database_test_list, "DataBase"), (ui.TestDocument.AI_test, "AI")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ai = TestAI()
    window = MainWindow("User", ai.gpt_slot)
    ai.mainWindow = window
    window.show()

    # # # User 测试
    # window.display_message("写一段Helo world 代码", "User")
    # # DataBase 测试
    # window.display_message(ui.TestDocument.Database_test_list, "DataBase")
    # # AI 测试
    # window.display_message(ui.TestDocument.AI_test, "AI")
    # # System 测试
    # window.display_message("output error", "System")

    sys.exit(app.exec_())
