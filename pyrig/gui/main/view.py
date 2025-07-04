from typing import TYPE_CHECKING

from PySide2.QtWidgets import QToolBar, QStatusBar, QLabel
from PySide2.QtCore import Qt

from pyapp.qt_gui.abc import STATUS_LABEL, QtWindowWrapper
from pyapp.qt_gui.utils import create_action, create_toolbar_expanding_spacer
from pyapp.qt_gui.icons.thirdparty.codicons import Codicons
from pyapp.qt_gui.icons.thirdparty.codicons import names as codicon_names

from ...app import PyRigApp
from ...logging import log_func_call
from ..widgets.baseframe import BaseView
if TYPE_CHECKING:
    from .ctrl import MainWindow


class MainWindowView(QtWindowWrapper):
    @log_func_call
    def __init__(self, controller: 'MainWindow'):
        super().__init__("PyRig", controller)
        self.basewidget: BaseView
        self.controller: MainWindow
        self.get_window_qtroot().resize(*PyRigApp.get_default_win_size())

        self.create_toolbar()
        self.create_statusbar()
        self.create_chips()

    @log_func_call
    def create_toolbar(self):
        qtwin = self.qtroot
        ctrl = self.controller

        toolbar = QToolBar("Main Toolbar", qtwin)
        qtwin.addToolBar(Qt.TopToolBarArea, toolbar)
        self.toolbar = toolbar

        toolbar.addAction(create_action(qtwin, "New",
                                        Codicons.icon(codicon_names.new_file),
                                        ctrl.click_new))
        toolbar.addAction(create_action(qtwin, "Open",
                                        Codicons.icon(codicon_names.folder_opened),  # noqa: E501
                                        ctrl.click_open))
        toolbar.addAction(create_action(qtwin, "Save",
                                        Codicons.icon(codicon_names.save),
                                        ctrl.click_save))
        toolbar.addAction(create_action(qtwin, "Save As",
                                        Codicons.icon(codicon_names.save_as),
                                        ctrl.click_saveas))
        toolbar.addWidget(create_toolbar_expanding_spacer())
        toolbar.addAction(create_action(qtwin, "Config",
                                        Codicons.icon(codicon_names.json),
                                        ctrl.click_config))

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
        return BaseView(self)

    @log_func_call
    def create_chips(self):
        from PySide2.QtGui import QImage, QColor
        from .chip import Chip

        scene = self.basewidget.viewwidget.scene
        chipdir = PyRigApp.get_assets_dir()
        image = QImage((chipdir/'SMPTE_Color_Bars.png').as_posix())
        xx = 0
        nitems = 0
        for i in range(-11000, 11000, 110):
            xx += 1
            yy = 0
            for j in range(-7000, 7000, 70):
                yy += 1
                x = (i + 11000)/22000
                y = (j + 7000)/14000
                color = QColor(image.pixel(int(image.width()*x),
                                           int(image.height()*y)))
                item = Chip(color, xx, yy)
                item.setPos(i, j)
                scene.addItem(item)
                nitems += 1
