from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QEnterEvent
from PyQt5.QtWidgets import QMainWindow


class FLWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize_edge = None
        self.l_press = False
        self.direction = None
        self.edge = {}
        self.edge_mouse = {}
        self.init_edge()

    def init_edge(self):
        self.installEventFilter(self)
        self.edge_mouse = {
            'left': Qt.SizeHorCursor,
            'right': Qt.SizeHorCursor,
            'top': Qt.SizeVerCursor,
            'bottom': Qt.SizeVerCursor,
            'lt': Qt.SizeFDiagCursor,
            'rb': Qt.SizeFDiagCursor,
            'lb': Qt.SizeBDiagCursor,
            'rt': Qt.SizeBDiagCursor,
        }
        self.resize_edge = {
            'left': Qt.LeftEdge,
            'right': Qt.RightEdge,
            'top': Qt.TopEdge,
            'bottom': Qt.BottomEdge,
            'lt': Qt.LeftEdge | Qt.TopEdge,
            'rb': Qt.RightEdge | Qt.BottomEdge,
            'lb': Qt.LeftEdge | Qt.BottomEdge,
            'rt': Qt.TopEdge | Qt.RightEdge,
        }
        # 关闭系统标题栏
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint)
        self.setMouseTracking(True)

    def update_edge_data(self):
        height = self.height()
        width = self.width()
        self.edge['top'] = QRect(20, 0, width - 40, 20)
        self.edge['bottom'] = QRect(20, height - 20, width - 40, 20)
        self.edge['left'] = QRect(0, 20, 20, height - 40)
        self.edge['right'] = QRect(width - 20, 20, 20, height - 40)
        self.edge['lt'] = QRect(0, 0, 20, 20)
        self.edge['lb'] = QRect(0, height - 20, 20, 20)
        self.edge['rt'] = QRect(width - 20, 0, 20, 20)
        self.edge['rb'] = QRect(width - 20, height - 20, 20, 20)


    def mouseMoveEvent(self, event):
        # print(event.x(), event.y())
        self.change_mouse_cursor(event=event)

    # 窗口边缘调整窗口大小
    def mousePressEvent(self, event):
        if self.direction is not None:
            self.resize_window(event=event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.left_btn_released()

    def left_btn_released(self):
        self.l_press = False
        self.update_edge_data()

    # def resizeEvent(self, a0):
    #     if self.l_press is False:
    #         self.update_edge_data()

    def resize_window(self, btn=None, event=None):

        if self.direction is None:
            return

        if btn is None:
            btn = event.button()

        if btn == Qt.LeftButton:
            self.l_press = True
            self.windowHandle().startSystemResize(self.resize_edge[self.direction])

    def change_mouse_cursor(self, pos=None, event=None):
        # 作为槽函数时使用pos
        if pos is None:
            pos = event.pos()

        if self.l_press:
            return
            # 根据鼠标在窗口的位置 改变鼠标手势
        if self.isMaximized():
            return

        is_in_edge = False
        for key in self.edge:
            if self.edge[key].contains(pos):
                self.direction = key
                self.setCursor(self.edge_mouse[key])
                is_in_edge = True
                break
        # 不在边缘则回复正常指针
        if is_in_edge is False:
            self.direction = None
            self.setCursor(Qt.ArrowCursor)

    def eventFilter(self, obj, event):

        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
            self.direction = None
        return super().eventFilter(obj, event)


#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = FLWindow()
#     window.setGeometry(1000, 1000, 400, 300)
#     window.show()
#     sys.exit(app.exec_())
