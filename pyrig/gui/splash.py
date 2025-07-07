from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt
from PySide2.QtSvg import QSvgRenderer

from pyapp.qt_gui.abc import QtSplashScreen

from ..app import PyRigApp


class SplashScreen(QtSplashScreen):
    def __init__(self):
        splash_path = PyRigApp.get_assets_dir()/'logo.svg'
        mode = Qt.AspectRatioMode.KeepAspectRatio
        pixmap = QPixmap(splash_path.as_posix() if splash_path.exists()
                         else None).scaled(400, 400, aspectMode=mode)
        super().__init__(pixmap)
        self.set_progress(message="Loading PyRig...")
