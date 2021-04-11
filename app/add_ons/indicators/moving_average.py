import numpy as np
import pyqtgraph as pg

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
            mva = values[field_input.current].ewm(com=field.value).mean()
            plot = quotation_plot.plot(
                x=[x.timestamp() for x in values.index],
                y=mva,
                connect="finite",
                pen=pg.mkPen(
                    field.color, width=field.width, style=field.line_style
                ),
            )
            self.register_plot(plot=plot)

def rolling_mean(values, length):
    """Find the rolling mean for the given data dans the given length

    :param values: All values to analyse
    :type values: np.array
    :param length: The length to calculate the mean
    :type length: int
    :return: The rolling mean
    :rtype: np.array
    """
    ret = np.cumsum(values, dtype=float)
    ret[length:] = ret[length:] - ret[:-length]
    mva = ret[length - 1 :] / length

    # Padding
    padding = np.array([np.nan for i in range(length)])
    mva = np.append(padding, mva)

    return mva
