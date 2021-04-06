import time
import pyqtgraph as pg
from PySide2 import QtCore, QtWidgets
from add_ons.charts import fibonnaci

class ROIManager(QtCore.QObject):
    def __init__(self, parent=None):
        super(ROIManager, self).__init__(parent)

        # Constants
        self.current_tool = None
        self.current_handle = None
        self.current_graph = None
        self._graph = self.parent().wgt_graph.graph

        # Signals
        self.parent().wgt_graph.signals.sig_graph_clicked.connect(
            self._on_roi_add_requested
        )
        self.parent().wgt_graph.signals.sig_graph_mouse_moved.connect(self._on_mouse_moved)
        # self.parent().wgt_graph.signals.sig_graph_mouse_pressed.connect(self._on_mouse_pressed)
        # self.parent().wgt_graph.signals.sig_graph_mouse_released.connect(self._on_mouse_released)

    def drawer(self, graph, event):
        """Drawer over the graph

        :param graph: The graph on whch to draw
        :type graph: pg.PlotItem
        :param event: The event
        :type event: object
        """
        self.current_graph = graph
        vb = graph.vb
        mouse_point = vb.mapSceneToView(event.pos())
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
    def _on_mouse_moved(self, event):
        if self.current_handle:
            vb = self.current_graph.vb
            mousePoint = vb.mapSceneToView(event.pos())
            self.current_handle.setPos(mousePoint)

    @QtCore.Slot(object)
    def _on_mouse_released(self, event):
        print("Released", event)

    @QtCore.Slot(object)
    def _on_mouse_pressed(self, event):
        print("Pressed", event)

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
        roi = pg.LineSegmentROI((initial_pos, initial_pos), removable=True)
        self.current_handle = roi.getHandles()[-1]
        self.current_graph.addItem(roi)
        roi.sigRemoveRequested.connect(self._on_roi_remove_requested)

    def fibonnaci(self, initial_pos, **kwargs):
        self.fibo = fibonnaci.Fibonnaci(self)
        self.fibo_item = self.fibo.run(graph=self.current_graph, position=initial_pos)
        self.fibo_item.sigRegionChanged.connect(self.fibo.move_items)
        self.fibo_item.sigRemoveRequested.connect(self._on_roi_remove_requested)
