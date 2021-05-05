import os
import json

from PySide2 import QtCore, QtGui, QtWidgets
import qtawesome as qta

from libs.events_handler import EventHandler
from libs.login_view import LoginView
import resources_rc


class Main_ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent=None):
        super(Main_ToolBar, self).__init__(parent=parent)

        self.signals = EventHandler()

        self.setMovable(False)
        self.setIconSize(QtCore.QSize(20, 20))
        self.login = LoginView(parent=self)

        account = QtWidgets.QAction(QtGui.QIcon('D:\\Desk\\python\\TradeFinance\\app\\resources\svg\\account.svg'), 'Account', self)
        account.triggered.connect(self.launch_login)

        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(10)
        self.layout().setContentsMargins(0, 0, 0, 0)

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.addWidget(spacer)
        self.addAction(account)

    def launch_login(self):
        self.login.show()
