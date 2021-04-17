# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'order.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(500, 350)
        Form.setMinimumSize(QSize(300, 350))
        Form.setMaximumSize(QSize(500, 350))
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.buy_btn = QPushButton(Form)
        self.buy_btn.setObjectName(u"buy_btn")

        self.horizontalLayout_2.addWidget(self.buy_btn)

        self.sell_btn = QPushButton(Form)
        self.sell_btn.setObjectName(u"sell_btn")

        self.horizontalLayout_2.addWidget(self.sell_btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.order_wgt = QTabWidget(Form)
        self.order_wgt.setObjectName(u"order_wgt")
        self.order_wgt.setStyleSheet(u"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_market = QGroupBox(self.tab)
        self.groupBox_market.setObjectName(u"groupBox_market")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_market)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.groupBox_market)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(75, 0))
        self.label.setMaximumSize(QSize(75, 100))

        self.horizontalLayout_3.addWidget(self.label)

        self.box_quantity_market = QSpinBox(self.groupBox_market)
        self.box_quantity_market.setObjectName(u"box_quantity_market")
        self.box_quantity_market.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.box_quantity_market.setMaximum(999999)

        self.horizontalLayout_3.addWidget(self.box_quantity_market)

        self.line = QFrame(self.groupBox_market)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_3.addWidget(self.line)

        self.currency = QLabel(self.groupBox_market)
        self.currency.setObjectName(u"currency")
        self.currency.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.currency)


        self.verticalLayout_2.addWidget(self.groupBox_market)

        self.line_2 = QFrame(self.tab)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.verticalSpacer = QSpacerItem(20, 277, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.order_wgt.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_2 = QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_8 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(75, 0))
        self.label_2.setMaximumSize(QSize(75, 100))

        self.horizontalLayout_8.addWidget(self.label_2)

        self.box_quantity_limit = QSpinBox(self.groupBox_2)
        self.box_quantity_limit.setObjectName(u"box_quantity_limit")
        self.box_quantity_limit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.box_quantity_limit.setMaximum(999999)

        self.horizontalLayout_8.addWidget(self.box_quantity_limit)

        self.line_3 = QFrame(self.groupBox_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_8.addWidget(self.line_3)

        self.currency_2 = QLabel(self.groupBox_2)
        self.currency_2.setObjectName(u"currency_2")
        self.currency_2.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_8.addWidget(self.currency_2)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_9 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(75, 0))
        self.label_4.setMaximumSize(QSize(75, 100))

        self.horizontalLayout_9.addWidget(self.label_4)

        self.box_limit_price = QSpinBox(self.groupBox_3)
        self.box_limit_price.setObjectName(u"box_limit_price")
        self.box_limit_price.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.box_limit_price.setMaximum(999999)

        self.horizontalLayout_9.addWidget(self.box_limit_price)

        self.line_4 = QFrame(self.groupBox_3)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_9.addWidget(self.line_4)

        self.currency_3 = QLabel(self.groupBox_3)
        self.currency_3.setObjectName(u"currency_3")
        self.currency_3.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_9.addWidget(self.currency_3)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.groupBox_7 = QGroupBox(self.tab_2)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.horizontalLayout_14 = QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_7 = QLabel(self.groupBox_7)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(75, 0))
        self.label_7.setMaximumSize(QSize(75, 100))

        self.horizontalLayout_14.addWidget(self.label_7)

        self.combo_time = QComboBox(self.groupBox_7)
        self.combo_time.setObjectName(u"combo_time")
        self.combo_time.setMinimumSize(QSize(292, 0))

        self.horizontalLayout_14.addWidget(self.combo_time)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.groupBox_7)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.order_wgt.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout = QVBoxLayout(self.tab_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_5 = QGroupBox(self.tab_3)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout_11 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_5 = QLabel(self.groupBox_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(75, 0))
        self.label_5.setMaximumSize(QSize(75, 100))

        self.horizontalLayout_11.addWidget(self.label_5)

        self.box_quantity_stop = QSpinBox(self.groupBox_5)
        self.box_quantity_stop.setObjectName(u"box_quantity_stop")
        self.box_quantity_stop.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.box_quantity_stop.setMaximum(999999)

        self.horizontalLayout_11.addWidget(self.box_quantity_stop)

        self.line_6 = QFrame(self.groupBox_5)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_11.addWidget(self.line_6)

        self.currency_5 = QLabel(self.groupBox_5)
        self.currency_5.setObjectName(u"currency_5")
        self.currency_5.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_11.addWidget(self.currency_5)


        self.verticalLayout.addWidget(self.groupBox_5)

        self.groupBox_4 = QGroupBox(self.tab_3)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_10 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_8 = QLabel(self.groupBox_4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(75, 0))
        self.label_8.setMaximumSize(QSize(75, 100))

        self.horizontalLayout_10.addWidget(self.label_8)

        self.box_stop_price = QSpinBox(self.groupBox_4)
        self.box_stop_price.setObjectName(u"box_stop_price")
        self.box_stop_price.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.box_stop_price.setMaximum(999999)

        self.horizontalLayout_10.addWidget(self.box_stop_price)

        self.line_5 = QFrame(self.groupBox_4)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_10.addWidget(self.line_5)

        self.currency_4 = QLabel(self.groupBox_4)
        self.currency_4.setObjectName(u"currency_4")
        self.currency_4.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_10.addWidget(self.currency_4)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_6 = QGroupBox(self.tab_3)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.horizontalLayout_12 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_6 = QLabel(self.groupBox_6)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(75, 0))
        self.label_6.setMaximumSize(QSize(75, 100))

        self.horizontalLayout_12.addWidget(self.label_6)

        self.box_limit_price_stop = QSpinBox(self.groupBox_6)
        self.box_limit_price_stop.setObjectName(u"box_limit_price_stop")
        self.box_limit_price_stop.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.box_limit_price_stop)

        self.line_7 = QFrame(self.groupBox_6)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.VLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_12.addWidget(self.line_7)

        self.currency_6 = QLabel(self.groupBox_6)
        self.currency_6.setObjectName(u"currency_6")
        self.currency_6.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_12.addWidget(self.currency_6)


        self.verticalLayout.addWidget(self.groupBox_6)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.order_wgt.addTab(self.tab_3, "")

        self.verticalLayout_4.addWidget(self.order_wgt)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.lb_total = QLabel(Form)
        self.lb_total.setObjectName(u"lb_total")

        self.horizontalLayout_13.addWidget(self.lb_total)

        self.lb_price = QLabel(Form)
        self.lb_price.setObjectName(u"lb_price")
        self.lb_price.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.lb_price)

        self.lb_currency = QLabel(Form)
        self.lb_currency.setObjectName(u"lb_currency")
        self.lb_currency.setMaximumSize(QSize(10, 16777215))

        self.horizontalLayout_13.addWidget(self.lb_currency)


        self.verticalLayout_4.addLayout(self.horizontalLayout_13)

        self.btn_order = QPushButton(Form)
        self.btn_order.setObjectName(u"btn_order")

        self.verticalLayout_4.addWidget(self.btn_order)


        self.retranslateUi(Form)

        self.order_wgt.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Buy Sell Window", None))
        self.buy_btn.setText(QCoreApplication.translate("Form", u"BUY", None))
        self.sell_btn.setText(QCoreApplication.translate("Form", u"SELL", None))
        self.groupBox_market.setTitle("")
        self.label.setText(QCoreApplication.translate("Form", u"Amount", None))
        self.currency.setText(QCoreApplication.translate("Form", u"Stocks", None))
        self.order_wgt.setTabText(self.order_wgt.indexOf(self.tab), QCoreApplication.translate("Form", u"MARKET", None))
        self.groupBox_2.setTitle("")
        self.label_2.setText(QCoreApplication.translate("Form", u"Amount", None))
        self.currency_2.setText(QCoreApplication.translate("Form", u"Shares", None))
        self.groupBox_3.setTitle("")
        self.label_4.setText(QCoreApplication.translate("Form", u"Limit Price", None))
        self.currency_3.setText(QCoreApplication.translate("Form", u"EUR", None))
        self.groupBox_7.setTitle("")
        self.label_7.setText(QCoreApplication.translate("Form", u"Date", None))
        self.order_wgt.setTabText(self.order_wgt.indexOf(self.tab_2), QCoreApplication.translate("Form", u"LIMIT", None))
        self.groupBox_5.setTitle("")
        self.label_5.setText(QCoreApplication.translate("Form", u"Amount", None))
        self.currency_5.setText(QCoreApplication.translate("Form", u"EUR", None))
        self.groupBox_4.setTitle("")
        self.label_8.setText(QCoreApplication.translate("Form", u"Stop Price", None))
        self.currency_4.setText(QCoreApplication.translate("Form", u"EUR", None))
        self.groupBox_6.setTitle("")
        self.label_6.setText(QCoreApplication.translate("Form", u"Limit Price", None))
        self.currency_6.setText(QCoreApplication.translate("Form", u"EUR", None))
        self.order_wgt.setTabText(self.order_wgt.indexOf(self.tab_3), QCoreApplication.translate("Form", u"STOP", None))
        self.lb_total.setText(QCoreApplication.translate("Form", u"Total :", None))
        self.lb_price.setText(QCoreApplication.translate("Form", u"50.00", None))
        self.lb_currency.setText(QCoreApplication.translate("Form", u"\u20ac", None))
        self.btn_order.setText(QCoreApplication.translate("Form", u"PLACE BUY ORDER", None))
    # retranslateUi

