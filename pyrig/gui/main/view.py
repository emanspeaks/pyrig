from typing import TYPE_CHECKING

from PySide2.QtWidgets import QToolBar, QStatusBar, QLabel
from PySide2.QtCore import Qt

from pyapp.gui.window import GuiWindowView
from pyapp.gui.loadstatus import (
    load_status_step, loading_step_context, register_load_step,
    register_as_load_step,
)
from pyapp.gui.utils import create_action, create_toolbar_expanding_spacer
from pyapp.gui.styles import STATUS_LABEL

from ...app import PyRigApp
from ...logging import log_func_call
from ...constants import (
    CHIP_I_MAX, CHIP_I_MIN, CHIP_I_STEP, CHIP_J_MAX, CHIP_J_MIN, CHIP_J_STEP,
)
from ..widgets.baseframe import BaseView
from ..icons import NewIcon, OpenIcon, SaveIcon, SaveAsIcon, ConfigIcon
if TYPE_CHECKING:
    from .pres import MainWindow


class MainWindowView(GuiWindowView['MainWindow', BaseView]):
    @staticmethod
    @log_func_call
    def register_chip_load_steps():
        n = 0
        for i in range(CHIP_I_MIN, CHIP_I_MAX, CHIP_I_STEP):
            for j in range(CHIP_J_MIN, CHIP_J_MAX, CHIP_J_STEP):
                n += 1
                register_load_step(f"Creating chip {n}")

    @log_func_call
    def __init__(self, basetitle: str, presenter: 'MainWindow' = None):
        super().__init__(basetitle, presenter)
        self.qtobj.resize(*PyRigApp.get_default_win_size())

        self.create_toolbar()
        self.create_statusbar()
        self.create_chips()

    @load_status_step("Creating toolbar")
    @log_func_call
    def create_toolbar(self):
        qtwin = self.qtobj
        ctrl = self.gui_pres

        toolbar = QToolBar("Main Toolbar", qtwin)
        qtwin.addToolBar(Qt.TopToolBarArea, toolbar)
        self.toolbar = toolbar

        toolbar.addAction(create_action(qtwin, "New", NewIcon.icon(),
                                        ctrl.click_new))
        toolbar.addAction(create_action(qtwin, "Open", OpenIcon.icon(),
                                        ctrl.click_open))
        toolbar.addAction(create_action(qtwin, "Save", SaveIcon.icon(),
                                        ctrl.click_save))
        toolbar.addAction(create_action(qtwin, "Save As", SaveAsIcon.icon(),
                                        ctrl.click_saveas))
        toolbar.addWidget(create_toolbar_expanding_spacer())
        toolbar.addAction(create_action(qtwin, "Config", ConfigIcon.icon(),
                                        ctrl.click_config))

    @load_status_step("Creating status bar and loading AVCAD databases")
    @log_func_call
    def create_statusbar(self):
        qtwin = self.qtobj
        ctrl = self.gui_pres

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

    @register_as_load_step(register_chip_load_steps)
    @log_func_call
    def create_chips(self):
        from PySide2.QtGui import QImage, QColor
        from .chip import Chip

        scene = self.basewidget.viewwidget.scene
        chipdir = PyRigApp.get_assets_dir()
        image = QImage((chipdir/'SMPTE_Color_Bars.png').as_posix())
        xx = 0
        nitems = 0
        for i in range(CHIP_I_MIN, CHIP_I_MAX, CHIP_I_STEP):
            xx += 1
            yy = 0
            for j in range(CHIP_J_MIN, CHIP_J_MAX, CHIP_J_STEP):
                nitems += 1
                with loading_step_context(f"Creating chip {nitems}",
                                          show_step_start=False):
                    yy += 1
                    x = (i + 11000)/22000
                    y = (j + 7000)/14000
                    color = QColor(image.pixel(int(image.width()*x),
                                               int(image.height()*y)))
                    item = Chip(color, xx, yy)
                    item.setPos(i, j)
                    scene.addItem(item)
