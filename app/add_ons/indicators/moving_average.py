import numpy as np
import pyqtgraph as pg
from PySide2 import QtGui, QtCore, QtWidgets

from utils import constants as cst
from utils.indicators_utils import Indicator, InputField, ChoiceField


class MovingAverage(Indicator):
    def __init__(self):
        super(MovingAverage, self).__init__()

        self.name = "Moving Average"
        self.description = "Moving Average"

        # Define and register all customisable settings
        field_input = ChoiceField(
            "Input", choices=[cst.OPEN, cst.CLOSE, cst.HIGH, cst.LOW], default=cst.CLOSE
        )
        self.register_field(field_input)
        line1 = InputField(
            "Trader MMA 1", color=(51, 153, 255), value=3, width=2
        )
        self.register_fields(line1)

    def create_indicator(self, graph_view, *args, **kwargs):
        super(MovingAverage, self).create_indicator(self, graph_view)

        # Get values
        values = graph_view.values
        quotation_plot = graph_view.g_quotation

        # Get field
        field_input = self.get_field("Input")

        for field in self.fields:
            if not isinstance(field, InputField):
                # Escape ChoiceFields
                continue
            mva = values[field_input.current].rolling(com=field.value).mean()
            plot = quotation_plot.plot(
                x=[x.timestamp() for x in values.index],
                y=mva,
                connect="finite",
                pen=pg.mkPen(
                    field.color, width=field.width, style=field.line_style
                ),
            )
            self.register_plot(plot=plot)


class ExpoMovingAverage(Indicator):
    def __init__(self):
        super(ExpoMovingAverage, self).__init__()

        self.name = "Exponential Moving Average"
        self.description = "Exponential Moving Average"

        # Define and register all customisable settings
        field_input = ChoiceField(
            "Input", choices=[cst.OPEN, cst.CLOSE, cst.HIGH, cst.LOW], default=cst.CLOSE
        )
        self.register_field(field_input)

        line1 = InputField(
            "Trader MMA 1", color=(51, 153, 255), value=3, width=2
        )
        self.register_fields(line1)


    def create_indicator(self, graph_view, *args, **kwargs):
        super(ExpoMovingAverage, self).create_indicator(self, graph_view)

        # Get values
        values = graph_view.values
        quotation_plot = graph_view.g_quotation

        # Get field
        field_input = self.get_field("Input")

        for field in self.fields:
            if not isinstance(field, InputField):
                # Escape ChoiceFields
                continue
            mva = values[field_input.current].ewm(window=field.value).mean()
            plot = quotation_plot.plot(
                x=[x.timestamp() for x in values.index],
                y=mva,
                connect="finite",
                pen=pg.mkPen(
                    field.color, width=field.width, style=field.line_style
                ),
            )
            self.register_plot(plot=plot)