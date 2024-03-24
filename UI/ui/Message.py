from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTextEdit, QGridLayout, QTextBrowser
from ui.roleInfo import roleInfo
from ui.Avatar import AvatarLabel
import ui.MsgBrowser as msgBrs


class Message(QWidget):
    def __init__(self, text, role="User", parent=None ):
        super().__init__(parent)
        self.msg_browser = None
        self.parent = parent
        self.setParent(parent)

        layout = QVBoxLayout(self)

        # 头像角色组件
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)

        # 创建头像标签
        avatar_path = roleInfo.get(role)
        avatar_path = "" if avatar_path is None else avatar_path
        self.avatar = AvatarLabel(avatar_path, self)
        top_layout.addWidget(self.avatar)

        # 角色名 + 样式
        top_layout.addWidget(QLabel(
            "<p style='margin-left:10px;font-size:22px;font-family:微软雅黑;color:rgb(230, 230, 230);line-height:40px; "
            "width:100% ; white-space: pre-wrap; letter-spacing: 3px'>" + role + "</p>"))

        layout.addWidget(top_widget)

        # 根据角色名生成对应MessageBrowser类 默认或异常时为User
        try:
            self.msg_browser = getattr(msgBrs, role + "MsgBrowser")(self)
        except AttributeError:
            self.msg_browser = msgBrs.UserMsgBrowser(self)

        # 向主布局加入browser并更新
        self.layout().addWidget(self.msg_browser)
        self.msg_browser.setText(text)

        # 更新组件尺寸适配内容
        self.update_size()

        # # 添加红色边框样式
        # self.setStyleSheet("border: 2px solid red;")

    # 根据主窗口变化更新组件size
    def update_size(self):

        # 设置主Widget和msg_browser宽度
        self.setFixedWidth(self.parent.width() - 120)
        self.msg_browser.setFixedWidth(self.width() - 20)

        # 休眠一段时间，等待组件更新获取具体数据并更新size
        QTimer.singleShot(10, self.set_real_height)

    # 设置本组件高度 使其恰好显示所有内容
    def set_real_height(self):
        text_height = int(self.msg_browser.document().size().height())
        self.setFixedHeight(text_height + 150)
        self.msg_browser.setFixedHeight(text_height + 35)
