from PyQt6.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem, QInputDialog
from PyQt6.QtGui import QBrush
from PyQt6.QtCore import Qt

class Bus(QGraphicsRectItem):
    def __init__(self, x, y, name="Bus", voltage=1.0, angle=0, width=40, height=20):
        super().__init__(-width / 2, -height / 2, width, height)  # Set rectangle size
        self.setPos(x, y)
        self.setBrush(QBrush(Qt.GlobalColor.blue))
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | 
                      QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.name = name
        self.voltage = voltage
        self.angle = angle
        self.lines = []  # Store connected lines

        self.text = QGraphicsTextItem(self.name, self)
        self.text.setPos(-width / 2 + 5, -height / 2 - 15)


    def mouseDoubleClickEvent(self, event):
        value, ok = QInputDialog.getDouble(None, "Edit Voltage", 
                                           "Enter Voltage (p.u.):", 
                                           self.voltage, 0, 10, 2)
        if ok:
            self.voltage = value

    def mouseMoveEvent(self, event):
        """ Update lines when moving the bus """
        super().mouseMoveEvent(event)
        #print(self.pos())
        for line in self.lines:
            line.updatePosition()

