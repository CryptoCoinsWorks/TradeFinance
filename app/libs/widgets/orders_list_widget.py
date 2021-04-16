from pprint import pprint
from datetime import datetime
from ui.order_list_widget import Ui_Form
from PySide2 import QtCore, QtWidgets, QtGui
from libs.events_handler import EventHandler

header = [
    'Ticker',
    'ID',
    'Date',
    'Type',
    'Volume',
    'S/L',
    'T/P',
    'Price',
    'Profit',
    "CLOSE"
]


class OrderList(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(OrderList, self).__init__()

        self.signals = EventHandler()
        self.setupUi(self)
        self.set_ui()

    def set_ui(self):
        self.list_wdg.setHeaderLabels(header)

    QtCore.Slot(list)
    def _load_positions(self, positions):
        for row, order in enumerate(positions):
            list_value = [order['ticker'],
                          str(order['id']),
                          str(datetime.fromtimestamp(order['date']).strftime('%Y-%m-%d %H:%M:%S')),
                          order['order_type'],
                          str(order['amount']),
                          order['limit'],
                          order['stop'],
                          str(order['price']),
                          str(order['id'])
                          ]
            item = QtWidgets.QTreeWidgetItem(self.list_wdg, list_value)
            close_btn = QtWidgets.QPushButton(text='X')
            close_btn.setObjectName('close_position')
            close_btn.setProperty('index', str(order['id']))
            close_btn.setProperty('item', item)
            close_btn.clicked.connect(self.close_position)
            self.list_wdg.setItemWidget(item, len(list_value), close_btn)

    def close_position(self):
        """
        This method delete the position from the file,
        and remove from te TableWidget.
        """
        ids = self.sender().property('index')
        item = self.sender().property('item')
        self.signals.sig_order_close.emit(int(ids))
        index_item = self.list_wdg.indexFromItem(item)
        self.list_wdg.takeTopLevelItem(index_item.row())