import os
import json
import numpy as np
from utils import utils
import pyqtgraph as pg
from pprint import pprint
from add_ons.charts import fibonnaci
from utils import constants as cst
from libs.roi_manager import ROIManager
from libs.widgets.roi_lines import *
from PySide2 import QtCore, QtGui, QtWidgets
from pyqtgraph.parametertree.Parameter import Parameter, registerParameterType


from libs.graph.candlestick import CandlestickItem
from libs.events_handler import EventHandler

# TODO import from palette or Qss
color = (53, 53, 53)
pg.setConfigOption("background", color)
pg.setConfigOptions(antialias=True)



class GraphView(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent=parent)

        # Constants
        self.prices_axis = list()
        self.axis_right = None
        self.values = None
        self.ticker = None
        self.v_line = None
        self.h_line = None
        self.buy_line = None
        self.limit_line = None
        self.stop_line = None
        self.release = False
        self.pos = False

        self.signals = EventHandler()

        self.g_quotation = self.addPlot(row=0, col=0, name="Quotation")
        self.g_quotation.showGrid(x=True, y=True, alpha=0.3)
        self.g_vb = self.g_quotation.vb

        self.set_cross_hair()
        self.g_quotation.scene().sigMouseClicked.connect(
            self._on_mouse_clicked
        )

    def plot_quotation(self, data, ticker, clear=True):
        """Plot the quotation

        :param data: The data to plot
        :type data: pd.dataframe
        :param clear: Clear the graph before plot, defaults to True
        :type clear: bool, optional
        """
        self.ticker = ticker
        self.values = data
        if clear:
            self.g_quotation.clear()
        ls_data = []
        dates = [x.timestamp() for x in data.index]
        for index, (_time, _open, _close, _high, _low) in enumerate(
            zip(
                data.index,
                data[cst.OPEN].values,
                data[cst.CLOSE].values,
                data[cst.HIGH].values,
                data[cst.LOW].values,
            )
        ):
            ls_data.append((dates[index], _open, _close, _high, _low))
        item = CandlestickItem(ls_data)
        self.g_quotation.addItem(item)

        self.prices_axis.append(data[cst.CLOSE].iloc[-1])
        self.set_time_x_axis(widget=self.g_quotation)
        self.set_y_axis(widget=self.g_quotation)

        # Set Limit Graph from the price
        price_variation = (np.amax(data[cst.CLOSE])-np.amin(data[cst.CLOSE])) / 2

        self.range_view = (dates[-240], dates[-1])
        self.g_quotation.setXRange(self.range_view[0], self.range_view[1])
        self.g_quotation.setLimits(xMin=dates[0]-10000000,
                                   xMax=dates[-1]+10000000,
                                   yMin=np.amin(data[cst.CLOSE])-price_variation,
                                   yMax=np.amax(data[cst.CLOSE])+price_variation,
                                   )
        self.set_cross_hair()

    def set_cross_hair(self):
        """Set the cross hair"""
        color = (200, 200, 200)
        label_opts = {
            "position": 0.95,
            "color": color,
            "movable": True,
            "fill": (74, 74, 74),
        }
        pen = pg.mkPen(color, width=1, style=QtCore.Qt.DashLine)
        self.v_line = pg.InfiniteLine(angle=90, movable=False, pen=pen)
        self.h_line = pg.InfiniteLine(
            angle=0,
            movable=False,
            label="{value:0.3f}",
            labelOpts=label_opts,
            pen=pen,
        )
        self.g_quotation.addItem(self.v_line, ignoreBounds=True)
        self.g_quotation.addItem(self.h_line, ignoreBounds=True)
        self.g_quotation.scene().sigMouseMoved.connect(self._on_mouse_moved)

    def set_time_x_axis(self, widget):
        widget.setAxisItems({"bottom": pg.DateAxisItem(orientation="bottom")})

    def set_y_axis(self, widget):
        """Set Y Axis in Left and add Price.
        :param widget: GraphWidget
        :type widget: PQQt.GraphWidget
        :param data_close: Data Price cst.CLOSE
        :type data_close: DataFrame
        """
        widget.showAxis('right')
        self.axis_right = widget.getAxis('right')
        self._add_ticker_right_axis()

    def _add_ticker_right_axis(self):
        """This method append tickers in Right Axis.
        """
        prices = list()
        for price in self.prices_axis:
            prices.append((price, str(round(price, 1))))
        self.axis_right.setTicks([prices])

    @QtCore.Slot(object)
    def _on_mouse_moved(self, event):
        """Signal on mouse moved

        :param event: Mouse position
        :type event: QtCore.QPointF
        """
        sender = self.sender()
        if self.g_quotation.sceneBoundingRect().contains(event):
            mousePoint = self.g_vb.mapSceneToView(event)
            self.v_line.setPos(mousePoint.x())
            self.h_line.setPos(mousePoint.y())

    @QtCore.Slot(object)
    def _on_mouse_clicked(self, event):
        """Called on mouse clicked

        :param event: Mouse clicked
        :type event: event
        """
        items = self.g_quotation.scene().items(event.scenePos())
        plot_items = [x for x in items if isinstance(x, pg.PlotItem)]
        self.signals.sig_graph_clicked.emit(plot_items, event)

    def mousePressEvent(self, event):
        self.signals.sig_graph_mouse_pressed.emit(event)
        super(GraphView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.signals.sig_graph_mouse_released.emit(event)
        super(GraphView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.signals.sig_graph_mouse_moved.emit(event)
        super(GraphView, self).mouseMoveEvent(event)

    QtCore.Signal(dict)
    def draw_position(self, postions):
        if isinstance(postions, dict):
            postions = [postions]

        for position in postions:
            self.buy_line = pg.InfiniteLine(
                pos=position['price'],
                angle=0,
                movable=False,
                pen=pg.mkPen(color=(55, 110, 55),
                             style=QtCore.Qt.DashLine,
                             width=0.8),
                labelOpts=position['price'],
                )
            if position['order_execution'] == "LIMIT":
                self.limit_line =  pg.InfiniteLine(
                    pos=position['limit'],
                    angle=0,
                    movable=False,
                    pen=pg.mkPen(color=(110, 55, 55),
                                 style=QtCore.Qt.DashLine,
                                 width=0.8),
                    labelOpts=position['limit'],
                )
                self.g_quotation.addItem(self.limit_line)
                self.prices_axis.append(position['limit'])

            # if position['order_execution'] == "STOP":

            self.g_quotation.addItem(self.buy_line)
            self.prices_axis.append(position['price'])

        self._add_ticker_right_axis()

    def mouseDragEvent(self, ev, axis=None):
        self.updateScaleBox(ev.pos(), ev.pos())

    def save_items(self):
        path = os.path.join(os.environ.get("APP_HOME"),
                            "chart",
                            "{}_chart.json".format(self.ticker)
                            )
        if not self.ticker:
            return
        if utils.file_from_path(path):
            settings = list()
            for item in self.g_quotation.allChildItems():
                setting = dict()
                if isinstance(item, TrendLine):
                    setting['TrendLine'] = item.saveState()
                if isinstance(item, fibonnaci.FibonnaciROI):
                    setting['FibonnaciROI'] = item.saveState()
                if isinstance(item, VerticalLine):
                    setting['VerticalLine'] = {'pos': item.value()}
                if isinstance(item, HorizontalLine):
                    setting['HorizontalLine'] = {'pos': item.value()}
                if setting:
                    settings.append(setting)
            with open(path, 'w') as f:
                json.dump(settings, f, indent=4)

    def restore_items(self, parent, ticker):
        path = os.path.join(os.environ.get("APP_HOME"), "chart", "{}_chart.json".format(ticker))
        if os.path.isfile(path):
            with open(path, 'r') as f:
                setting = json.load(f)
            ROIManager.restore_items(self=parent, path=setting, graph=self.g_quotation)

class GraphWidget(QtWidgets.QWidget):
    """Widget wrapper for the graph"""

    def __init__(self, parent=None):
        super(GraphWidget, self).__init__(parent=parent)

        layout = QtWidgets.QHBoxLayout()
        self._graph = GraphView(parent=self)
        layout.addWidget(self._graph)
        self.setLayout(layout)

        self.signals = EventHandler()

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        # Relay Signals
        self._graph.signals.sig_graph_clicked.connect(
            self.signals.sig_graph_clicked.emit
        )
        self._graph.signals.sig_graph_mouse_pressed.connect(
            self.signals.sig_graph_mouse_pressed.emit
        )
        self._graph.signals.sig_graph_mouse_released.connect(
            self.signals.sig_graph_mouse_released.emit
        )
        self._graph.signals.sig_graph_mouse_moved.connect(
            self.signals.sig_graph_mouse_moved.emit
        )



    @property
    def graph(self):
        """Return the graph

        :return: The graph view
        :rtype: GraphView object
        """
        return self._graph

    def draw_resistance(self, *args, **kwargs):
        print("hello")


