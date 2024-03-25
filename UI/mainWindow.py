import sys
from time import sleep

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QPushButton
from ui.MainWindow import Ui_MainWindow
from ui.FLWindow import FLWindow
import ui.StyleSheet as qss
from ui.Message import Message


class AIThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, gpt_slot, input):
        super().__init__()
        self.gpt_slot = gpt_slot
        self.input = input

    def run(self):
        result = self.gpt_slot(self.input)
        self.finished.emit(result)


class NWindow(FLWindow):
    def __init__(self, role="User", gpt_slot=None):
        super().__init__()
        self.btn = None
        self.ui = None
        self.setWindowTitle('')
        self.setupUi()
        self.widget_list = []
        self.wait_reply = False
        self.setMouseTracking(True)
        self.restore = 0
        self.gpt_slot = gpt_slot
        self.role = role

    def setupUi(self):
        self.setMouseTracking(True)  # 启用鼠标跟踪
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.setStyleSheet("background-color:red;")

        # 发送按钮
        send_button = QPushButton("Send")
        send_button.setParent(self.ui.input_widget)
        send_button.setObjectName("send_button")
        send_button.raise_()
        self.btn = send_button

        # 输入区定位
        # input_widget.width不准确 实际为 self.size().width() - 10*2(边框*2)
        # input_edit 距input_widget右边界20
        self.ui.input_edit.setGeometry(20, 0, self.width() - 60, 100)
        # send_button 应距离input_edit右边界85
        send_button.setGeometry(self.size().width() - 140, 10, 85, 80)

        self.ui.input_edit.setStyleSheet(qss.input_edit)
        send_button.setStyleSheet(qss.send_button)
        self.ui.head_widget.setStyleSheet(qss.head_widget)

        # 滚动区内容新增-->滚动至底部
        self.ui.scroll_area.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom)

        self.ui.input_edit.set_send_fn(self.send_message)
        self.ui.resize_btn.clicked.connect(self.change_restore)
        send_button.clicked.connect(self.send_message)

    def resizeEvent(self, event):
        # 更新边界信息
        if self.l_press is False:
            self.update_edge_data()

        # 更新输入区定位
        self.btn.setGeometry(self.size().width() - 140, 10, 85, 80)
        self.ui.input_edit.setGeometry(20, 0, self.width() - 60, 100)

        # 更新所有Message布局
        for i in self.widget_list:
            i.update_size()

    def display_message(self, message, role):
        """
        :param message: 显示的信息
        :param role: 消息来源（角色）
        """
        msg = Message(message, role, parent=self.ui.scroll_widget)
        msg.setParent(self.ui.scroll_area)

        # 存入msg组件列表
        self.widget_list.append(msg)
        # 将消息添加到对话记录显示区域
        self.ui.scroll_widget_layout.addWidget(msg)
        # 保证消息从最上方开始放置
        self.ui.scroll_widget_layout.setAlignment(Qt.AlignTop)

    def scroll_to_bottom(self):
        self.ui.scroll_area.verticalScrollBar().setValue(
            self.ui.scroll_area.verticalScrollBar().maximum()
        )

    def send_message(self):
        # 获取用户输入
        user_input = self.ui.input_edit.toPlainText().strip()

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
        self.ui.input_edit.clear()

    def change_restore(self):
        if self.restore == 0:
            self.showFullScreen()
            self.restore = 1
        else:
            self.showNormal()
            self.restore = 0

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
        from ui.TestDocument import Database_test_list, AI_test
        return (Database_test_list, "DataBase"), (AI_test, "AI")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ai = TestAI()
    window = NWindow("User", ai.gpt_slot)
    ai.mainWindow = window
    window.show()
    sys.exit(app.exec_())
