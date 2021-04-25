import pyqtgraph as pg
from PySide2 import QtCore, QtWidgets


class Measure(object):
    def __init__(self, parent=None):
        super(Measure, self).__init__()
        self.name = "Measure"
        self.description = "This Mesure give you % from a starting point to an end point."

        self.legend = None
        self.rbScaleBox = None

    def run(self, graph=None, p1=None, p2=None):
        self.quotation_plot = graph
        try:
            self.quotation_plot.removeItem(self.rbScaleBox)
            self.quotation_plot.removeItem(self.legend)
        except:
            pass

        if p1:
            percent = ((p2.toTuple()[1] - p1.toTuple()[1]) / p1.toTuple()[1]) * 100
            width = p1.toTuple()[0] - p2.toTuple()[0]
            height = p1.toTuple()[1] - p2.toTuple()[1]

            negativ = False
            color_pen = (25, 118, 210)
            color_brush = 33, 150, 243, 100

            if p2.toTuple()[1] < p1.toTuple()[1]:
                negativ = True
                color_pen = (210, 46, 25)
                color_brush = 243, 58, 33, 100

            self.rbScaleBox = QtWidgets.QGraphicsRectItem(p2.toTuple()[0],
                                                          p2.toTuple()[1],
                                                          width,
                                                          height
                                                          )
            self.rbScaleBox.setPen(pg.mkPen(color_pen, width=1))
            self.rbScaleBox.setBrush(pg.mkBrush(color_brush))
            self.rbScaleBox.setZValue(1e9)
            center_legend = p1.toTuple()[0] + ((p2.toTuple()[0] - p1.toTuple()[0]) / 2)

            self.legend = self._set_legend(x=center_legend,
                                           y=p2.toTuple()[1],
                                           percentage=round(percent, 2),
                                           price=round(p2.toTuple()[1], 2),
                                           negativ=negativ)

            self.quotation_plot.addItem(self.rbScaleBox)
            self.quotation_plot.addItem(self.legend)

    def _set_legend(self, x, y, percentage="", price='', negativ=False):
        legend_text = '{} ({}%) \n'.format(price, percentage)

        anchoring = (0, 1)
        if negativ:
            anchoring = (0, -0.5)

        label = pg.TextItem(text=legend_text,
                            anchor=anchoring,
                            )
        label.setPos(x, y)
        return label

    def remove(self):
        try:
            self.quotation_plot.removeItem(self.rbScaleBox)
            self.quotation_plot.removeItem(self.legend)
        except:
            raise ValueError
