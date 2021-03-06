import os
import json

from PySide2 import QtCore, QtGui, QtWidgets
import yfinance as yf

from libs.events_handler import EventHandler
from libs.tickers_dialog import TickersDialogWindow
from libs.widgets.busywidget import BusyIndicator
from libs.thread_pool import ThreadPool
from libs.io.order_setting import OrderSettings
from libs.io.favorite_settings import FavoritesManager
from libs.widgets.sentimentals_widget import Sentimental_Widget_Item
from libs.splashcreen import SplashScreen
from libs.roi_manager import ROIManager
from libs.login_view import LoginView

from ui import main_window

from utils import utils
from utils import utils_orders
from utils import constants as cst
from utils import db_models

SCRIPT_PATH = os.path.dirname(__file__)


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None, data=None):
        super(MainWindow, self).__init__(parent=parent)

        path = os.path.join(SCRIPT_PATH, cst.splashcreen)

        self.splash = SplashScreen(path, cst.TITLE)
        self.splash.show()
        self.splash.show_message("Loading UI...\n\n")
        QtWidgets.QApplication.processEvents()

        self.setupUi(self)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)

        # Constants
        self.tickers_dialog = None
        self.tool_bar.init_toolbar()

        # Load all components
        self._init_app_home()
        self.tickers_dialog = TickersDialogWindow(parent=self, tickers=data)
        self.busy_indicator = BusyIndicator(parent=self)
        self.thread_pool = ThreadPool()
        self.signals = EventHandler()
        self.favorites_manager = FavoritesManager(parent=self)
        self.orders_manager = OrderSettings(parent=self)
        self.roi_manager = ROIManager(parent=self)

        # Signals
        self.lie_ticker.mousePressEvent = self.tickers_dialog.show
        self.tickers_dialog.signal.sig_ticker_choosen.connect(
            self._on_ticker_selected
        )
        self.tickers_dialog.signal.sig_ticker_added_favorite.connect(
            self.favorites_manager._on_add_ticker_favorite
        )
        self.tickers_dialog.signal.sig_ticker_removed_favorite.connect(
            self.favorites_manager._on_remove_ticker_favorite
        )
        self.tickers_dialog.signal.sig_ticker_added_favorite.connect(
            self.wgt_favorites._on_favorite_added
        )
        self.tickers_dialog.signal.sig_ticker_removed_favorite.connect(
            self.wgt_favorites._on_favorite_removed
        )
        self.favorites_manager.signals.sig_favorite_loaded.connect(
            self.tickers_dialog._on_favorite_loaded
        )
        self.wgt_favorites.signals.sig_favorite_clicked.connect(
            self._on_ticker_selected
        )
        self.signals.sig_ticker_data_fetched.connect(
            self._on_process_ticker_data
        )
        self.signals.sig_ticker_infos_fetched.connect(
            self.wgt_company._on_ticker_infos
        )
        self.signals.sig_data.connect(
            self.wgt_order.get_data
        )
        self.tickers_dialog.signal.sig_ticker_choosen.connect(
            self._thread_articles
        )
        self.wgt_favorites.signals.sig_favorite_clicked.connect(
            self._thread_articles
        )
        self.wgt_favorites.signals.sig_favorite_clicked.connect(
            self._on_financials
        )
        self.tickers_dialog.signal.sig_ticker_choosen.connect(
            self._on_financials
        )
        self.thread_pool.signals.sig_thread_pre.connect(
            self.busy_indicator.show
        )
        self.thread_pool.signals.sig_thread_post.connect(
            self.busy_indicator.hide
        )
        self.wgt_indicators.signals.sig_indicator_switched.connect(
            self._on_indicator_switched
        )
        self.action_reload_indicators.triggered.connect(
            self.wgt_indicators.reload_indicators
        )
        self.tool_bar.signals.sig_action_triggered.connect(
            self._on_action_triggered
        )
        self.favorites_manager.signals.sig_favorite_loaded.connect(
            self.wgt_favorites._on_favorite_loaded
        )
        self.wgt_order.signals.sig_order_added.connect(
            self.orders_manager.save_orders
        )
        self.wgt_order.signals.sig_order_added.connect(
            self.wgt_graph.graph.draw_position
        )
        self.orders_manager.signals.sig_order_create.connect(
            self.wgt_order_list._load_positions
        )
        self.wgt_order_list.signals.sig_order_close.connect(
            self.orders_manager.close_order
        )
        self.orders_manager.signals.sig_order_loaded.connect(
            self.wgt_order_list._load_positions
        )
        self.top_toolbar.signals.sig_account.connect(
            self.load_account
        )

        self.pub_go_welcome.clicked.connect(self.stw_main.slide_in_prev)
        self.pub_go_graph.clicked.connect(self.stw_main.slide_in_next)
        self.pub_go_market_prev.clicked.connect(self.wgt_markets_2.slide_in_prev)
        self.pub_go_market_next.clicked.connect(self.wgt_markets_2.slide_in_next)

        # Action which needs to be loaded after all signals
        self.splash.show_message("Loading Favorites...\n\n")
        self.settings_datas()
        self.splash.hide()

    def _init_app_home(self):
        """Init the APP_HOME of the application"""
        base_path = os.path.expanduser("~")
        app_home = os.path.join(base_path, ".trade_finance")
        if not os.path.exists(app_home):
            try:
                os.makedirs(app_home)
            except Exception as error:
                print(error)
        os.environ["APP_HOME"] = app_home

    def _retrieve_data(self):
        """Retrieve data from the API"""
        tick = self.lie_ticker.text()
        ticker = yf.Ticker(tick)
        self.signals.sig_ticker_infos_fetched.emit(ticker.info)
        data = ticker.history(period=cst.PERIODE,
                              interval=cst.INTERVAL,
                              start=cst.START_DATE)
        self.signals.sig_ticker_data_fetched.emit(data)
        self.signals.sig_data.emit(tick, data)

    @QtCore.Slot(object)
    def _on_process_ticker_data(self, data):
        """Called when informations about the ticker are available.

        :param data: The data of the ticker
        :type data: panda dataframe
        """
        tick = self.lie_ticker.text()
        orders = utils_orders.check_ticker_orders(tick)
        self.wgt_graph.graph.plot_quotation(data=data, ticker=tick)
        self.wgt_graph.graph.restore_items(parent=self.roi_manager, ticker=tick)
        if orders:
            self.wgt_graph.graph.draw_position(orders)

        for indicator in self.wgt_indicators.indicators:
            if not indicator.enabled:
                continue
            # Remove indicator
            indicator.remove_indicator(graph_view=self.wgt_graph.graph)
            # Re create indicator
            indicator.create_indicator(graph_view=self.wgt_graph.graph)
        if self.stw_main.currentIndex() == 0:
            self.stw_main.slide_in_next()

    @QtCore.Slot(str)
    def _on_ticker_selected(self, ticker_name: str):
        """Callback on ticker selected from the ticker dialog

        :param ticker_name: The name of the selected ticker
        :type ticker_name: str
        """
        self.lie_ticker.setText(ticker_name)
        self.thread_pool.execution(function=self._retrieve_data)

    @QtCore.Slot(object, bool)
    def _on_indicator_switched(self, indicator: object, state: bool):
        """Callback on indicator activated from the indicator widget

        :param indicator: The selected indicator
        :type indicator: dict
        """
        if state:
            indicator.create_indicator(graph_view=self.wgt_graph.graph)
        else:
            indicator.remove_indicator(graph_view=self.wgt_graph.graph)

    @QtCore.Slot(str, dict)
    def _on_action_triggered(self, action: str, args: dict):
        """Callback on action triggered from the toolbar

        :param action: The action to find and call
        :type action: str
        :param args: Args for the action
        :type args: dict
        """
        action_obj = utils.find_method(module=action, obj=self)
        if action_obj:
            action_obj(**args)

    @QtCore.Slot(str)
    def set_sentiment_compagny(self, ticker):
        """This method set the sentimental widget for
        the select tick.
        """
        utils.clear_layout(self.financials_layout)
        widget = Sentimental_Widget_Item()
        self.thread_pool.execution(function=widget.set_sentimental_ui,
                                   ticker=ticker)
        self.financials_layout.addWidget(widget)

    @QtCore.Slot(str)
    def _on_financials(self, ticker):
        """Callback on ticker selected from favorites or ticker dialog.
           Get the fundamentals and the sentiments from the ticker.
        """
        self.set_sentiment_compagny(ticker)
        self.thread_pool.execution(function=self.wid_table_financ.on_set_financials_table,
                                   ticker=ticker)

    def _thread_articles(self, ticker):
        """This method get fundamentals in a threadpool.
        """
        self.wgt_articles._on_get_articles(ticker=ticker)

    def settings_datas(self):
        """This method set setting or get account from setting.
        """
        setting_path = os.path.join(os.getenv('APP_HOME'), "setting.json")
        if not os.path.exists(setting_path):
            with open(setting_path, 'w') as f:
                json.dump(dict(), f, indent=4)
                login_account = {}
        else:
            with open(setting_path, 'r') as f:
                login_account = json.load(f)['last_login']
        self.load_account(login_account)

    @QtCore.Slot(dict)
    def load_account(self, account):
        """This method load all the components and set a variable
            from a account.
        """
        cst.LOGIN = account
        self.favorites_manager.load_favorite()
        self.orders_manager.load_position()

    def resizeEvent(self, event):
        if self.tickers_dialog:
            self.tickers_dialog.move_to()

    def moveEvent(self, event):
        self.tickers_dialog = None
        if self.tickers_dialog:
            ...

    def closeEvent(self, event):
        self.favorites_manager.save_favorites()
        self.wgt_graph.graph.save_items()
