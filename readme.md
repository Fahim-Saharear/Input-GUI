# Power System Visualization Tool

A Python-based power system visualization tool that uses PyQt6 to create and manipulate a graphical scene representing electrical components like buses, lines, loads, and power sources. This tool allows for dynamic interaction with the system, such as editing impedances, voltage, and power values of components, and visualizing connections between them.

## Features

- **Interactive Buses**: Bus components can be represented by rectangles, and their properties can be edited (e.g., voltage).
- **Lines**: Power lines can be drawn between buses, with an optional arrowhead indicating direction.
- **Loads**: Load components can be added to the system, each with an editable power consumption value.
- **Sources**: Power sources (e.g., generators) can be added, each with adjustable voltage and power outputs (active and reactive).
- **Dynamic Updates**: Moving buses, sources, or loads will automatically update connections, such as lines, accordingly.
- **Graphical Interface**: A graphical interface to interact with the power system components and modify their properties dynamically.

## Installation

To get started with this project, you need to have Python 3.6 or higher installed. Follow these steps to install the necessary dependencies and run the application:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/power-system-visualization.git
    cd power-system-visualization
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python main.py
    ```

## Usage

### Interacting with the System:

- **Adding Components**: You can add components such as buses, sources, and loads to the scene by clicking on the canvas.
- **Editing Component Properties**: 
    - Double-click on a bus, load, or source to edit its properties.
    - For buses and sources, you can edit properties like voltage. For loads, you can adjust the power consumption.
- **Moving Components**: You can move components around the canvas by dragging them.
- **Connecting Components**: Draw lines between buses, loads, and sources to connect them.

### Key Classes:

- **Bus**: A bus is a point in the system where components (like sources, loads, and lines) are connected. You can modify its voltage and see how it affects the connected components.
- **Line**: A line represents a power connection between two buses. It can optionally have an arrow indicating the direction of power flow.
- **Load**: A load consumes power. You can adjust the power consumption of a load via a dialog.
- **Source**: A power source (e.g., generator). You can adjust its voltage, real power, and reactive power.

## Requirements

- Python 3.6 or higher
- PyQt6
- (Other dependencies listed in `requirements.txt`)

## Contributing

Contributions are welcome! If you would like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request. 

### Steps for contributing:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- PyQt6: Used for the graphical user interface.
- Qt: For providing the foundation for graphical user interface components.
"# Input GUI" 
"# Input-GUI" 
