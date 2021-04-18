import numpy as np
import pyqtgraph as pg

from utils import utils
from utils import constants as cst
from libs.graph.bargraph import BarGraphItem
from utils.indicators_utils import Indicator, InputField, ChoiceField

from PySide2 import QtCore, QtGui


class Stochastic(Indicator):
    def __init__(self):
        super(Stochastic, self).__init__()

        self.name = "Stochastic"
        self.description = "Momentum is use to spot trend reversals."

        self.g_moment = None

        # Define and register all customisable settings
        field_k = InputField("K", value=14, color=(0, 148, 255), width=2)
        field_d = InputField("D", value=3, color=(255, 82, 82), width=2)
        self.register_fields(
            field_k,
            field_d
        )

    def create_indicator(self, graph_view, *args, **kwargs):
        super(Stochastic, self).create_indicator(self, graph_view)

        # Get values
        values = graph_view.values
        self.quotation_plot = graph_view.g_quotation

        # Init plot
        self.g_stock = graph_view.addPlot(
            row=2, col=0, width=1, title="<b>{name}</b>".format(name=self.name)
        )
        self.g_stock.setMaximumHeight(150)
        self.g_stock.showGrid(x=True, y=True, alpha=0.3)
        self.g_stock.setXLink("Quotation")

        # Retrive settings
        field_k = self.get_field("K")
        field_d = self.get_field("D")

        data = self.stockastic_calcul(data=values,
                                      k=field_k.value,
                                      d=field_d.value)

        # Calculations
        # Skip the 11 first days
        self.g_stock.plot(
            x=[x.timestamp() for x in values.index],
            y=data['%K'],
            pen=pg.mkPen(
                field_k.color,
                width=field_k.width,
                style=field_k.line_style,
            ),
        )
        self.g_stock.plot(
            x=[x.timestamp() for x in values.index],
            y=data['%D'],
            pen=pg.mkPen(
                field_d.color,
                width=field_d.width,
                style=field_d.line_style,
            ),
        )

        self.set_time_x_axis(self.g_stock)

    def stockastic_calcul(self, data, k, d):

        data['L14'] = data['Low'].rolling(window=k).min()
        data['H14'] = data['High'].rolling(window=k).max()

        # Create the "%K" column in the DataFrame
        data['%K'] = 100 * ((data['Close'] - data['L14']) / (data['H14'] - data['L14']))
        # Create the "%D" column in the DataFrame
        data['%D'] = data['%K'].rolling(window=d).mean()

        return data

    def set_time_x_axis(self, widget):
        """Set the time on the X axis

        :param widget: The widget on which to add time
        :type widget: Plot
        """
        widget.setAxisItems({"bottom": pg.DateAxisItem(orientation="bottom")})

    def remove_indicator(self, graph_view, *args, **kwargs):
        super(Stochastic, self).remove_indicator(graph_view)
        graph_view.removeItem(self.g_stock)
        self.g_stock = None

