import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import shutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


import tempfile


def load_data():
    """
    Load data from the CSV file.
    """
    if not filename:
        tk.messagebox.showerror("Error", "No file selected")
        return None
    return pd.read_csv(filename, sep='  ', engine='python')


def create_histogram(df, window):
    figure = plt.Figure(figsize=(6, 5), dpi=100)
    ax = figure.add_subplot(111)

    # Scale the data from the second column (index 1)
    scaled_data = df.iloc[:, 1] * 10**9
    scaled_data.plot(kind='hist', ax=ax)
    ax.set_ylabel('Count')
    ax.set_xlabel('Charge [nC]')

    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Adding the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas._tkcanvas.pack()



def on_button_click():
    # Only proceed if file and inputs are valid
    if filename and entry1_1.get() and entry1_2.get() and entry1_3.get() and entry2.get() and entry3.get() and entry4.get():
        df = load_data()
        if df is None:
            return

        runname = "Run"
        begshot = int(entry2.get()) - 1
        endshot = int(entry3.get())

        # Average charge from entry1_2 to entry1_3
        beg_index = int(entry1_2.get()) - 1
        end_index = int(entry1_3.get())
        avg_charge = df.iloc[beg_index:end_index, 1].mean() * 10**9
        print(f'Average Charge On OSL: {avg_charge}')

        df1 = df.iloc[begshot:endshot]
        df1.to_csv(runname + 'int.txt', index=False)

        # New OSL Dose calculation
        osl_dose = round(float(entry1_1.get()) / avg_charge, 2)
        print(f'OSL Dose: {osl_dose}')

        # Material multiplier
        material = combo.get()
        if material == "Quartz":
            multiplier = 0.97
        elif material == "Plastic":
            multiplier = 0.8
        elif material == "Electronics":
            multiplier = 0.5
        else:
            tk.messagebox.showerror(title="Invalid material", message="Please select a material.")
            return

        print(f'Material Multiplier: {multiplier}')
        result = round((int(entry4.get()) * osl_dose * multiplier * avg_charge) / 1000000, 2)

        # Create new window for the result and the histogram
        new_window = tk.Toplevel(root)
        new_window.title("Dose and Charge Histogram")

        # Display result and other details
        result_label = tk.Label(new_window, text=f"Dose: {result} [Mrad]\nMaterial: {material}\nStart Shot: {begshot + 1}\nEnd Shot: {endshot}\n# Pulses: {entry4.get()}\nDose on OSL: {osl_dose} [rad/nC]\nFile Name: {filename}")
        result_label.pack()

        # Use the new create_histogram function
        create_histogram(df1, new_window)





def on_button_click2():
    # Only proceed if file and entry2 and entry3 inputs are valid
    if filename and entry2.get() and entry3.get():
        df = load_data()  # Use the modular load_data function
        if df is None:
            return

        runname = "Run"
        begshot = int(entry2.get()) - 1
        endshot = int(entry3.get()) 

        df1 = df.iloc[begshot:endshot]
        df1.to_csv(runname + 'int.txt', index=False)

        # Create new window for the result and the histogram
        new_window = tk.Toplevel(root)
        new_window.title("Dose and Charge Histogram")

        # Use the new create_histogram function
        scaled_data = create_histogram(df1, new_window)

        # Calculate statistics using the scaled data
        mean = scaled_data.mean()
        std_dev = scaled_data.std()
        total_entries = len(scaled_data)
        
        # Add statistics text to histogram
        stats_text = f"Mean: {mean:.2f} \nStd Dev: {std_dev:.2f}  \nTotal Entries: {total_entries}"
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax = scaled_data.plot(kind='hist').axes  # Get the axes from the plot
        ax.text(0.85, 1.13, stats_text, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)
        ax.set_ylabel('Count')
        ax.set_xlabel('Charge [nC]')


def choose_file():
    global filename
    filename = filedialog.askopenfilename()
    # Check if selected file is a '.meas' or '.txt' file
    if filename.endswith('.meas') or filename.endswith('.txt'):
        temp_dir = tempfile.gettempdir()  # returns the location of temporary directory
        shutil.copy(filename, temp_dir)  # copies the file to the temp directory
        file_label.config(text=filename)  # update label with selected file path
    else:
        # Show error if file is not of the expected type
        tk.messagebox.showerror(title="Invalid file", message="Please select a '.meas' or '.txt' file.")

root = tk.Tk()

filename = ''  # Initialize filename

root.title("Dose Calculator")

label3 = tk.Label(root, text="Select file")
label3.grid(row=0, column=0)
file_button = tk.Button(root, text="Browse", command=choose_file)
file_button.grid(row=1, column=0)
file_label = tk.Label(root, text="")
file_label.grid(row=2, column=0)

label1 = tk.Label(root, text="OSL [Dose rad/#] [Start] [End]")
label1.grid(row=0, column=1)
# Create a frame to hold the three entry boxes
entry_frame = tk.Frame(root)
entry_frame.grid(row=1, column=1)

# Create the three entry boxes
entry1_1 = tk.Entry(entry_frame, width=10)
entry1_1.pack(side="left")

entry1_2 = tk.Entry(entry_frame, width=10)
entry1_2.pack(side="left")

entry1_3 = tk.Entry(entry_frame, width=10)
entry1_3.pack(side="left")


label6 = tk.Label(root, text="# Pulses")
label6.grid(row=0, column=2)
entry4 = tk.Entry(root)
entry4.grid(row=1, column=2)

label2 = tk.Label(root, text="Start Shot")
label2.grid(row=3, column=0)
entry2 = tk.Entry(root)
entry2.grid(row=4, column=0)

label4 = tk.Label(root, text="End Shot")
label4.grid(row=3, column=1)
entry3 = tk.Entry(root)
entry3.grid(row=4, column=1)

label5 = tk.Label(root, text="Material")
label5.grid(row=3, column=2)
combo = ttk.Combobox(root)
combo['values'] = ("Quartz", "Plastic", "Electronics")
combo.grid(row=4, column=2)

button = tk.Button(root, text="Calculate Dose", command=on_button_click)
button.grid(row=5, column=1)  # span across 3 columns

button2 = tk.Button(root, text="Histogram", command=on_button_click2)
button2.grid(row=5, column=2)  # span across 3 columns

root.mainloop()