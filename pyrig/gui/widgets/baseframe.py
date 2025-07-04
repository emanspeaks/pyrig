from PySide2.QtWidgets import (
    QGraphicsView, QFrame, QLabel, QSlider, QWidget, QStyle,
    QVBoxLayout, QHBoxLayout, QGridLayout, QButtonGroup, QDialog
)
from PySide2.QtGui import QPainter, QTransform, QWheelEvent
from PySide2.QtOpenGL import QGLFormat, QGLWidget, QGL
from PySide2.QtCore import QSize, Qt, QRectF
from PySide2.QtPrintSupport import QPrintDialog, QPrinter

from pyapp.qt_gui.widgets.windowbase import WindowBaseFrame
from pyapp.qt_gui.widgets.graphview import GraphViewWidget
from pyapp.qt_gui.abc import QtWindowWrapper
from pyapp.qt_gui.utils import (
    create_icon_toolbtn, create_text_toolbtn, create_slider
)

from ...app import PyRigApp
from ...logging import log_func_call, get_logger


class BaseView(WindowBaseFrame):
    BASE_ICON_PATHS = {
        "zoom_in": "zoomin.png",
        "zoom_out": "zoomout.png",
        "rotate_left": "rotateleft.png",
        "rotate_right": "rotateright.png",
        "print": "fileprint.png",
    }

    @classmethod
    @log_func_call
    def get_icon_path(cls, key: str):
        return PyRigApp.get_assets_dir()/'chip'/cls.BASE_ICON_PATHS[key]

    @log_func_call
    def add_zoom_controls(self):
        zoomInIcon = create_icon_toolbtn(self, self.icon_size,
                                         self.get_icon_path("zoom_in"),
                                         self.zoomIn, True)
        zoomOutIcon = create_icon_toolbtn(self, self.icon_size,
                                          self.get_icon_path("zoom_out"),
                                          self.zoomOut, True)

        zoomSlider = create_slider(self, 0, 500, 250, self.setupMatrix)
        zoomSlider.setTickPosition(QSlider.TicksRight)
        self.zoomSlider = zoomSlider

        zoomSliderLayout = QVBoxLayout()
        zoomSliderLayout.addWidget(zoomInIcon)
        zoomSliderLayout.addWidget(zoomSlider)
        zoomSliderLayout.addWidget(zoomOutIcon)
        return zoomSliderLayout

    @log_func_call
    def add_rotate_controls(self):
        rotateLeftIcon = create_icon_toolbtn(self, self.icon_size,
                                             self.get_icon_path("rotate_left"),
                                             self.rotateLeft)
        rotateRightIcon = create_icon_toolbtn(self, self.icon_size,
                                              self.get_icon_path("rotate_right"),  # noqa: E501
                                              self.rotateRight)

        rotateSlider = create_slider(self, -360, 360, 0, self.setupMatrix)
        rotateSlider.setOrientation(Qt.Horizontal)
        rotateSlider.setTickPosition(QSlider.TicksBelow)
        self.rotateSlider = rotateSlider

        rotateSliderLayout = QHBoxLayout()
        rotateSliderLayout.addWidget(rotateLeftIcon)
        rotateSliderLayout.addWidget(rotateSlider)
        rotateSliderLayout.addWidget(rotateRightIcon)
        return rotateSliderLayout

    @log_func_call
    def add_view(self):
        viewwidget = GraphViewWidget(self)
        self.viewwidget = viewwidget

        view = viewwidget.view
        view.setRenderHint(QPainter.Antialiasing, False)
        view.setDragMode(QGraphicsView.RubberBandDrag)
        view.setOptimizationFlags(QGraphicsView.DontSavePainterState)
        view.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        view.wheelEvent = self.wheelEvent

        vscroll = view.verticalScrollBar()
        vscroll.valueChanged.connect(self.setResetButtonEnabled)

        hscroll = view.horizontalScrollBar()
        hscroll.valueChanged.connect(self.setResetButtonEnabled)

        return view

    @log_func_call
    def add_reset_button(self):
        resetbtn = create_text_toolbtn(self, "0", self.resetView,
                                       enabled=False)
        self.resetButton = resetbtn
        return resetbtn

    @log_func_call
    def add_ptr_mode_buttons(self):
        selectModeButton = create_text_toolbtn(self, "Select",
                                               self.togglePointerMode,
                                               toggleable=True,
                                               toggle_depressed=True)
        self.selectModeButton = selectModeButton

        dragModeButton = create_text_toolbtn(self, "Drag",
                                             self.togglePointerMode,
                                             toggleable=True)
        self.dragModeButton = dragModeButton

        pointerModeGroup = QButtonGroup(self.qtroot)
        pointerModeGroup.setExclusive(True)
        pointerModeGroup.addButton(selectModeButton)
        pointerModeGroup.addButton(dragModeButton)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Pointer Mode"))
        layout.addWidget(selectModeButton)
        layout.addWidget(dragModeButton)
        return layout

    @log_func_call
    def add_graphics_ctrl_buttons(self):
        antialiasButton = create_text_toolbtn(self, "Antialiasing",
                                              self.toggleAntialiasing,
                                              toggleable=True)
        self.antialiasButton = antialiasButton

        openGlButton = create_text_toolbtn(self, "OpenGL",
                                           self.toggleOpenGL,
                                           toggleable=True,
                                           enabled=QGLFormat.hasOpenGL())
        self.openGlButton = openGlButton

        printButton = create_icon_toolbtn(self, self.icon_size,
                                          self.get_icon_path("print"),
                                          self.print)
        self.printButton = printButton

        layout = QHBoxLayout()
        layout.addWidget(antialiasButton)
        layout.addWidget(openGlButton)
        layout.addWidget(printButton)
        return layout

    @log_func_call
    def __init__(self, parent: QtWindowWrapper, name: str = "Chip View"):
        super().__init__(parent)
        self.name = name

        frame = self.qtroot
        frame.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)

        icon_width = frame.style().pixelMetric(QStyle.PM_ToolBarIconSize)
        self.icon_size = QSize(icon_width, icon_width)

        topbar = QHBoxLayout()
        topbar.addWidget(QLabel(name))
        topbar.addStretch()
        topbar.addLayout(self.add_ptr_mode_buttons())
        topbar.addStretch()
        topbar.addLayout(self.add_graphics_ctrl_buttons())

        baselayout = QGridLayout()
        baselayout.addLayout(topbar, 0, 0)
        baselayout.addWidget(self.add_view(), 1, 0)
        baselayout.addLayout(self.add_zoom_controls(), 1, 1)
        baselayout.addLayout(self.add_rotate_controls(), 2, 0)
        baselayout.addWidget(self.add_reset_button(), 2, 1)
        frame.setLayout(baselayout)

        self.setupMatrix()

    @log_func_call
    def zoomIn(self):
        self.zoomSlider.setValue(self.zoomSlider.value() + 1)

    @log_func_call
    def zoomOut(self):
        self.zoomSlider.setValue(self.zoomSlider.value() - 1)

    @log_func_call
    def zoomInBy(self, level: int):
        self.zoomSlider.setValue(self.zoomSlider.value() + level)

    @log_func_call
    def zoomOutBy(self, level: int):
        self.zoomSlider.setValue(self.zoomSlider.value() - level)

    @log_func_call
    def resetView(self):
        self.zoomSlider.setValue(250)
        self.rotateSlider.setValue(0)
        self.setupMatrix()
        self.viewwidget.view.ensureVisible(QRectF(0, 0, 0, 0))
        self.resetButton.setEnabled(False)

    @log_func_call
    def setResetButtonEnabled(self, value=None):
        self.resetButton.setEnabled(True)

    @log_func_call
    def setupMatrix(self, value=None):
        scale = 2 ** ((self.zoomSlider.value() - 250) / 50)
        matrix = QTransform()
        matrix.scale(scale, scale)
        matrix.rotate(self.rotateSlider.value())
        self.viewwidget.view.setTransform(matrix)
        self.setResetButtonEnabled()

    @log_func_call
    def togglePointerMode(self, checked: bool):
        view = self.viewwidget.view
        view.setDragMode(QGraphicsView.RubberBandDrag
                         if self.selectModeButton.isChecked()
                         else QGraphicsView.ScrollHandDrag)
        view.setInteractive(self.selectModeButton.isChecked())

    @log_func_call
    def toggleOpenGL(self, checked: bool):
        view = self.viewwidget.view
        view.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers))
                         if self.openGlButton.isChecked()
                         else QWidget())

    @log_func_call
    def toggleAntialiasing(self, checked: bool):
        self.viewwidget.view.setRenderHint(QPainter.Antialiasing,
                                           self.antialiasButton.isChecked())

    @log_func_call
    def print(self):
        printer = QPrinter(QPrinter.HighResolution)
        widget = self.qtroot
        dialog = QPrintDialog(printer, widget)
        if dialog.exec_() == QDialog.Accepted:
            view = self.viewwidget.view
            painter = QPainter(printer)
            try:
                # via trial and error, found that this needs both rects to
                # work reliably
                view.render(painter, QRectF(printer.pageRect()), view.rect())

            finally:
                if painter.isActive():
                    painter.end()
                else:
                    get_logger().error("Failed to end QPainter on printer")

    @log_func_call
    def rotateLeft(self):
        self.rotateSlider.setValue(self.rotateSlider.value() - 10)

    @log_func_call
    def rotateRight(self):
        self.rotateSlider.setValue(self.rotateSlider.value() + 10)

    @log_func_call
    def wheelEvent(self, e: QWheelEvent):
        if e.modifiers() & Qt.ControlModifier:
            if e.angleDelta().y() > 0:
                self.zoomInBy(6)
            else:
                self.zoomOutBy(6)
            e.accept()

        else:
            QGraphicsView.wheelEvent(self.viewwidget.view, e)
