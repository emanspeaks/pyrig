from PySide2.QtWidgets import QLabel
from PySide2.QtCore import Qt

from pyapp.qt_gui.abc import QtWindowBaseWidgetWrapper, QtWindowWrapper

from ...logging import log_func_call

from .graphview import GraphViewWidget


class WindowBaseQLabel(QtWindowBaseWidgetWrapper):
    @log_func_call
    def __init__(self, parent: QtWindowWrapper, text: str = "", *args,
                 **kwargs):
        super().__init__(parent, *args, **kwargs)
        qtroot = QLabel(text, self.get_window_qtroot())
        self.qtroot = qtroot
        qtroot.setAlignment(Qt.AlignCenter)


class WindowBaseGraphView(QtWindowBaseWidgetWrapper, GraphViewWidget):
    @log_func_call
    def __init__(self, parent: QtWindowWrapper):
        QtWindowBaseWidgetWrapper.__init__(self, parent)
        GraphViewWidget.__init__(self, parent)
