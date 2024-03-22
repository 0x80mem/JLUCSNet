# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize

from ui.HeadWidget import HeadWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, list):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 930)
        self.list = []
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        # self.head_widget = QtWidgets.QWidget(self.centralwidget)
        self.head_widget = HeadWidget(self.centralwidget, MainWindow)
        self.head_widget.setObjectName("head_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.head_widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.h_widget = QtWidgets.QWidget(self.head_widget)
        self.h_widget.setStyleSheet("")
        self.h_widget.setObjectName("h_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.h_widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(385, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.minBtn = QtWidgets.QPushButton(self.h_widget)
        self.minBtn.setObjectName("minBtn")
        self.horizontalLayout_2.addWidget(self.minBtn)
        self.restore = QtWidgets.QPushButton(self.h_widget)
        self.restore.setObjectName("maxBtn")
        self.horizontalLayout_2.addWidget(self.restore)
        self.exitBtn = QtWidgets.QPushButton(self.h_widget)
        self.exitBtn.setObjectName("exitBtn")
        self.horizontalLayout_2.addWidget(self.exitBtn)
        self.gridLayout.addWidget(self.h_widget, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.head_widget)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.msg_widget = QtWidgets.QWidget(self.widget_3)
        self.msg_widget.setObjectName("msg_widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.msg_widget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.msg_widget.setStyleSheet("border:none")
        self.chat_area = QtWidgets.QScrollArea(self.msg_widget)
        self.chat_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setObjectName("chat_area")

        self.chat_widget = QtWidgets.QWidget()
        self.chat_widget.setGeometry(QtCore.QRect(0, 0, 647, 446))
        self.chat_widget.setObjectName("chat_widget")

        self.chat_widget_layout = QtWidgets.QGridLayout(self.chat_widget)
        self.chat_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_widget_layout.setSpacing(0)
        self.chat_widget_layout.setObjectName("chat_widget_layout")
        self.chat_area.setWidget(self.chat_widget)
        self.gridLayout_3.addWidget(self.chat_area, 0, 0, 1, 1)

        self.verticalLayout.addWidget(self.msg_widget)

        self.input_area = QtWidgets.QWidget(self.widget_3)
        self.input_area.setObjectName("input_area")
        self.input_area.setFixedHeight(100)

        self.textEdit = QtWidgets.QTextEdit(self.input_area)
        self.textEdit.setObjectName("textEdit")

        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用垂直滚动条
        self.textEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条
        self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum())

        self.verticalLayout.addWidget(self.input_area)

        self.verticalLayout.setStretch(0, 7)
        self.verticalLayout.setStretch(1, 1)
        self.horizontalLayout.addWidget(self.widget_3)
        self.horizontalLayout.setStretch(0, 3)
        self.verticalLayout_2.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.minBtn.clicked.connect(MainWindow.showMinimized)  # type: ignore
        self.restore.clicked.connect(MainWindow.showFullScreen)  # type: ignore
        self.exitBtn.clicked.connect(MainWindow.close)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.exitBtn.setStyleSheet("QPushButton{"
                                   "    border-image:url(./img/close.png);"
                                   "}"
                                   "QPushButton::hover{"
                                   "    border-image:url(./img/close_hover.png);"
                                   "}"
                                   ""
                                   )
        self.minBtn.setStyleSheet("QPushButton{"
                                  "    border-image:url(./img/minus.png);"
                                  "}"
                                  "QPushButton::hover{"
                                  "    border-image:url(./img/minus_hover.png);"
                                  "}"
                                  ""
                                  )
        self.restore.setStyleSheet("QPushButton{"
                                   "    border-image:url(./img/restore.png);"
                                   "}"
                                   "QPushButton::hover{"
                                   "    border-image:url(./img/restore_hover.png);"
                                   "}"
                                   ""
                                   )
        self.chat_widget.setStyleSheet("QWidget#chat_widget{border:none; background-color:rgb(33,33,33);}")
        self.h_widget.setStyleSheet("QPushButton {"
                                    "   width: 40px;"
                                    "   height: 40px;"
                                    "   border: none;"
                                    "   border-radius:10px;"
                                    "}"
                                    )
        self.chat_area.verticalScrollBar().setStyleSheet(
            "QScrollBar:vertical {"
            "    border: none;"
            "    background: rgb(50,50,50);"
            "    width: 10px;"  # 设置滚动条宽度
            "    margin: 0px 0px 0px 0px;"
            "}"
            "QScrollBar::handle:vertical {"
            "    background: transparent;"  # 设置滚动条滑块颜色
            "    min-height: 20px;"  # 设置滑块最小高度
            "}"
            "QScrollBar::add-line:vertical {"
            "    height: 0px;"  # 隐藏下箭头

            "}"
            "QScrollBar::sub-line:vertical {"
            "    height: 0px;"  # 隐藏上箭头

            "}"
            "QScrollBar::sub-page:vertical {"
            "    background: rgb(33,33,33);"

            "}"
            "QScrollBar::add-page:vertical {"
            "    background: rgb(33,33,33);"

            "}"
            "QScrollBar::handle::hover:vertical {"
            "    background: rgb(66,66,66);"

            "}"

        )


    def up_size(self):
        self.chat_widget.setFixedWidth(self.chat_area.width())