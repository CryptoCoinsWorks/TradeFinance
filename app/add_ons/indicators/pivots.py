import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import pyqtgraph as pg

from utils import utils
from utils import constants as cst
from utils.indicators_utils import Indicator, InputField, ChoiceField

from PySide2 import QtCore, QtGui


class PivotsPoint(Indicator):
    def __init__(self):
        super(PivotsPoint, self).__init__()

        self.name = "Pivots Point"
        self.description = "A pivot point is used to determine the overall trend of the market over different time " \
                           "frames. The pivot point itself is simply the average of the intraday high and low, " \
                           "and the closing price from the previous trading day. "

        self.all_lines = list()
        self.quotation_plot = None

        # Define and register all customisable settings
        field_R3 = InputField("R3", color=(0, 106, 255), width=2)
        field_R2 = InputField("R2", color=(0, 106, 255), width=2)
        field_R1 = InputField("R1", color=(0, 106, 255), width=2)
        field_PP = InputField("PP", color=(0, 255, 0), width=2)
        field_S1 = InputField("S1", color=(255, 0, 0), width=2)
        field_S2 = InputField("S2", color=(255, 0, 0), width=2)
        field_S3 = InputField("S3", color=(255, 0, 0), width=2)
        self.register_fields(
            field_R3,
            field_R2,
            field_R1,
            field_PP,
            field_S1,
            field_S2,
            field_S3,
        )

    def create_indicator(self, graph_view, *args, **kwargs):
        super(PivotsPoint, self).create_indicator(self, graph_view)

        # Get values
        values = graph_view.values
        ticker = graph_view.ticker
        self.quotation_plot = graph_view.g_quotation

        # Get Monthly Data
        ticker = yf.Ticker(ticker)
        data = ticker.history(period=cst.PERIODE,
                              interval=cst.INTERVAL_MONTH,
                              start=cst.START_DATE)

        # Calculations
        data = self.pp_sr(all_data=values, data=data)[30:]

        for col in ['PP', 'R1', 'R2', 'R3', 'S1', 'S2', 'S3']:
            # Retrive settings
            field_input = self.get_field(col)
            line = self.quotation_plot.plot(
                x=[x.timestamp() for x in data.index],
                y=data[col],
                pen=pg.mkPen(
                    field_input.color,
                    width=field_input.width,
                    style=field_input.line_style,
                )
            )
            self.all_lines.append(line)

    def pp_sr(self, all_data, data):
        PP = pd.Series((data['High'] + data['Low'] + data['Close']) / 3)
        R1 = pd.Series(2 * PP - data['Low'])
        S1 = pd.Series(2 * PP - data['High'])
        R2 = pd.Series(PP + data['High'] - data['Low'])
        S2 = pd.Series(PP - data['High'] + data['Low'])
        R3 = pd.Series(data['High'] + 2 * (PP - data['Low']))
        S3 = pd.Series(data['Low'] - 2 * (data['High'] - PP))
        psr = {'PP': PP, 'R1': R1, 'S1': S1, 'R2': R2,
               'S2': S2, 'R3': R3, 'S3': S3}
        PSR = pd.DataFrame(psr)

        df = pd.concat([all_data, PSR], axis=1)

        for column, i in df.items():
            value = 0
            for index, i in enumerate(df[column]):
                if str(i) == "nan":
                    df[column][index] = value
                else:
                    value = i

        return self.append_days_offset(df)

    def append_days_offset(self, df):
        """This Method add 1 month with last value for
           Supports & Resistances PP.
        """
        days = list()
        start_date = df.index[-1]
        end_day = start_date + datetime.timedelta(days=30)
        test = {'PP': [], 'R1': [], 'S1': [], 'R2': [], 'S2': [], 'R3': [], 'S3': []}
        for n in range(int((end_day - start_date).days)):
            day = start_date + datetime.timedelta(n + 1)
            test['PP'].append(df['PP'].iloc[-1])
            test['R1'].append(df['R1'].iloc[-1])
            test['S1'].append(df['S1'].iloc[-1])
            test['R2'].append(df['R2'].iloc[-1])
            test['S2'].append(df['S2'].iloc[-1])
            test['R3'].append(df['R3'].iloc[-1])
            test['S3'].append(df['S3'].iloc[-1])
            days.append(day)

        last_df = pd.DataFrame(test)
        last_df.index = pd.DatetimeIndex(days)

        df = df.append(last_df)

        return df

    def remove_indicator(self, graph_view, *args, **kwargs):
        super(PivotsPoint, self).remove_indicator(graph_view)
        for line in self.all_lines:
            self.quotation_plot.removeItem(line)
