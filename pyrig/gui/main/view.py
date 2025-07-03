from typing import TYPE_CHECKING

from PySide2.QtWidgets import (
    QToolBar, QAction, QStatusBar, QLabel, QWidget, QSizePolicy,
)
from PySide2.QtCore import Qt

from pyapp.qt_gui.abc import STATUS_LABEL, QtWindowWrapper
from pyapp.qt_gui.widgets.windowbase import WindowBaseGraphView

from ...app import PyRigApp
from ...logging import log_func_call
if TYPE_CHECKING:
    from .ctrl import MainWindow


class MainWindowView(QtWindowWrapper):
    @log_func_call
    def __init__(self, controller: 'MainWindow'):
        super().__init__("PyRig", controller)
        self.basewidget: WindowBaseGraphView
        self.controller: MainWindow
        self.get_window_qtroot().resize(*PyRigApp.get_default_win_size())

        self.create_toolbar()
        self.create_statusbar()

    @log_func_call
    def create_toolbar(self):
        qtwin = self.qtroot
        ctrl = self.controller

        toolbar = QToolBar("Main Toolbar", qtwin)
        # toolbar.setMovable(False)
        qtwin.addToolBar(Qt.TopToolBarArea, toolbar)
        self.toolbar = toolbar

        act_new = QAction("New", qtwin)
        act_new.triggered.connect(ctrl.click_new)
        toolbar.addAction(act_new)

        act_open = QAction("Open", qtwin)
        act_open.triggered.connect(ctrl.click_open)
        toolbar.addAction(act_open)

        act_save = QAction("Save", qtwin)
        act_save.triggered.connect(ctrl.click_save)
        toolbar.addAction(act_save)

        act_saveas = QAction("Save As", qtwin)
        act_saveas.triggered.connect(ctrl.click_saveas)
        toolbar.addAction(act_saveas)

        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        # Add Config action
        act_config = QAction("Config", qtwin)
        act_config.triggered.connect(ctrl.click_config)
        toolbar.addAction(act_config)

    @log_func_call
    def create_statusbar(self):
        qtwin = self.qtroot
        ctrl = self.controller

        statusbar = QStatusBar(qtwin)
        qtwin.setStatusBar(statusbar)

        avcad_dbdir_label = QLabel(statusbar)
        avcad_dbdir_label.setCursor(Qt.PointingHandCursor)
        avcad_dbdir_label.mousePressEvent = ctrl.click_avcad_dbdir
        avcad_dbdir_label.setObjectName(STATUS_LABEL)
        statusbar.addPermanentWidget(avcad_dbdir_label)
        self.status_dbdir = avcad_dbdir_label

        ctrl.update_avcad_dbdir_label(self)

    @log_func_call
    def create_basewidget(self):
        return WindowBaseGraphView(self)
        # return WindowBaseQLabel(self, "Welcome to PyRig!")
