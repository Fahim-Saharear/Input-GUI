from PyQt6.QtWidgets import QGraphicsLineItem, QInputDialog, QGraphicsPolygonItem, QGraphicsTextItem
from PyQt6.QtGui import QPen, QBrush, QPolygonF, QTransform 
from PyQt6.QtCore import Qt, QPointF, QLineF

class Line(QGraphicsLineItem):
    def __init__(self, name, item1, item2, impedance=0.1, is_directed=False):
        super().__init__()
        self.setPen(QPen(Qt.GlobalColor.black, 2))
        self.setFlags(QGraphicsLineItem.GraphicsItemFlag.ItemIsSelectable)
        self.setZValue(-1)
        self.name = name
        self.item1 = item1
        self.item2 = item2
        self.impedance = impedance
        self.is_directed = is_directed
        self.arrow_item = None  # To hold the arrow item

        # Link the line to both buses        
        item1.lines.append(self)
        item2.lines.append(self)
        self.updatePosition()

    def updatePosition(self):
        """ Adjust line position based on bus positions and update arrowhead direction """
        # Update the line between the two buses
        self.setLine(self.item1.scenePos().x(), self.item1.scenePos().y(), 
                     self.item2.scenePos().x(), self.item2.scenePos().y())

        # If the line is directed, update the arrow
        if self.is_directed:
            self.updateArrowhead()

    def updateArrowhead(self):
        """ Update the direction of the arrow at the end of the line """
        # Remove the previous arrow if it exists
        if self.arrow_item:
            self.scene().removeItem(self.arrow_item)
            self.arrow_item = None

        # Draw new arrow
        line = self.line()
        line_f = QLineF(line.p1(), line.p2())  # Create a QLineF for better angle calculation
        angle = line_f.angle()  # Get the angle of the line
        length = line_f.length()

        # Define the arrow size and position
        arrow_size = 10
        arrow = QPolygonF()
        arrow.append(QPointF(0, 0))
        arrow.append(QPointF(arrow_size, -arrow_size / 2))
        arrow.append(QPointF(arrow_size, arrow_size / 2))

        # Rotate the arrow to match the line’s angle
        transform = QTransform()
        transform.rotate(180 - angle)
        arrow = transform.map(arrow)

        # Calculate the position for the arrow (closer to p2)
        # Use a ratio t (0 <= t <= 1) to control how far from p1 the arrow will be
        t = 0.9  # 90% of the way from p1 to p2 (closer to p2 but not at p2)
        arrow_pos = line_f.pointAt(t)  # Get the point on the line at ratio t

        # Position the arrow at the end of the line
        arrow.translate(arrow_pos)

        # Create an arrow item and add it to the scene
        self.arrow_item = QGraphicsPolygonItem(arrow, self)
        self.arrow_item.setBrush(QBrush(Qt.GlobalColor.red))  # Set arrow color
        self.arrow_item.setZValue(1)  # Ensure the arrow is above the line

    def mouseDoubleClickEvent(self, event):
        value, ok = QInputDialog.getDouble(None, "Edit Impedance", 
                                           "Enter Impedance (p.u.):", 
                                           self.impedance, 0, 10, 2)
        if ok:
            self.impedance = value

    def mouseMoveEvent(self, event):
        """ Update the position of the line and arrow dynamically when the buses are moved """
        self.updatePosition()
        super().mouseMoveEvent(event)
