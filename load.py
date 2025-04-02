from PyQt6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QInputDialog, QGraphicsRectItem
from PyQt6.QtGui import QPen, QBrush
from PyQt6.QtCore import Qt

class Load(QGraphicsRectItem):
    def __init__(self, x, y, load_value=0.0, name="Load"):
        super().__init__(-20, -10, 20, 20)  # Rectangle shape
        self.setPos(x, y)  # Position of the load
        self.setBrush(QBrush(Qt.GlobalColor.green))  # Set the color of the load
        self.setPen(QPen(Qt.GlobalColor.black))  # Outline of the load
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | 
                      QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.name = name
        self.load_value = load_value
        self.lines = []  # Store connected lines

        # Create a text item for the load's name and value
        self.text_item = QGraphicsTextItem(f"{self.name}: {self.load_value} MW", self)
        self.text_item.setPos(-15, -25)  # Position of the text above the load

    def mouseDoubleClickEvent(self, event):
        # Edit the load value when double-clicked
        value, ok = QInputDialog.getDouble(None, "Edit Load", 
                                           f"Enter Load Value (MW) for {self.name}:",
                                           self.load_value, 0, 1000, 2)
        if ok:
            self.load_value = value
            # Update the text display to reflect the new load value
            self.text_item.setPlainText(f"{self.name}: {self.load_value} MW")
    
    def mouseMoveEvent(self, event):
        """ Update any connected items (like lines or buses) when the load is moved """
        super().mouseMoveEvent(event)
        #print(self.pos())
        for line in self.lines:
            line.updatePosition()
