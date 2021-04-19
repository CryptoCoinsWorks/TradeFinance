import numpy as np
import pyqtgraph as pg

from utils import constants as cst
from utils.indicators_utils import Indicator, InputField, ChoiceField


class Expo_MMA(Indicator):
    def __init__(self):
        super(Expo_MMA, self).__init__()

        self.name = "Expo Moving Average (3, 5, 8, 10, 12, 15)"
        self.description = "Expo Multiple Moving Average (MMA)"

        # Define and register all customisable settings
        field_input = ChoiceField(
            "Input", choices=[cst.OPEN, cst.CLOSE, cst.HIGH, cst.LOW], default=cst.CLOSE
        )
        self.register_field(field_input)
        line1 = InputField(
            "Trader MMA 1", color=(51, 153, 255), value=3, width=2
        )
        line2 = InputField(
            "Trader MMA 2", color=(0, 138, 230), value=5, width=1.8
        )
        line3 = InputField(
            "Trader MMA 3", color=(0, 138, 230), value=8, width=1.6
        )
        line4 = InputField(
            "Trader MMA 4", color=(0, 138, 230), value=10, width=1.4
        )
        line5 = InputField(
            "Trader MMA 5", color=(0, 138, 230), value=12, width=1.2
        )
        line6 = InputField(
            "Trader MMA 6", color=(0, 138, 230), value=15, width=1
        )
        self.register_fields(line1, line2, line3, line4, line5, line6)

    def create_indicator(self, graph_view, *args, **kwargs):
        super(Expo_MMA, self).create_indicator(self, graph_view)

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


class MMA(Indicator):
    def __init__(self):
        super(MMA, self).__init__()

        self.name = "Moving Average (3, 5, 8, 10, 12, 15)"
        self.description = "Moving Average (3, 5, 8, 10, 12, 15)"

        # Define and register all customisable settings
        field_input = ChoiceField(
            "Input", choices=[cst.OPEN, cst.CLOSE, cst.HIGH, cst.LOW], default=cst.CLOSE
        )
        self.register_field(field_input)
        line1 = InputField(
            "Trader EMA 1", color=(51, 153, 255), value=3, width=2
        )
        line2 = InputField(
            "Trader EMA 2", color=(0, 138, 230), value=5, width=1.8
        )
        line3 = InputField(
            "Trader EMA 3", color=(0, 138, 230), value=8, width=1.6
        )
        line4 = InputField(
            "Trader EMA 4", color=(0, 138, 230), value=10, width=1.4
        )
        line5 = InputField(
            "Trader EMA 5", color=(0, 138, 230), value=12, width=1.2
        )
        line6 = InputField(
            "Trader EMA 6", color=(0, 138, 230), value=15, width=1
        )
        self.register_fields(line1, line2, line3, line4, line5, line6)

        line7 = InputField(
            "Investor EMA 1", color=(179, 36, 0), value=30, width=2
        )
        line8 = InputField(
            "Investor EMA 2", color=(179, 36, 0), value=35, width=1.8
        )
        line9 = InputField(
            "Investor EMA 3", color=(255, 0, 0), value=40, width=1.6
        )
        line10 = InputField(
            "Investor EMA 4", color=(255, 0, 0), value=45, width=1.4
        )
        line11 = InputField(
            "Investor EMA 5", color=(255, 0, 0), value=50, width=1.2
        )
        line12 = InputField(
            "Investor EMA 6", color=(255, 255, 255), value=60, width=1
        )
        self.register_fields(line7, line8, line9, line10, line11, line12)

    def create_indicator(self, graph_view, *args, **kwargs):
        super(MMA, self).create_indicator(self, graph_view)

        # Get values
        values = graph_view.values
        quotation_plot = graph_view.g_quotation

        # Get field
        field_input = self.get_field("Input")

        for field in self.fields:
            if not isinstance(field, InputField):
                # Escape ChoiceFields
                continue
            # TODO need pass this to EMA instead of MMA
            mva = values[field_input.current].rolling(window=field.value).mean()
            plot = quotation_plot.plot(
                x=[x.timestamp() for x in values.index],
                y=mva,
                connect="finite",
                pen=pg.mkPen(
                    field.color, width=field.width, style=field.line_style
                ),
            )
            self.register_plot(plot=plot)
