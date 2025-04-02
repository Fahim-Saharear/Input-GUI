from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsTextItem, QInputDialog, QGraphicsPolygonItem, QGraphicsRectItem
from PyQt6.QtGui import QPen, QBrush, QPainter, QPainterPath, QPolygonF, QTransform 
from PyQt6.QtCore import Qt, QPointF, QLineF

class Source(QGraphicsEllipseItem):
    def __init__(self, x, y, voltage=1.0, name="Source"):
        super().__init__(-15, -15, 30, 30)  # Circle shape
        self.setPos(x, y)  # Position of the source
        self.setBrush(QBrush(Qt.GlobalColor.red))  # Set the color of the source
        self.setPen(QPen(Qt.GlobalColor.black))  # Outline of the source
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | 
                      QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.name = name
        self.voltage = voltage
        self.lines = []  # Store connected lines

        # Create a text item for the source's name and voltage
        self.text_item = QGraphicsTextItem(f"{self.name}: {self.voltage} p.u.", self)
        self.text_item.setPos(-10, -25)  # Position of the text above the source

    def mouseDoubleClickEvent(self, event):
        # Edit the voltage when double-clicked
        value, ok = QInputDialog.getDouble(None, "Edit Voltage", 
                                           f"Enter Voltage (p.u.) for {self.name}:",
                                           self.voltage, 0, 10, 2)
        
        if ok:
            self.voltage = value
            # Update the text display to reflect the new voltage value
            self.text_item.setPlainText(f"{self.name}: {self.voltage} p.u.")
    
    def mouseMoveEvent(self, event):
        """ Update any connected items (like lines or buses) when the source is moved """
        super().mouseMoveEvent(event)
        #print(self.pos())
        for line in self.lines:
            line.updatePosition()

