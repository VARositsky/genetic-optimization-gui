import sys

import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QBrush, QColor, QPen


class VisualWidget(qtw.QGraphicsView):
    def __init__(self, points=None, squares=None, parent=None):
        super().__init__(parent)
        self.colors = None
        self.scene = qtw.QGraphicsScene(self)
        self.setScene(self.scene)
        self.setDragMode(self.ScrollHandDrag)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setMouseTracking(True)
        self.cursor_cords = None
        self.set_data(points, squares, update=False)
        self.set_theme("white")

    def set_theme(self, theme):
        themes = {
            "white": {
                "bg_color": Qt.white,
                "sqr_color": QColor(0, 128, 255, 80),
                "sqr_border_color": Qt.blue,
                "point_color": Qt.red,
                "text_color": Qt.black,
                "covered_point_color": Qt.green,
                "border_color": "#cccccc"
            },
            "dark": {
                "bg_color": QColor("#0f0124"),
                "sqr_color": QColor(149, 242, 128, 128),
                "sqr_border_color": QColor("#0cc56c"),
                "point_color": QColor(207, 17, 42),
                "text_color": Qt.white,
                "covered_point_color": Qt.green,
                "border_color": "black",
            }
        }

        self.colors = themes.get(theme, themes["white"])
        border_color = self.colors.get("border_color", "#cccccc")
        self.setStyleSheet(f"QGraphicsView {{ border: 1px solid {border_color}; }}")

        self.draw()

    def set_data(self, points, squares, update=True):
        self.points = points if points is not None else []
        self.squares = squares if squares is not None else []
        if update: self.draw()

    def draw(self):
        self.scene.clear()
        self.scene.setBackgroundBrush(self.colors["bg_color"])

        self.cursor_cords = qtw.QGraphicsTextItem()
        self.cursor_cords.setZValue(1000)
        self.cursor_cords.setFlag(qtw.QGraphicsTextItem.ItemIgnoresTransformations)
        self.scene.addItem(self.cursor_cords)
        self.cursor_cords.setDefaultTextColor(self.colors["text_color"])
        self.cursor_cords.setVisible(False)

        for square in self.squares:
            x, y, w = square.x, square.y, square.w
            rect_item = qtw.QGraphicsRectItem(x, y, w, w)
            color = self.colors["sqr_color"]
            rect_item.setBrush(QBrush(color))
            pen = QPen(self.colors["sqr_border_color"], 5)
            pen.setCosmetic(True)
            rect_item.setPen(pen)
            self.scene.addItem(rect_item)

        for x, y in self.points:
            point_item = qtw.QGraphicsEllipseItem(-6, -6, 12, 12)
            point_item.setPos(x, y)

            if self._is_point_covered(x, y):
                point_color = self.colors["covered_point_color"]
            else:
                point_color = self.colors["point_color"]

            point_item.setBrush(QBrush(point_color))
            point_item.setPen(QPen(point_color))

            point_item.setFlag(
                qtw.QGraphicsItem.ItemIgnoresTransformations
            )

            self.scene.addItem(point_item)

        bounding_rect = self.scene.itemsBoundingRect()
        if not bounding_rect.isNull():
            center = bounding_rect.center()
            bounding_rect.setSize(bounding_rect.size() * 1.25)
            bounding_rect.moveCenter(center)
            self.scene.setSceneRect(bounding_rect)
        else:
            self.scene.setSceneRect(-100, -100, 800, 600)
            

        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def wheelEvent(self, event):
        # Один стандартный шаг колеса изменяет масштаб примерно на 10%.
        zoom_factor = 1.10
        wheel_steps = event.angleDelta().y() / 120.0
        factor = zoom_factor ** wheel_steps

        current_scale = self.transform().m11()
        new_scale = current_scale * factor

        # Ограничение слишком сильного приближения и отдаления.
        if 0.05 <= new_scale <= 100:
            self.scale(factor, factor)

        cursor_pos = event.pos()

        self.cursor_cords.setPos(
            self.mapToScene(cursor_pos + QPoint(10, -10))
        )

    def mouseMoveEvent(self, event):
        cursor_pos = event.pos()
        self.cursor_cords.setPos(self.mapToScene(cursor_pos + QPoint(10, -10)))
        scenePos = self.mapToScene(cursor_pos)
        self.cursor_cords.setPlainText(f"{scenePos.x():.4f}, {scenePos.y():.4f}")
        self.cursor_cords.setVisible(True)
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self.cursor_cords.setVisible(False)
        super().leaveEvent(event)
    
    @staticmethod
    def _get_square_values(square):
        """Поддерживает как Square, так и кортеж (x, y, w)."""
        if hasattr(square, "x"):
            return square.x, square.y, square.w

        return square


    def _is_point_covered(self, point_x, point_y):
        for square in self.squares:
            square_x, square_y, width = self._get_square_values(square)

            if (
                square_x <= point_x <= square_x + width
                and square_y <= point_y <= square_y + width
            ):
                return True

        return False