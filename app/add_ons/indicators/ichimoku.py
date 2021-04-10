import numpy as np
import pyqtgraph as pg
from pprint import pprint
from PySide2 import QtCore, QtGui, QtWidgets

from utils import constants as cst
from utils.indicators_utils import Indicator, InputField, ChoiceField

class Ichimoku(Indicator):
    def __init__(self):
        super(Ichimoku, self).__init__()

        self.name = "Ichimuku"
        self.description = "Ichimuku"

        line_tenkan = InputField(
            "Tenkan", color=(55, 55, 55), width=2, disable_line_style=True
        )
        line_kijun = InputField(
            "Kijun", color=(218, 218, 42), width=2, disable_line_style=True
        )
        line_span_a = InputField(
            "Senkou Span A", color=(218, 81, 42), width=1, disable_line_style=True
        )
        line_span_b = InputField(
            "Senkou Span B", color=(130, 218, 42), width=1, disable_line_style=True
        )
        line_chikou = InputField(
            "Chikou Span", color=(48, 218, 42), width=2, disable_line_style=True
        )
        cloud = InputField(
            "Cloud", color=(131, 29, 29, 50)
        )
        self.register_fields(
            line_tenkan,
            line_kijun,
            line_span_a,
            line_span_b,
            line_chikou,
            cloud
        )
        self.g_filler = None

    def create_indicator(self, graph_view, *args, **kwargs):
        super(Ichimoku, self).create_indicator(self, graph_view)

        # Get values
        self.values = graph_view.values
        self.quotation_plot = graph_view.g_quotation

        field_tenkan = self.get_field("Tenkan")
        field_kijun = self.get_field("Kijun")
        field_span_a = self.get_field("Senkou Span A")
        field_span_b = self.get_field("Senkou Span B")
        field_chikou = self.get_field("Chikou Span")
        field_cloud = self.get_field("Cloud")

        self.get_ichimoku()

        tenkan = self.quotation_plot.plot(
            x=[x.timestamp() for x in self.values.index],
            y=self.values['Tenkan'],
            pen=pg.mkPen(
                field_tenkan.color,
                width=field_tenkan.width,
                style=QtCore.Qt.SolidLine,
                ),
            )
        kijun = self.quotation_plot.plot(
            x=[x.timestamp() for x in self.values.index],
            y=self.values['Kijun'],
            pen=pg.mkPen(
                field_kijun.color,
                width=field_kijun.width,
                style=QtCore.Qt.SolidLine,
            ),
        )
        senlou_span_a = self.quotation_plot.plot(
            x=[x.timestamp() for x in self.values.index],
            y=self.values['SpanA'],
            pen=pg.mkPen(
                field_span_a.color,
                width=field_span_a.width,
                style=QtCore.Qt.SolidLine,
            ),
        )
        senlou_span_b = self.quotation_plot.plot(
            x=[x.timestamp() for x in self.values.index],
            y=self.values['SpanB'],
            pen=pg.mkPen(
                field_span_b.color,
                width=field_span_b.width,
                style=QtCore.Qt.SolidLine,
            ),
        )
        chikou_span = self.quotation_plot.plot(
            x=[x.timestamp() for x in self.values.index],
            y=self.values['Chikou'],
            pen=pg.mkPen(
                field_chikou.color,
                width=field_chikou.width,
                style=QtCore.Qt.SolidLine,
            ),
        )

        self.g_filler = pg.FillBetweenItem(
            curve1=senlou_span_a,
            curve2=senlou_span_b,
            brush=pg.mkBrush(field_cloud.color),
        )

        self. quotation_plot.addItem(self.g_filler)

        # Register all plots in order to delete them later
        self.register_plots(tenkan,
                            kijun,
                            senlou_span_a,
                            senlou_span_b,
                            chikou_span
                            )


    def tenkan(self):
        nine_high = self.values[cst.HIGH].rolling(window=9).max()
        nine_low = self.values[cst.LOW].rolling(window=9).min()
        self.values['Tenkan'] = (nine_high + nine_low) / 2

    def kijun(self):
        twenty_six_high = self.values[cst.HIGH].rolling(window=26).max()
        twenty_six_low = self.values[cst.LOW].rolling(window=26).min()
        self.values['Kijun'] = (twenty_six_high + twenty_six_low) / 2

    def senlou_span_a(self):
        self. values['SpanA'] = ((self.values['Tenkan'] + self.values['Kijun']) / 2).shift(26)

    def senlou_span_b(self):
        fifty_high = self.values[cst.HIGH].rolling(window=52).max()
        fifty_low = self.values[cst.LOW].rolling(window=52).min()
        self.values['SpanB'] = ((fifty_high + fifty_low) / 2).shift(26)

    def chikou_span(self):
        self.values['Chikou'] = self.values[cst.CLOSE].shift(-26)

    def get_ichimoku(self):
        self.tenkan()
        self.kijun()
        self.senlou_span_a()
        self.senlou_span_b()
        self.chikou_span()


    def move_items(self):
        """This method is call everytime the ROI is move.
        """
        pass

    def remove_indicator(self, graph_view, *args, **kwargs):
        super(Ichimoku, self).remove_indicator(graph_view)
        # graph_view.removeItem(self.tenkan)
        # graph_view.removeItem(self.kijun)
        # graph_view.removeItem(self.senlou_span_a)
        # graph_view.removeItem(self.senlou_span_b)
        # graph_view.removeItem(self.chikou_span)
        self.g_filler.setBrush(None)