import sys
import os
import platform
import subprocess
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog
from PyQt6.QtGui import QAction, QIcon, QPixmap, QImage
from PyQt6.QtCore import Qt, QDate
from datetime import datetime

from weather import get_weather_data
from models import predict_load, predict_generation
from process_data import process_data_load, process_data_generation, is_solar

class PowerSystemGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Power System Planning Study Tool")
        self.setGeometry(100, 100, 800, 500)  # Default size
        self.setWindowIcon(QIcon("icon.webp"))

        # Load and process the background image once
        self.process_background_image("bg.jpg")

        # Background Label for Image
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(self.bg_pixmap)
        self.bg_label.setScaledContents(True)  # Enables smooth resizing

        # Semi-transparent overlay to improve contrast
        self.overlay = QLabel(self)
        self.overlay.setStyleSheet("background-color: rgba(255, 255, 255, 150);")
        self.overlay.lower()  # Ensure it's behind everything

        # Central Widget and Layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

        # Create Menu Bar
        self.create_menu_bar()

        # Title Label
        title_label = QLabel("Power System Planning Study Tool")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; background: transparent; padding: 5px;")
        self.main_layout.addWidget(title_label)

        # Forecast Model Selection Buttons
        self.create_forecast_buttons()

        # Date and Hour Dropdowns
        self.create_datetime_dropdowns()

        # Run Optimization Button
        self.run_button = QPushButton("Run Optimization")
        self.run_button.setStyleSheet("font-weight: bold; padding: 8px; background-color: gray;")
        self.run_button.clicked.connect(self.run_optimization)
        self.main_layout.addWidget(self.run_button, alignment=Qt.AlignmentFlag.AlignCenter)


        # Selected Model
        self.selected_model = None
        self.date = None
        self.hour = None

        # Results
        self.load_prediction = None
        self.gen_prediction_solar = None
        self.gen_prediction_wind = None

    def process_background_image(self, image_path):
        """Loads, blurs, and stores the background image."""
        if os.path.exists(image_path):
            try:
                img = cv2.imread(image_path)
                img = cv2.GaussianBlur(img, (15, 15), 10)  # Apply blur effect
                height, width, channel = img.shape
                bytes_per_line = channel * width
                qt_img = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

                self.bg_pixmap = QPixmap.fromImage(qt_img)
            except Exception as e:
                print(f"Error applying blur effect: {e}")
                self.bg_pixmap = QPixmap(image_path)  # Use normal image if blur fails
        else:
            self.bg_pixmap = QPixmap()  # Empty pixmap if image doesn't exist

    def resizeEvent(self, event):
        """Smoothly adjusts the background size without reprocessing the image."""
        self.bg_label.setGeometry(self.rect())  # Resize image with window
        self.overlay.setGeometry(self.rect())  # Resize overlay as well
        super().resizeEvent(event)

    def create_menu_bar(self):
        """Creates the menu bar."""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(QAction("New", self, triggered=self.reset_gui))
        file_menu.addAction(QAction("Exit", self, triggered=self.quit_app))

        about_menu = menu_bar.addMenu("&About")
        about_menu.addAction(QAction("User Manual", self, triggered=self.open_user_manual))

        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(QAction("Update", self, triggered=self.update_status))

    def create_forecast_buttons(self):
        """Creates buttons for selecting a forecasting model."""
        forecast_layout = QHBoxLayout()
        forecast_label = QLabel("Select Forecast Model - ")
        forecast_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        forecast_label.setStyleSheet("background: transparent; padding: 2px;")
        forecast_layout.addWidget(forecast_label)

        self.model_buttons = {}
        models = ["Random Forest", "xGBoost", "Neural Net"]
        for model in models:
            btn = QPushButton(model)
            btn.setCheckable(True)
            btn.setStyleSheet("background-color: lightgray; padding: 5px;")
            btn.clicked.connect(lambda checked, m=model: self.select_forecast_model(m))
            self.model_buttons[model] = btn
            forecast_layout.addWidget(btn)

        self.main_layout.addLayout(forecast_layout)

    def select_forecast_model(self, selected_model):
        """Handles forecast model selection."""
        for model, button in self.model_buttons.items():
            if model == selected_model:
                button.setChecked(True)
                button.setStyleSheet("background-color: green; color: white; padding: 5px; font-weight: bold;")
                self.status_bar.showMessage(f"{model} Model Selected")
                self.selected_model = model  # Store the selected model
            else:
                button.setChecked(False)
                button.setStyleSheet("background-color: lightgray; padding: 5px;")
    
    def get_selected_date(self):
        selected_date = self.date_dropdown.currentText()
        selected_hour = self.hour_dropdown.currentText()
        self.date = selected_date
        self.hour = selected_hour
        return self.date

    def create_datetime_dropdowns(self):
        """Creates date and hour selection dropdowns."""
        datetime_layout = QHBoxLayout()

        # Date Dropdown
        date_label = QLabel("Select Date")
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_label.setStyleSheet("background: transparent; padding-bottom: 2px;")
        self.date_dropdown = QComboBox()
        self.populate_date_dropdown()
        self.date_dropdown.setFixedWidth(240)

        # Hour Dropdown
        hour_label = QLabel("Select Hour")
        hour_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hour_label.setStyleSheet("background: transparent; padding-bottom: 2px;")
        self.hour_dropdown = QComboBox()
        self.hour_dropdown.addItems([str(h) for h in range(24)])
        self.hour_dropdown.setFixedWidth(240)

        # Add to layout
        datetime_layout.addWidget(date_label)
        datetime_layout.addWidget(self.date_dropdown)
        datetime_layout.addWidget(hour_label)
        datetime_layout.addWidget(self.hour_dropdown)
        self.main_layout.addLayout(datetime_layout)

    def populate_date_dropdown(self):
        """Populates date dropdown with the next 7 days."""
        today = QDate.currentDate()
        for i in range(0, 7):
            self.date_dropdown.addItem(today.addDays(i).toString("yyyy-MM-dd"))


    def reset_gui(self):
        """Resets GUI to default state."""
        for button in self.model_buttons.values():
            button.setChecked(False)
            button.setStyleSheet("background-color: lightgray; padding: 5px;")
        self.date_dropdown.setCurrentIndex(0)
        self.hour_dropdown.setCurrentIndex(0)
        self.status_bar.showMessage("Ready")

    def open_user_manual(self):
        """Opens the user manual PDF."""
        manual_path = os.path.abspath("User_Manual.pdf")
        if os.path.exists(manual_path):
            if platform.system() == "Windows":
                os.startfile(manual_path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", manual_path])
            else:
                subprocess.run(["xdg-open", manual_path])
        else:
            self.status_bar.showMessage("User Manual not found!")

    def run_forecast(self):
        """Runs the forecast script."""
        self.get_selected_date()
        # data = process_data(self.date, self.hour)
        date = datetime.strptime(f"{self.date} {self.hour}", "%Y-%m-%d %H")
        load_data = process_data_load(date)
        generation_data = process_data_generation(date)


        if self.selected_model == "Random Forest":
            self.load_prediction = predict_load("load_random_forsest", load_data)
            self.gen_prediction_wind = predict_generation("gen_random_forsest", generation_data)
            self.gen_prediction_solar = predict_generation("gen_random_forsest", is_solar(generation_data))
        elif self.selected_model == "xGBoost":
            self.load_prediction = predict_load("load_xgboost", load_data)
            self.gen_prediction_wind = predict_generation("gen_xgboost", generation_data)
            self.gen_prediction_solar = predict_generation("gen_xgboost", is_solar(generation_data))
        elif self.selected_model == "Neural Net":
            self.load_prediction = predict_load("load_neural_network", load_data)
            self.gen_prediction_wind = predict_generation("gen_neural_network", generation_data)
            self.gen_prediction_solar = predict_generation("gen_neural_network", is_solar(generation_data))

        self.status_bar.showMessage(f"Forecasting Completed {self.gen_prediction_solar} {self.gen_prediction_wind} {self.load_prediction}")


    def run_optimization(self):
        """Runs the optimization script."""
        self.run_forecast()
        # script_path = os.path.abspath("generate_sld.py")
        # if os.path.exists(script_path):
        #     subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #     self.status_bar.showMessage("Running SLD Optimization...")
        # else:
        #     self.status_bar.showMessage("SLD script not found!")

    def update_status(self):
        self.status_bar.showMessage("Running Updated Version")

    def quit_app(self):
        QApplication.quit()

if __name__ == "__main__":
    # Download weather data
    get_weather_data()
    app = QApplication(sys.argv)
    window = PowerSystemGUI()
    window.show()
    sys.exit(app.exec())