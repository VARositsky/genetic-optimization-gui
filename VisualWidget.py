import sys
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QBrush, QColor, QPen

class VisualWidget(qtw.QGraphicsView):
    def __init__(self, points=None, squares=None, parent=None):
        super().__init__(parent)

        self.scene = qtw.QGraphicsScene(self)
        self.setScene(self.scene)
        self.setDragMode(self.ScrollHandDrag)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setMouseTracking(True)
        self.cursor_cords = None
        points = points if points is not None else []
        squares = squares if squares is not None else []
        self.set_data(points, squares)

    def set_data(self, points, squares):
        self.scene.clear()

        self.cursor_cords = qtw.QGraphicsTextItem()
        self.cursor_cords.setZValue(1000)
        self.cursor_cords.setFlag(qtw.QGraphicsTextItem.ItemIgnoresTransformations)
        self.scene.addItem(self.cursor_cords)
        self.cursor_cords.setVisible(False)

        for x, y, w in squares:
            rect_item = qtw.QGraphicsRectItem(x, y, w, w)
            color = QColor(0, 128, 255, 80)
            rect_item.setBrush(QBrush(color))
            pen = QPen(Qt.blue, 5)
            pen.setCosmetic(True)
            rect_item.setPen(pen)
            self.scene.addItem(rect_item)

        for x, y in points:
            point_item = qtw.QGraphicsEllipseItem(x - 6, y - 6, 12, 12)
            point_item.setFlag(qtw.QGraphicsEllipseItem.ItemIgnoresTransformations)
            point_item.setBrush(QBrush(Qt.red))
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
        zoom_factor = 1.25
        factor = zoom_factor if event.angleDelta().y() > 0 else 1 / zoom_factor
        self.scale(factor, factor)
        cursor_pos = event.pos()
        self.cursor_cords.setPos(self.mapToScene(cursor_pos + QPoint(10, -10)))

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


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    v = VisualWidget(points=[(1, 3), (4, 4)], squares=[(-3, -5, 20), (1, 1, 20)])
    v.show()
    sys.exit(app.exec_())