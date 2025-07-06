from PySide2.QtWidgets import (
    QGraphicsItem, QStyleOptionGraphicsItem, QWidget, QStyle,
    QGraphicsSceneMouseEvent,
)
from PySide2.QtCore import QRectF, QRect, Qt, QLineF, QPoint
from PySide2.QtGui import QPainterPath, QColor, QPainter, QBrush, QPen, QFont
from ...logging import log_func_call, DEBUGLOW2

ITEMFLAGS = QGraphicsItem.GraphicsItemFlag


class Chip(QGraphicsItem):
    @log_func_call(DEBUGLOW2, trace_only=True)
    def __init__(self, color: QColor, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.setZValue((x + y) % 2)
        self.setFlags(ITEMFLAGS.ItemIsSelectable | ITEMFLAGS.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        self.stuff: list[QPoint] = list()

    @log_func_call(DEBUGLOW2, trace_only=True)
    def boundingRect(self):
        return QRectF(0, 0, 110, 70)

    @log_func_call(DEBUGLOW2, trace_only=True)
    def shape(self):
        path = QPainterPath()
        path.addRect(14, 14, 82, 42)
        return path

    @log_func_call(DEBUGLOW2, trace_only=True)
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem,
              widget: QWidget):
        stuff = self.stuff

        fillColor = (self.color.darker(150)
                     if option.state & QStyle.State_Selected else self.color)
        if option.state & QStyle.State_MouseOver:
            fillColor = fillColor.lighter(125)

        lod = option.levelOfDetailFromTransform(painter.worldTransform())
        if lod < 0.2:
            if lod < 0.125:
                painter.fillRect(QRectF(0, 0, 110, 70), fillColor)
                return

            b = painter.brush()
            painter.setBrush(fillColor)
            painter.drawRect(13, 13, 97, 57)
            painter.setBrush(b)
            return

        oldPen = painter.pen()
        pen = oldPen
        width = 0
        if option.state & QStyle.State_Selected:
            width += 2

        pen.setWidth(width)
        b = painter.brush()
        darkscale = 120 if option.state & QStyle.State_Sunken else 100
        painter.setBrush(QBrush(fillColor.darker(darkscale)))

        painter.drawRect(QRect(14, 14, 79, 39))
        painter.setBrush(b)

        if lod >= 1:
            painter.setPen(QPen(Qt.gray, 1))
            painter.drawLine(15, 54, 94, 54)
            painter.drawLine(94, 53, 94, 15)
            painter.setPen(QPen(Qt.black, 0))

        # Draw text
        if lod >= 2:
            font = QFont("Times", 10)
            font.setStyleStrategy(QFont.ForceOutline)
            painter.setFont(font)
            painter.save()
            painter.scale(0.1, 0.1)
            painter.drawText(170, 180, f"Model: VSC-2000 (Very Small Chip) at {self.x}x{self.y}")  # noqa: E501
            painter.drawText(170, 200, "Serial number: DLWR-WEER-123L-ZZ33-SDSJ")  # cspell:disable-line  # noqa: E501
            painter.drawText(170, 220, "Manufacturer: Chip Manufacturer")
            painter.restore()

        # Draw lines
        lines = []
        if lod >= 0.5:
            for i in range(0, 11, 1 if lod > 0.5 else 2):
                lines.append(QLineF(18 + 7 * i, 13, 18 + 7 * i, 5))
                lines.append(QLineF(18 + 7 * i, 54, 18 + 7 * i, 62))

            for i in range(0, 7, 1 if lod > 0.5 else 2):
                lines.append(QLineF(5, 18 + i * 5, 13, 18 + i * 5))
                lines.append(QLineF(94, 18 + i * 5, 102, 18 + i * 5))

        if lod >= 0.4:
            lineData = [
                QLineF(25, 35, 35, 35),
                QLineF(35, 30, 35, 40),
                QLineF(35, 30, 45, 35),
                QLineF(35, 40, 45, 35),
                QLineF(45, 30, 45, 40),
                QLineF(45, 35, 55, 35)
            ]
            lines.extend(lineData)

        painter.drawLines(lines)

        # Draw red ink
        if len(stuff) > 1:
            p = painter.pen()
            painter.setPen(QPen(Qt.red, 1, Qt.SolidLine, Qt.RoundCap,
                                Qt.RoundJoin))
            painter.setBrush(Qt.NoBrush)
            path = QPainterPath()
            path.moveTo(stuff[0])
            for i in range(1, len(stuff)):
                path.lineTo(stuff[i])
            painter.drawPath(path)
            painter.setPen(p)

    @log_func_call
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        super().mousePressEvent(event)
        self.update()

    @log_func_call
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if event.modifiers() & Qt.ShiftModifier:
            self.stuff.append(event.pos())
            self.update()
        else:
            super().mouseMoveEvent(event)

    @log_func_call
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        self.update()
        super().mouseReleaseEvent(event)
