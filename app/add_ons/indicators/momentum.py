import numpy as np
import pyqtgraph as pg

from utils import utils
from utils import constants as cst
from libs.graph.bargraph import BarGraphItem
from utils.indicators_utils import Indicator, InputField, ChoiceField

from PySide2 import QtCore, QtGui


class Momentum(Indicator):
    def __init__(self):
        super(Momentum, self).__init__()

        self.name = "Momentum"
        self.description = "Momentum is use to spot trend reversals."

        self.g_moment = None

        # Define and register all customisable settings
        field_input = InputField("Momentum", value=11, color=(255, 106, 0), width=2)
        self.register_fields(
            field_input,
        )

    def create_indicator(self, graph_view, *args, **kwargs):
        super(Momentum, self).create_indicator(self, graph_view)

        # Get values
        values = graph_view.values
        self.quotation_plot = graph_view.g_quotation

        # Init plot
        self.g_moment = graph_view.addPlot(
            row=2, col=0, width=1, title="<b>{name}</b>".format(name=self.name)
        )
        self.g_moment.setMaximumHeight(150)
        self.g_moment.showGrid(x=True, y=True, alpha=0.3)
        self.g_moment.setXLink("Quotation")

        # Retrive settings
        field_input = self.get_field("Momentum")

        data = self.moment_calcul(data=values, offset=field_input.value)

        # Calculations
        # Skip the 11 first days
        self.g_moment.plot(
            x=[x.timestamp() for x in values[field_input.value:].index],
            y=data['Momentum'][field_input.value:],
            pen=pg.mkPen(
                field_input.color,
                width=field_input.width,
                style=field_input.line_style,
            ),
        )
        self.set_time_x_axis(self.g_moment)

    def moment_calcul(self, data, offset):
        momentum = list()
        for i in np.arange(len(data)):
            if i < offset:
                momentum.append(0)
                continue
            momentum.append((data['Close'][i] / data['Close'][i - offset]) * 100)

        data['Momentum'] = np.array(momentum)
        return data

    def set_time_x_axis(self, widget):
        """Set the time on the X axis

        :param widget: The widget on which to add time
        :type widget: Plot
        """
        widget.setAxisItems({"bottom": pg.DateAxisItem(orientation="bottom")})

    def remove_indicator(self, graph_view, *args, **kwargs):
        super(Momentum, self).remove_indicator(graph_view)
        graph_view.removeItem(self.g_moment)
        self.g_moment = None

