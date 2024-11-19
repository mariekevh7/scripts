import numpy as np
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem

POINT_RADIUS = 2

class PolygonDrawer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.points = {}
        self.setDragMode(QGraphicsView.NoDrag)
        # no drag didn't work so set the scene rect to keep scene from moving
        self.scene.setSceneRect(0, 0, 800, 600)
        self.polygon_item = None

    def mousePressEvent(self, event):
        click_pos = self.mapToScene(event.pos())
        new_x = click_pos.x()
        new_y = click_pos.y()
        if event.button() == 1:
            # point already exists
            if f"{new_x:.1f}, {new_y:.1f}" in self.points.keys():
                return

            # show ellipse to mark a corner point
            item = QGraphicsEllipseItem(click_pos.x() - POINT_RADIUS, click_pos.y() - POINT_RADIUS, POINT_RADIUS*2, POINT_RADIUS*2)
            item.setBrush(Qt.red)
            item.setPen(Qt.red)
            self.scene.addItem(item)

            self.points[f"{new_x:.1f}, {new_y:.1f}"] = item

            # If there are enough points (3 or more), draw the polygon
            if len(self.points) > 2:
                pts_list = [(float(x), float(y)) for pos in self.points.keys() for x, y in [pos.split(",")]]
                polygon = QPolygonF([QPointF(*p) for p in pts_list])
                if hasattr(self, 'polygon_item') and self.polygon_item is not None:
                    self.scene.removeItem(self.polygon_item)
                self.polygon_item = self.scene.addPolygon(polygon, Qt.red)

        elif event.button() == 2:
            # right click, see if it interferes with any points
            for pos in reversed(self.points.keys()):
                x, y = pos.split(",")
                distance = np.sqrt((float(x) - new_x) ** 2 + (float(y) - new_y) ** 2)
                print(distance, x, y)
                if distance <= POINT_RADIUS*1.2:
                    # remove the point within radius (+ 20% buffer)
                    self.scene.removeItem(self.points[pos])
                    self.points.pop(pos)
                    return

    def reset(self):
        self.points = []
        self.scene.clear()


if __name__ == '__main__':
    app = QApplication([])

    window = PolygonDrawer()
    window.setWindowTitle("Polygon Drawer")
    window.resize(400, 400)
    window.show()

    app.exec_()

