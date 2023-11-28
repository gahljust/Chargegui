# Charge GUI

This application is designed to calculate doses for various materials and visualize charge data using histograms. It is built with Python using the Tkinter framework for the GUI, Pandas for data manipulation, and Matplotlib for plotting histograms.

## Features

- **Data Loading**: Load `int.meas` or `int.txt` files containing charge data.
- **Dose Calculation**: Calculate doses based on user inputs and file data.
- **Data Visualization**: Generate interactive histograms to represent charge distributions.
- **Statistical Analysis**: Display basic statistics like mean, standard deviation, and total entries on histograms.

## Installation

To run this application, you need Python installed on your system. Clone or download this repository to your local machine.

### Dependencies

- Python 3.x
- Pandas
- Matplotlib
- Tkinter (usually included with Python)

Install the required packages using pip:

```bash
pip install pandas matplotlib
```

## Usage

1. **Start the Application**: Run the script to open the GUI.
2. **Load Data**: Click 'Browse' to select and load a `int.meas` or `int.txt` file.
3. **Set Parameters**: Enter the required parameters for OSL dose calculation including the estimated dose from th OSLs, the shot numbers for the OSLs, and the total number of shots for the OSLs, in the first row entry boxes. Then on the bottom row enter the shot numbers for the material you want to calculate the dose in, and finally choose the type of material in the dropdown menu on the bottom right.
4. **Calculate Dose**: Click 'Calculate Dose' to perform the calculation and display the results.
5. **Visualize Data**: Click 'Histogram' to generate and view an interactive histogram of the charge data.


