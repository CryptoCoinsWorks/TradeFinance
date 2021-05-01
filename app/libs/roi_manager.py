import time
import pyqtgraph as pg
from libs.widgets.roi_lines import TrendLine, HorizontalLine, VerticalLine
from PySide2 import QtCore, QtWidgets
from add_ons.charts import fibonnaci
from add_ons.charts import measure as ms

#TODO
# - RightClick : Cancel Drawing in graph


class ROIManager(QtCore.QObject):
    def __init__(self, parent=None):
        super(ROIManager, self).__init__(parent)

        # Constants
        self.current_tool = None
        self.current_handle = None
        self.current_graph = None
        self.measure_widget = False
        self.release = False
        self.position_origin = None
        self._graph = self.parent().wgt_graph.graph

        # Signals
        self.parent().wgt_graph.signals.sig_graph_clicked.connect(
            self._on_roi_add_requested
        )
        self.parent().wgt_graph.signals.sig_graph_mouse_moved.connect(self._on_mouse_moved)
        self.parent().wgt_graph.signals.sig_graph_mouse_pressed.connect(self._on_mouse_pressed)
        self.parent().wgt_graph.signals.sig_graph_mouse_released.connect(self._on_mouse_released)

    def drawer(self, graph, event):
        """Drawer over the graph

        :param graph: The graph on whch to draw
        :type graph: pg.PlotItem
        :param event: The event
        :type event: object
        """
        self.current_graph = graph
        self.vb = graph.vb
        mouse_point = self.vb.mapSceneToView(event.pos())
        if self.current_tool:
            self.current_tool(initial_pos=mouse_point)  # Exec the current tool

    def set_tool(self, **kwargs):
        """Set the current tool. kwargs may have a tool which corresponds to
        the method to call inside this module.

        :return: The current tool
        :rtype: method if found, None instead
        """
        self.current_tool = getattr(self, kwargs.get("tool", None), None)
        return self.current_tool

    def unset_tool(self):
        """Unset the current tool"""
        self.current_tool = None
        self.current_handle = None
        self.current_graph = None

    def remove_roi(self, roi):
        """Remove the given roi

        :param roi: The roi to remove
        :type roi: pg.ROI
        """
        print(roi)

    @QtCore.Slot(object)
    def _on_mouse_pressed(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.unset_tool()
        if self.measure_widget:
            if self.release:
                self.release = False
                self.position_origin = None
                self.measure_widget = False
                self.measu.remove()
                self.unset_tool()

    @QtCore.Slot(object)
    def _on_mouse_released(self, event):
        # self.save_item()
        # self.restore_items()
        # print("Released", event)
        pass

    @QtCore.Slot(object)
    def _on_mouse_moved(self, event):
        if self.current_handle:
            mousePoint = self.vb.mapSceneToView(event.pos())
            self.current_handle.setPos(mousePoint)
        if self.measure_widget:
            pos = self.vb.mapSceneToView(event.pos())
            self.measu.run(graph=self.current_graph, p1=self.position_origin, p2=pos)

    @QtCore.Slot(list, object)
    def _on_roi_add_requested(self, objects, event):
        """Called on a draw requested"""
        if not self.current_handle:
            if objects:
                self.drawer(graph=objects[0], event=event)
        else:
            self.unset_tool()

    @QtCore.Slot(object)
    def _on_roi_remove_requested(self, roi):
        """Called on a request for ROI deletion

        :param roi: The roi to remove
        :type roi: pg.ROI
        """
        self.remove_roi(roi=roi)

    def bounded_line_drawer(self, initial_pos, **kwargs):
        """Draw a bounded line
        """
        # roi = pg.LineSegmentROI((initial_pos, initial_pos), removable=True)
        roi = TrendLine((initial_pos, initial_pos))
        self.current_handle = roi.getHandles()[-1]
        self.current_graph.addItem(roi)
        roi.sigRemoveRequested.connect(self._on_roi_remove_requested)

    def horizontal_line(self, initial_pos, **kwargs):
        h_line = HorizontalLine(initial_pos.x())
        self.current_graph.addItem(h_line)

    def vertical_line(self, initial_pos, **kwargs):
        h_line = VerticalLine(initial_pos.x())
        self.current_graph.addItem(h_line)

    def fibonnaci(self, initial_pos, **kwargs):
        size = None
        if kwargs.get('size'):
            size = kwargs.get('size')
        if kwargs.get('current_graph'):
            self.current_graph = kwargs.get('current_graph')
        self.fibo = fibonnaci.Fibonnaci(self)
        self.fibo_item = self.fibo.run(graph=self.current_graph, position=initial_pos, size=size)
        self.fibo_item.sigRegionChanged.connect(self.fibo.move_items)
        self.fibo_item.sigRemoveRequested.connect(self._on_roi_remove_requested)
        self.unset_tool()

    def measure_fct(self, initial_pos, **kwargs):
        self.measure_widget = True
        self.release = True
        self.measu = ms.Measure(self)
        self.position_origin = initial_pos

    def restore_items(self, path, graph):
        for item in path:
            for widget, state in item.items():
                if widget == "LineSegmentROI":
                    roi = pg.LineSegmentROI((0, 0), removable=True)
                    roi.setState(state)
                    self.current_graph.addItem(roi)
                if widget == "FibonnaciROI":
                    position = QtCore.QPointF(state['pos'][0], state['pos'][1])
                    self.fibonnaci(initial_pos=position, size=state['size'], current_graph=graph)
                if widget == "VerticalLine":
                    position = state['pos']
                    v_line = VerticalLine(pos=position)
                    self.current_graph.addItem(v_line)
                if widget == "HorizontalLine":
                    position = state['pos']
                    h_line = HorizontalLine(pos=position)
                    self.current_graph.addItem(h_line)
