from PySide2.QtGui import QPixmap, QPainter
from PySide2.QtCore import Qt, QSize
from PySide2.QtSvg import QSvgRenderer

from pyapp.gui.abc import QtSplashScreen

from ..app import PyRigApp


class SplashScreen(QtSplashScreen):
    def __init__(self):
        splash_path = PyRigApp.get_assets_dir()/'logo.svg'
        size = QSize(400, 400)
        pixmap = QPixmap(size)
        pixmap.fill(Qt.gray)
        if splash_path.exists():
            renderer = QSvgRenderer(splash_path.as_posix())
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            try:
                renderer.render(painter)
            finally:
                painter.end()

        super().__init__(pixmap)
        self.set_progress(message="Loading PyRig...")
