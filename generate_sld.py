from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMainWindow, QLabel
from PyQt6.QtGui import QPainter, QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt
from sld_data import bus_data, line_data, source_data, load_data
from bus import Bus
from line import Line
from load import Load
from source import Source
import sys

class SLDCanvas(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 800, 600)
        self.buses = {}
        self.lines = []
        self.loads = {}
        self.sources = {}

        # Create example buses and lines
        for data in bus_data:
            bus = Bus(data["x"], data["y"], data["name"], data["voltage"], data["angle"], data["width"], data["height"])
            self.addItem(bus)
            self.buses[data["name"]] = bus
        
        for data in source_data:
            source = Source(data["x"], data["y"], data["voltage"], data["name"])
            self.addItem(source)
            self.sources[data["name"]] = source
        
        for data in load_data:
            load = Load(data["x"], data["y"], data["power"], data["name"])
            self.addItem(load)
            self.loads[data["name"]] = load
     
        for data in line_data:
            item1 = self.buses.get(data["item1"]) or self.sources.get(data["item1"]) or self.loads.get(data["item1"])
            item2 = self.buses.get(data["item2"]) or self.sources.get(data["item2"]) or self.loads.get(data["item2"])

            if item1 and item2:
                print(f"Connecting {item1.name} to {item2.name}")
                line = Line(data["name"], item1, item2, data["impedance"], data["is_directed"])
                self.addItem(line)
                self.lines.append(line)

class SLDApp(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(SLDCanvas())
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setWindowTitle("SCOPF Tool")
        self.resize(820, 620)
        self.setWindowIcon(QIcon("icon.webp"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SLDApp()
    window.show()
    sys.exit(app.exec())
