"""

Author: Hamed Gharghi
Date: 8/2/2024
Description: This script provides a PyQt5-based application to visualize 3D surface plots using Plotly.
             Users can select a data file, set axis titles, and view the plot in a browser window.
             It supports data files in CSV or TXT format and allows for saving the plot as an image from the browser.
"""

import sys
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QIcon

class PlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set Fusion style
        QApplication.setStyle('Fusion')

        self.setWindowTitle('Surface Plot 3D')
        self.setGeometry(100, 100, 350, 250)  # Adjusted window size
        self.setWindowIcon(QIcon('icon.png'))

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel('No file selected')
        self.file_button = QPushButton('Browse')
        self.file_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_button)
        main_layout.addLayout(file_layout)

        # Show example data format button
        example_button = QPushButton('Show Example Data Format')
        example_button.clicked.connect(self.show_example_format)
        main_layout.addWidget(example_button)

        # X-axis title
        x_layout = QHBoxLayout()
        x_title_label = QLabel("X-axis Title:")
        self.x_title_edit = QLineEdit(self)
        self.x_title_edit.setPlaceholderText("X-axis title")

        x_layout.addWidget(x_title_label)
        x_layout.addWidget(self.x_title_edit)
        main_layout.addLayout(x_layout)

        # Y-axis title
        y_layout = QHBoxLayout()
        y_title_label = QLabel("Y-axis Title:")
        self.y_title_edit = QLineEdit(self)
        self.y_title_edit.setPlaceholderText("Y-axis title")

        y_layout.addWidget(y_title_label)
        y_layout.addWidget(self.y_title_edit)
        main_layout.addLayout(y_layout)

        # Z-axis title
        z_layout = QHBoxLayout()
        z_title_label = QLabel("Z-axis Title:")
        self.z_title_edit = QLineEdit(self)
        self.z_title_edit.setPlaceholderText("Z-axis title")

        z_layout.addWidget(z_title_label)
        z_layout.addWidget(self.z_title_edit)
        main_layout.addLayout(z_layout)

        # Plot button
        self.plot_button = QPushButton('Show Plot')
        self.plot_button.clicked.connect(self.plot_data)
        main_layout.addWidget(self.plot_button)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Apply Slate Gray theme stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #2F4F4F;  /* Slate gray background */
                color: #F5F5F5;  /* Very light gray text color */
            }
            QLabel {
                color: #F5F5F5;  /* Very light gray text color */
            }
            QLineEdit {
                background-color: #2F4F4F;  /* Slate gray input background */
                color: #F5F5F5;  /* Very light gray text color */
                border: 1px solid #708090;  /* Slate gray border */
                padding: 5px;
            }
            QPushButton {
                background-color: #708090;  /* Slate gray button background */
                color: #F5F5F5;  /* Very light gray button text */
                border: 1px solid #4682B4;  /* Steel blue border */
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4682B4;  /* Steel blue button on hover */
            }
            QPushButton:pressed {
                background-color: #4169E1;  /* Royal blue on press */
            }
        """)

    def browse_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Data File", "", "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.file_label.setText(file_name)
            self.data_file = file_name

    def show_example_format(self):
        example_text = (
            "Example Data Format:\n\n"
            "X,Y,Z\n"
            "0,0,0\n"
            "0,1,1\n"
            "0,2,4\n"
            "1,0,1\n"
            "1,1,2\n"
            "1,2,5\n"
            "2,0,4\n"
            "2,1,5\n"
            "2,2,6\n\n"
            "Ensure that your data file contains columns X, Y, and Z with each row representing a grid point. The data should be in CSV or TXT format."
        )
        QMessageBox.information(self, "Example Data Format", example_text)

    def plot_data(self):
        if not hasattr(self, 'data_file') or not self.data_file:
            QMessageBox.warning(self, "Error", "No data file selected. Please select a file before plotting.")
            return

        try:
            # Load data
            data = pd.read_csv(self.data_file, delimiter=',')
            x = data['X'].values
            y = data['Y'].values
            z = data['Z'].values

            # Check if data is suitable for 3D surface plot
            if len(x) != len(y) or len(y) != len(z):
                QMessageBox.warning(self, "Error", "Data length mismatch. Ensure that X, Y, and Z values have the same length.")
                return

            # Reshape data
            grid_size = int(len(x) ** 0.5)  # Assuming a square grid
            if grid_size ** 2 != len(x):
                QMessageBox.warning(self, "Error", "Data cannot be reshaped into a grid. Ensure the data is in a square grid format.")
                return

            x = x.reshape((grid_size, grid_size))
            y = y.reshape((grid_size, grid_size))
            z = z.reshape((grid_size, grid_size))

            # Create the 3D surface plot
            fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Viridis', showscale=True)])

            # Update layout with titles
            fig.update_layout(
                title="3D Surface Plot",
                scene=dict(
                    xaxis_title=self.x_title_edit.text(),
                    yaxis_title=self.y_title_edit.text(),
                    zaxis_title=self.z_title_edit.text(),
                )
            )

            # Show the plot in a new browser window (offline mode)
            pio.show(fig, validate=False)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while plotting data: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plotter = PlotApp()
    plotter.show()
    sys.exit(app.exec_())
