from PySide2.QtGui import QIcon
from pyapp.gui.abc import QtApplicationBase, QtWindowWrapper

from ..logging import (
    log_func_call as _log_func_call,
    get_logger as _get_logger
)
from ..app import PyRigApp as _PyRigApp
from .splash import SplashScreen
from .main import MainWindow


class PyRigGui(QtApplicationBase):
    INIT_GUI_IN_CONSTRUCTOR: bool = True

    @_log_func_call
    def __init__(self, app_args: list[str], *firstwin_args,
                 **firstwin_kwargs):
        super().__init__(app_args, *firstwin_args, **firstwin_kwargs)
        self.splash: SplashScreen
        self.icon: QIcon = None

    @_log_func_call
    def create_first_window(self, *args, **kwargs) -> QtWindowWrapper:
        mw = MainWindow()
        self.windows.append(mw)
        mwview = mw.get_window()
        mwview.show()
        mwview.bring_to_front()

    @_log_func_call
    def init_gui(self, app_args: list[str], *firstwin_args, **firstwin_kwargs):
        super().init_gui(app_args, *firstwin_args, **firstwin_kwargs)
        self.load_icon()
        super().close_splash(self.windows[0].get_window_qtroot())

    @_log_func_call
    def load_icon(self):
        icon_path = _PyRigApp.get_assets_dir()/'logo.svg'
        if icon_path.exists():
            icon = QIcon(icon_path.as_posix())
            self.icon = icon
            self.qtroot.setWindowIcon(icon)
        else:
            _get_logger().error(f'Icon {icon_path} not found')

    @_log_func_call
    def create_splash(self):
        return SplashScreen()
