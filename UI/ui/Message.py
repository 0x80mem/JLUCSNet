from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from ui.roleInfo import roleInfo
from ui.avatar import AvatarLabel

class Message(QWidget):
    def __init__(self, text,role = "ChatGPT", parent=None):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout(self)

        topWidget = QWidget()
        topLayout = QHBoxLayout(topWidget)

        # 创建头像标签
        avatar_path = roleInfo.get(role)
        avatar_path = "" if avatar_path is None else avatar_path
        self.avatar = AvatarLabel(avatar_path, self)
        topLayout.addWidget(self.avatar)
        # 名字
        topLayout.addWidget(QLabel(
            "<p style='margin-left:10px;font-size:22px;font-family:微软雅黑;color:rgb(230, 230, 230);line-height:40px; "
            "width:100% ; white-space: pre-wrap; letter-spacing: 3px'>" + role + "</p>"))
        layout.addWidget(topWidget)

        # 创建文本Label
        self.text_Label = QLabel(self)
        self.text_Label.setWordWrap(True)
        layout.addWidget(self.text_Label)
        self.text_Label.setMinimumWidth(150)
        self.setMinimumHeight(150)
        # 设置默认文本
        self.setText(text)

        # # 添加红色边框样式
        # self.setStyleSheet("border: 2px solid red;")

    def setText(self, text):
        self.layout().removeWidget(self.text_Label)
        self.text_Label = QLabel(self)
        self.text_Label.setWordWrap(True)
        self.layout().addWidget(self.text_Label)
        ft = QFont()
        ft.setFamily("微软雅黑")
        ft.setPixelSize(27)
        self.text_Label.setFont(ft)
        self.setFixedWidth(self.parent.width() - 120)
        self.text_Label.setFixedWidth(self.width() - 20)
        text = ("<p style='margin-left:80px;color:rgb(240, 240, 240);line-height:20px; width:100% ; white-space: "
                  "pre-wrap; letter-spacing: 3px'>") + text + "</p>"
        self.text_Label.setText(text)

    def update_size(self):
        self.setFixedWidth(self.parent.width() - 120)
        self.setText(self.text_Label.text())
        self.repaint()
