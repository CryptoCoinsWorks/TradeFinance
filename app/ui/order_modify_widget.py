# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'order_modify_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(330, 200)
        Dialog.setMinimumSize(QSize(300, 200))
        Dialog.setMaximumSize(QSize(330, 200))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lb_ticker = QLabel(Dialog)
        self.lb_ticker.setObjectName(u"lb_ticker")
        self.lb_ticker.setMinimumSize(QSize(0, 9))
        self.lb_ticker.setMaximumSize(QSize(16777215, 9))
        self.lb_ticker.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lb_ticker)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_stoploss = QLabel(self.groupBox)
        self.label_stoploss.setObjectName(u"label_stoploss")
        self.label_stoploss.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.label_stoploss)

        self.box_stop = QDoubleSpinBox(self.groupBox)
        self.box_stop.setObjectName(u"box_stop")
        self.box_stop.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.box_stop.setMaximum(999999999.990000009536743)

        self.horizontalLayout.addWidget(self.box_stop)

        self.label_price = QLabel(self.groupBox)
        self.label_price.setObjectName(u"label_price")
        self.label_price.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.label_price)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_takeprofit = QLabel(self.groupBox_2)
        self.label_takeprofit.setObjectName(u"label_takeprofit")
        self.label_takeprofit.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_2.addWidget(self.label_takeprofit)

        self.box_profit = QDoubleSpinBox(self.groupBox_2)
        self.box_profit.setObjectName(u"box_profit")
        self.box_profit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.box_profit.setMaximum(999999999.990000009536743)

        self.horizontalLayout_2.addWidget(self.box_profit)

        self.label_price2 = QLabel(self.groupBox_2)
        self.label_price2.setObjectName(u"label_price2")
        self.label_price2.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.label_price2)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(40, 40, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.button_modify = QPushButton(Dialog)
        self.button_modify.setObjectName(u"button_modify")

        self.verticalLayout.addWidget(self.button_modify)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Modify Order", None))
        self.lb_ticker.setText(QCoreApplication.translate("Dialog", u"Ticker", None))
        self.groupBox.setTitle("")
        self.label_stoploss.setText(QCoreApplication.translate("Dialog", u"Stop Loss :", None))
        self.label_price.setText(QCoreApplication.translate("Dialog", u"-0.0\u20ac", None))
        self.groupBox_2.setTitle("")
        self.label_takeprofit.setText(QCoreApplication.translate("Dialog", u"Take Profit :", None))
        self.label_price2.setText(QCoreApplication.translate("Dialog", u"0.0\u20ac", None))
        self.button_modify.setText(QCoreApplication.translate("Dialog", u"MODIFY ORDER", None))
    # retranslateUi

