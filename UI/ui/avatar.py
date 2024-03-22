from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QBrush, QColor
from PyQt5.QtCore import Qt

class AvatarLabel(QLabel):
    def __init__(self, image_path,parent=None):
        super().__init__(parent)
        self.setScaledContents(True)
        self.setAvatar(image_path)

    def setAvatar(self, image_path):
        # 加载头像图片
        original_image = QPixmap(image_path)
        self.image_path = image_path
        # 创建一个空白的圆形图片
        circle_image = QPixmap(original_image.size())
        circle_image.fill(Qt.transparent)

        # 在圆形图片上绘制圆形头像
        painter = QPainter(circle_image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(Qt.white)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, original_image.width(), original_image.height())
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)

        # 将原始图像绘制到圆形图像上
        painter.drawPixmap(0, 0, original_image)
        painter.end()

        # 设置圆形头像到QLabel中显示
        self.setPixmap(circle_image)

        self.setFixedSize(50,50)