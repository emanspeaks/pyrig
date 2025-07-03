from PySide2.QtWidgets import QGraphicsView, QGraphicsScene

from pyapp.qt_gui.abc import QtWidgetWrapper, QtWindowWrapper

from ...logging import log_func_call


class GraphViewWidget(QtWidgetWrapper):
    @log_func_call
    def __init__(self, parent: QtWindowWrapper):
        super().__init__(parent)
        qtwin = parent.qtroot

        scene = QGraphicsScene()  # qtwin)
        self.scene = scene

        view = QGraphicsView(scene, qtwin)
        self.view = view
        self.qtroot = view
