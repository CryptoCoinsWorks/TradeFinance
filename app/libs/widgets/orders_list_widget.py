from datetime import datetime
from utils import utils_orders
from ui.order_list_widget import Ui_Form
from PySide2 import QtCore, QtWidgets, QtGui
from libs.events_handler import EventHandler
from libs.io import order_setting
from libs.modify_order_dialog import ModifyOrderDialog

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
    "Close",
]


class OrderList(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(OrderList, self).__init__()

        self.signals = EventHandler()
        self.setupUi(self)
        self.set_ui()

    def set_ui(self):
        self.list_wdg.setHeaderLabels(header)
        self.list_wdg.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_wdg.customContextMenuRequested.connect(self.contextMenuEvent)
        self._set_size()

    QtCore.Slot(list)
    def _load_positions(self, positions):
        """Load Positions from the file and create it in TreeWidget.
        """
        if isinstance(positions, dict):
            positions = [positions]
        for row, position in enumerate(positions):
            list_value = [position['ticker'],
                          str(position['id']),
                          str(datetime.fromtimestamp(position['date']).strftime('%Y-%m-%d %H:%M:%S')),
                          position['order_type'],
                          str(position['amount']),
                          str(position['take_profit']),
                          str(position['stop_loss']),
                          str(round(position['price'], 2)),
                          str(round(order_setting.get_profits(position), 2))
                          ]
            item = QtWidgets.QTreeWidgetItem(self.list_wdg, list_value)

            # Button Close Position
            close_btn = QtWidgets.QPushButton(text='X')
            close_btn.setObjectName('close_position')
            close_btn.setMaximumSize(40, 50)
            close_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            close_btn.setProperty('index', str(position['id']))
            close_btn.setProperty('item', item)
            close_btn.clicked.connect(self.close_position)

            self.list_wdg.setItemWidget(item, len(list_value), close_btn)

    def _set_size(self):
        """This method set size of the header.
        """
        self.list_wdg.setColumnWidth(len(header) - 1, 10)
        self.list_wdg.header().setStretchLastSection(False)
        for index, i in enumerate(header[:-1]):
            self.list_wdg.setColumnWidth(index, 150)
            self.list_wdg.header().setSectionResizeMode(index, QtWidgets.QHeaderView.Fixed)

    def close_position(self, id=None, item=None):
        """ This method delete the position from the file,
        and remove from te TableWidget.
        """
        if not id:
            id = self.sender().property('index')
            item = self.sender().property('item')
        self.signals.sig_order_close.emit(int(id))
        index_item = self.list_wdg.indexFromItem(item)
        self.list_wdg.takeTopLevelItem(index_item.row())

    def modify_position(self, items):
        """This method open a new window from Modify Menu.
            Set StopLoss and Take Profit
            Change in TreeWidget, and the order.json
        """
        form = ModifyOrderDialog(parent=self, position=items)
        form.exec_()
        if form.result() == 0:
            position = form.position
            utils_orders.modify_order(position)
            item = self.list_wdg.topLevelItem(items[0].row())
            item.setText(5, str(position['take_profit']))
            item.setText(6, str(position['stop_loss']))

    def contextMenuEvent(self, event):
        """Create a Menu for each Item in the TreeWidget.
        """
        indexes = self.list_wdg.selectedIndexes()
        context_menu = QtWidgets.QMenu(self.list_wdg)
        modify = context_menu.addAction("Modify Order")
        close = context_menu.addAction("Close")

        action = context_menu.exec_(self.list_wdg.mapToGlobal(event))

        if action == modify:
            self.modify_position(indexes)
        if action == close:
            id = indexes[1].data(QtCore.Qt.DisplayRole)
            item = self.list_wdg.currentItem()
            self.close_position(id=id, item=item)
