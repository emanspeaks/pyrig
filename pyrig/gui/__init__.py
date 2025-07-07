from pathlib import Path

from PySide2.QtGui import QIcon

from pyapp.qt_gui.abc import QtApplicationBase, QtWindowWrapper
from pyapp.config.keys import APP_ASSETS_DIR_KEY

from ..logging import (
    log_func_call as _log_func_call,
    get_logger as _get_logger, WARN
)
from ..app import PyRigApp as _PyRigApp


class PyRigGui(QtApplicationBase):
    """
    PyRig GUI Application class.
    This class initializes the GUI application and manages the main window.
    """

    INIT_GUI_IN_CONSTRUCTOR: bool = True

    @_log_func_call
    def __init__(self, app_args: list[str], *firstwin_args,
                 **firstwin_kwargs):
        super().__init__(app_args, *firstwin_args, **firstwin_kwargs)
        self.icon: QIcon = None

    @_log_func_call(WARN)
    def create_first_window(self, *args, **kwargs) -> QtWindowWrapper:
        "sets self.window to an instance of the concrete main window object"
        from .main import MainWindow
        mw = MainWindow()
        self.windows.append(mw)
        mwview = mw.get_window()
        mwview.get_window_qtroot().showNormal()  # Ensure start not minimized
        mwview.show()

    @_log_func_call
    def init_gui(self, app_args: list[str], *firstwin_args, **firstwin_kwargs):
        super().init_gui(app_args, *firstwin_args, **firstwin_kwargs)
        self.load_icon()

    @_log_func_call
    def load_icon(self):
        icon_path = Path(_PyRigApp.get(APP_ASSETS_DIR_KEY, '.'))/'logo.svg'
        if icon_path.exists():
            icon = QIcon(icon_path.as_posix())
            self.icon = icon
            self.qtroot.setWindowIcon(icon)
        else:
            _get_logger().error(f'Icon {icon_path} not found')
