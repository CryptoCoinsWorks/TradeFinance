import pyqtgraph as pg
from PySide2 import QtCore, QtWidgets


class TrendLine(pg.LineSegmentROI):
    def __init__(self, pos, removable=True):
        super(TrendLine, self).__init__(pos, removable=removable)


class HorizontalLine(pg.InfiniteLine):
    def __init__(self, pos):
        super(HorizontalLine, self).__init__(pos, angle=0)

class VerticalLine(pg.InfiniteLine):
    def __init__(self, pos):
        super(VerticalLine, self).__init__(pos, angle=90)
