import talib
import numpy as np
import pyqtgraph as pg
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from utils import constants as cst
from utils.indicators_utils import Indicator, InputField, ChoiceField


class RegressionLinear(Indicator):
    def __init__(self):
        super(RegressionLinear, self).__init__()

        self.name = "Linear Regression"
        self.description = "Linear Regression"

        self.g_filler_up = None
        self.g_filler_down = None

        # Define and register all customisable settings
        field_input = ChoiceField(
            "Input", choices=[cst.OPEN, cst.CLOSE, cst.HIGH, cst.LOW], default=cst.CLOSE
        )
        field_base = InputField("Base", color=(255, 255, 255), width=2, disable_line_style=True)
        field_up = InputField("High", color=(38, 166, 154, 50), width=2, disable_line_style=True)
        field_down = InputField("Low", color=(239, 83, 80, 50), width=2, disable_line_style=True)

        self.register_fields(
            field_input,
            field_base,
            field_up,
            field_down,
        )

    def create_indicator(self, graph_view, *args, **kwargs):
        super(RegressionLinear, self).create_indicator(graph_view)

        # Get values
        values = graph_view.values
        quotation_plot = graph_view.g_quotation

        # Retrive settings
        field_input = self.get_field("Input").current
        field_base = self.get_field("Base")
        field_up = self.get_field("High")
        field_down = self.get_field("Low")

        # Calculate
        date, pred = self.regression(date=values.index, value=values[field_input].values)

        plot = quotation_plot.plot(
            x=[x.timestamp() for x in date],
            y=pred,
            pen=pg.mkPen(
                color=field_base.color,
                width=field_base.width,
            ),
        )

        plot_up = quotation_plot.plot(
            x=[x.timestamp() for x in date],
            y=pred + np.std(pred),
            pen=pg.mkPen(
                color=field_up.color,
                width=field_up.width,
            ),
        )
        plot_down = quotation_plot.plot(
            x=[x.timestamp() for x in date],
            y=pred - np.std(pred),
            pen=pg.mkPen(
                color=field_down.color,
                width=field_down.width,
            ),
        )

        self.g_filler_up = pg.FillBetweenItem(
            curve1=plot,
            curve2=plot_up,
            brush=pg.mkBrush(field_up.color),
        )
        quotation_plot.addItem(self.g_filler_up)

        self.g_filler_down = pg.FillBetweenItem(
            curve1=plot,
            curve2=plot_down,
            brush=pg.mkBrush(field_down.color),
        )
        quotation_plot.addItem(self.g_filler_down)

        # Register all plots in order to delete them later
        self.register_plots(plot, plot_up, plot_down)

    def regression(self, date, value):
        """This method calcul the Linear Regression from the data.
        Using MachineLearning, with the LinearRegression Model.
        """
        # Create array from 1 to lenght of DataFrame
        x = np.array([x for x in range(len(value))]).reshape((-1, 1))
        y = value.reshape((-1, 1))
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)
        regressor = LinearRegression().fit(x_train, y_train)
        y_pred = regressor.predict(x_test)

        # Sorted from x array
        result_list = list(zip([x[0] for x in x_test], [x[0] for x in y_pred]))
        result_list = sorted(result_list, key=lambda x: x[0])

        price = list()
        dates = list()
        for x in result_list:
            dates.append(date[x[0]])
            price.append(x[1])

        return dates, price

    def remove_indicator(self, graph_view, *args, **kwargs):
        super(RegressionLinear, self).remove_indicator(graph_view)
        self.g_filler_up.setBrush(None)
        self.g_filler_down.setBrush(None)
        self.g_filler_up = None
        self.g_filler_down = None
