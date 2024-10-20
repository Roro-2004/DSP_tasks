import numpy as np
import matplotlib.pyplot as plt
from tkinter import Button, Label, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox


def read_signal_file(file_path):
    try:
        # Use np.loadtxt with usecols to select only the second column (signal values) and skip the first two rows
        data = np.loadtxt(file_path, skiprows=3, usecols=1)  # Skipping the first 2 rows and selecting column 1 (signal values)
        return data
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {e}")

def signal_representation():
    try:

        # Clear the main window to display the new page
        for widget in root.winfo_children():
            widget.destroy()

 
        # Read signal data from the file
        with open(r'D:\\uni\\DSP\\DSP_tasks\\task1\\signal1.txt', 'r') as f:
            for _ in range(3):  # Skip the first 3 lines
                next(f)
            time = []
            amplitude = []
            for line in f:
                time.append(float(line.split()[0]))
                amplitude.append(float(line.split()[1]))

        # Create a figure with two subplots (side-by-side)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Discrete representation
        ax1.stem(time, amplitude, basefmt='k')
        ax1.set_title('Discrete Representation')
        ax1.set_xlabel('Sample')
        ax1.set_ylabel('Amplitude')
        ax1.grid(True)

        # Continuous representation
        ax2.plot(time, amplitude)
        ax2.set_title('Continuous Representation')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Amplitude')
        ax2.grid(True)

        # Embed the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        # Back Button to return to the Task 1 Sub Tasks menu
        back_button = tk.Button(root, text="Back", command=task1_sub_tasks)
        back_button.pack(pady=20)

    except FileNotFoundError:
        print("Error: The specified file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def task1_sub_tasks():
    # Clear the main window for the task buttons
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Task 1 Sub Tasks")

    # Signal Representation Button
    signal_button = tk.Button(root, text="Signal Representation", command=signal_representation)
    signal_button.pack(pady=10)

    # Sine/Cosine Representation Button (for later use)
    sine_cosine_button = tk.Button(root, text="Sine/Cosine Representation", command=sine_cosine_generation_menue)
    sine_cosine_button.pack(pady=10)

    add_button = tk.Button(root, text="add 2 signals", command=add)
    add_button.pack(pady=10)

    sub_button = tk.Button(root, text="subtract 2 signals", command=sub)
    sub_button.pack(pady=10)

    button4 = tk.Button(root, text="normalize signals", command=normalize)
    button4.pack(pady=10)

def sine_cosine_generation_menue():
    # Create the main window
    rep_window = tk.Tk()
    rep_window.title("Sine/cos Representation")
    rep_window.geometry("700x700")
    rep_window.config(background="lightblue")
    frame = ttk.Frame(rep_window, padding="20")
    frame.grid(row=0, column=0, padx=10, pady=10)
    # Signal type label and dropdown
    ttk.Label(frame, text="Select Signal Type:").grid(row=0, column=0, sticky=tk.W)
    signal_type = ttk.Combobox(frame, values=["sin", "cos"], state="readonly")
    signal_type.grid(row=0, column=1, padx=5, pady=5)
    signal_type.set("sin")  # Default selection
    # Input fields for parameters
    ttk.Label(frame, text="Amplitude:").grid(row=1, column=0, sticky=tk.W)
    amplitude_entry = ttk.Entry(frame)
    amplitude_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Analog Frequency:").grid(row=2, column=0, sticky=tk.W)
    analog_freq_entry = ttk.Entry(frame)
    analog_freq_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Sampling Frequency:").grid(row=3, column=0, sticky=tk.W)
    sampling_freq_entry = ttk.Entry(frame)
    sampling_freq_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Phase Shift:").grid(row=4, column=0, sticky=tk.W)
    phase_shift_entry = ttk.Entry(frame)
    phase_shift_entry.grid(row=4, column=1, padx=5, pady=5)

    fig, ax = plt.subplots(figsize=(5, 4))
    canvas = FigureCanvasTkAgg(fig, master=rep_window)  # Embedding figure in Tkinter window
    canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)

    # Flags to track which signals have been plotted
    sine_plotted = False
    cosine_plotted = False

    # Function to plot signals based on user selection
    def plot_signals():
        nonlocal sine_plotted, cosine_plotted

        try:
            amplitude = float(amplitude_entry.get())
            analog_freq = float(analog_freq_entry.get())
            sampling_freq = float(sampling_freq_entry.get())
            phase_shift = float(phase_shift_entry.get())
            selected_signal = signal_type.get()

            if sampling_freq < 2 * analog_freq:
                print("Sampling frequency must be at least 2 times the analog frequency.")
                return

            
            t = np.arange(0.0, 1.0, 1.0 / sampling_freq)

            if selected_signal == "sin" and not sine_plotted:
                # Generate sine wave
                sine_samples = amplitude * np.sin(2 * np.pi * analog_freq * t + (phase_shift))
                ax.plot(t, sine_samples, label='Sine Signal', color='blue', linewidth=2)
                sine_plotted = True  # Mark sine wave as plotted

            if selected_signal == "cos" and not cosine_plotted:
                # Generate cosine wave
                cosine_samples = amplitude * np.cos(2 * np.pi * analog_freq * t + (phase_shift))
                ax.plot(t, cosine_samples, label='Cosine Signal', color='red', linewidth=2)
                cosine_plotted = True  # Mark cosine wave as plotted

            # Set limits for x and y axes
            ax.set_xlim(0,  0.01 )  # Display the first 0.01 seconds
            #ax.set_ylim(-amplitude * 1.5, amplitude * 1.5)  # Adjust y-limits based on amplitude
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude')
            ax.set_title('Sine and Cosine Signals')
            ax.grid(True)
           

            # Draw the canvas
            canvas.draw()

        except ValueError as ve:
            print(f"Please enter valid numbers for all fields. Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # Create plot button and attach command
    plot_button = ttk.Button(frame, text="Plot Signals", command=plot_signals)
    plot_button.grid(row=5, column=1, pady=15, padx=5)

    # Start the main loop
    rep_window.mainloop()


# Define the signal generation function
def generate_signal(signal_type, amplitude, phase_shift, analog_freq, sampling_freq):
    
    t = np.arange(0.0, 1.0, 1.0 / sampling_freq)
    # Generate sine or cosine signal
    if signal_type == 'sin':
        samples = amplitude * np.sin(2 * np.pi * analog_freq * t + phase_shift)
    elif signal_type == 'cos':
        samples = amplitude * np.cos(2 * np.pi * analog_freq * t + phase_shift)
    else:
        raise ValueError("Invalid signal type. Choose 'sine' or 'cosine'.")

    # Indices (discrete time steps)
    indices = np.arange(len(t))
    return indices, samples, t

# Sample validation function (for demonstration purposes)
def SignalSamplesAreEqual(file_name, indices, samples):
    expected_indices = []
    expected_samples = []
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            L = line.strip()
            if len(L.split(' ')) == 2:
                L = line.split(' ')
                V1 = int(L[0])
                V2 = float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
                
    if len(expected_samples) != len(samples):
        return "Test case failed, your signal has different length from the expected one"
        
    for i in range(len(expected_samples)):
        if abs(samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            return "Test case failed, your signal has different values from the expected one"
    return "Test case passed successfully"

def sine_cos_validate():
    rep_window = tk.Tk()
    rep_window.title("sine / cosine veridect")
    rep_window.geometry("700x700")
     # Generate and validate the sine signal
    ind, samp, t = generate_signal("sin", 3, 1.96349540849362, 360, 720)
    sine_validation = "sine: " + SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task1\\SinOutput.txt", ind, samp)
    
    # Display the sine result on the same page
    label_sine = tk.Label(rep_window, text=sine_validation, font=('Arial', 14))
    label_sine.pack(pady=10)  # Adjust the padding as needed
    
    # Print the sine validation result
    print(sine_validation)

    # Generate and validate the cosine signal
    ind, samp, t = generate_signal("cos", 3, 2.35619449019235, 200, 500)
    cosine_validation = "cosine: " + SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task1\\CosOutput.txt", ind, samp)
    
    # Display the cosine result on the same page
    label_cosine = tk.Label(rep_window, text=cosine_validation, font=('Arial', 14))
    label_cosine.pack(pady=10)  # Adjust the padding as needed
    
    # Print the cosine validation result
    print(cosine_validation)
def add_validation():
    rep_window = tk.Tk()
    rep_window.title("add veridect veridect")
    rep_window.geometry("700x700")
    ind, samples = add()
    txt = "signal 1 + signal 2 "+ SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task2\\Signal1+signal2.txt",ind, samples )
    label_signal1_signal2= tk.Label(rep_window, text=txt, font=('Arial', 14))
    label_signal1_signal2.pack(pady=10)  # Adjust the padding as needed
    ind, samples = add()
    txt = "signal 1 + signal 3 "+ SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task2\\Signal1+signal3.txt",ind, samples )
    label_signal1_signal2= tk.Label(rep_window, text=txt, font=('Arial', 14))
    label_signal1_signal2.pack(pady=10)  # Adjust the padding as needed
def add():
    try:
        # Select the first file
        file1 = filedialog.askopenfilename(title="Select First Signal File", filetypes=[("Text Files", "*.txt")])
        if not file1:
            raise ValueError("No file selected for Signal 1.")

        # Select the second file
        file2 = filedialog.askopenfilename(title="Select Second Signal File", filetypes=[("Text Files", "*.txt")])
        if not file2:
            raise ValueError("No file selected for Signal 2.")

        # Read the signal values from both files
        signal1 = read_signal_file(file1)
        signal2 = read_signal_file(file2)

        # Ensure both signals have the same length
        if len(signal1) != len(signal2):
            raise ValueError("The two signals must have the same length.")

        # Add the signals together
        result_signal = signal1 + signal2
        index = np.arange(len(result_signal))  # Create an index array for plotting

        # Plot the result
        plt.figure(figsize=(10, 6))
        plt.plot(index, signal1, label='Signal 1')
        plt.plot(index, signal2, label='Signal 2')
        plt.plot(index, result_signal, label='Resulting Signal', linewidth=3, color='black')
        plt.title("Added Signals")
        plt.xlabel("Index")
        plt.ylabel("Signal Value")
        plt.legend()
        plt.grid(True)
        plt.show()

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    return index, result_signal
def sub():
    try:
        # Select the first file
        file1 = filedialog.askopenfilename(title="Select First Signal File", filetypes=[("Text Files", "*.txt")])
        if not file1:
            raise ValueError("No file selected for Signal 1.")

        # Select the second file
        file2 = filedialog.askopenfilename(title="Select Second Signal File", filetypes=[("Text Files", "*.txt")])
        if not file2:
            raise ValueError("No file selected for Signal 2.")

        # Read the signal values from both files
        signal1 = read_signal_file(file1)
        signal2 = read_signal_file(file2)

        # Ensure both signals have the same length
        if len(signal1) != len(signal2):
            raise ValueError("The two signals must have the same length.")

        # Subtract the signals
        result_signal = signal2 - signal1
        index = np.arange(len(result_signal))  # Create an index array for plotting

        # Plot the result
        plt.figure(figsize=(10, 6))
        plt.plot(index, signal1, label='Signal 1')
        plt.plot(index, signal2, label='Signal 2')
        plt.plot(index, result_signal, label='Resulting Signal (Signal 1 - Signal 2)', linewidth=3, color='black')
        plt.title("Subtracted Signals")
        plt.xlabel("Index")
        plt.ylabel("Signal Value")
        plt.legend()
        plt.grid(True)
        plt.show()

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    
    return index, result_signal

def sub_validation():
    rep_window = tk.Tk()
    rep_window.title("add veridect veridect")
    rep_window.geometry("700x700")
    ind, samples = sub()
    txt = "signal 1 - signal 2 "+ SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task2\\signal1-signal2.txt",ind, samples )
    label_signal1_signal2= tk.Label(rep_window, text=txt, font=('Arial', 14))
    label_signal1_signal2.pack(pady=10)  # Adjust the padding as needed
    ind, samples = sub()
    txt = "signal 1 - signal 3 "+ SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task2\\signal1-signal3.txt",ind, samples )
    label_signal1_signal2= tk.Label(rep_window, text=txt, font=('Arial', 14))
    label_signal1_signal2.pack(pady=10)  # Adjust the padding as needed
def normalize_validation():
    rep_window = tk.Tk()
    rep_window.title("normalize  veridect")
    rep_window.geometry("700x700")
    ind, samples = normalize()
    txt = "signal 1 normalized "+ SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task2\\normalize of signal 1 (from -1 to 1)-- output.txt",ind, samples )
    label_signal1_signal2= tk.Label(rep_window, text=txt, font=('Arial', 14))
    label_signal1_signal2.pack(pady=10)  # Adjust the padding as needed
    ind, samples = normalize()
    txt = "signal 2  normalized"+ SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task2\\normlize signal 2 (from 0 to 1 )-- output.txt",ind, samples )
    label_signal1_signal2= tk.Label(rep_window, text=txt, font=('Arial', 14))
    label_signal1_signal2.pack(pady=10)  # Adjust the padding as needed
def normalize():
    def on_submit():
        try:
            # Get the selected range type from the combobox
            range_type = combobox.get()
            if range_type not in ["[-1, 1]", "[0, 1]"]:
                raise ValueError("Please select a valid normalization range.")
            
            # Select the signal file
            file1 = filedialog.askopenfilename(title="Select Signal File", filetypes=[("Text Files", "*.txt")])
            if not file1:
                raise ValueError("No file selected for the signal.")
            
            # Read the signal from the file
            signal = read_signal_file(file1)
            min_val = np.min(signal)
            max_val = np.max(signal)

            # Normalize the signal based on the chosen range
            if range_type == "[-1, 1]":
                normalized_signal = 2 * (signal - min_val) / (max_val - min_val) - 1
            elif range_type == "[0, 1]":
                normalized_signal = (signal - min_val) / (max_val - min_val)
            else:
                raise ValueError("Invalid range_type. Choose '[-1, 1]' or '[0, 1]'.")

            # Create an index array for plotting
            index = np.arange(len(signal))

            # Plot the normalized signal
            plt.figure(figsize=(10, 6))
            plt.plot(index, normalized_signal, label='Normalized Signal', linewidth=3, color='black')
            plt.title(f"Normalized Signal (Range: {range_type})")
            plt.xlabel("Index")
            plt.ylabel("Signal Value")
            plt.legend()
            plt.grid(True)
            plt.show()
            if range_type =="[-1, 1]":
                print("signal 1 "+ SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task2\\normalize of signal 1 (from -1 to 1)-- output.txt", index, normalized_signal))
            else:
                print("signal 2  normalized"+ SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task2\\normlize signal 2 (from 0 to 1 )-- output.txt",index, normalized_signal))
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create a label and a combobox for the user to select the range
    label = Label(root, text="Select Normalization Range", font=("Arial", 14))
    label.pack(pady=10)

    combobox = Combobox(root, values=["[-1, 1]", "[0, 1]"], font=("Arial", 12))
    combobox.set("[-1, 1]")  # Set default value
    combobox.pack(pady=10)

    # Create a submit button
    submit_button = Button(root, text="Submit", font=("Arial", 14), bg="lightblue", command=on_submit)
    submit_button.pack(pady=20)

def menue():
     rep_window = tk.Tk()
     rep_window.title("validation menue")
     rep_window.geometry("700x700")
     button1 = tk.Button(rep_window, text="sin/cosine validation", command=sine_cos_validate)
     button1.pack(pady=10)
     button2 = tk.Button(rep_window, text="add signals", command=add_validation)
     button2.pack(pady=10)
     button3 = tk.Button(rep_window, text="subtract signals", command=sub_validation)
     button3.pack(pady=10)
     button4 = tk.Button(rep_window, text="normalize signals", command=normalize_validation)
     button4.pack(pady=10)

# Main window properties
root = tk.Tk()
root.title("Tasks")
root.geometry("900x600")  # Adjusted size to fit everything properly

task_1_button = tk.Button(root, text="main menue", command=task1_sub_tasks)
task_1_button.pack(pady=20)

task_2_button = tk.Button(root, text="validate", command=menue)
task_2_button.pack(pady=20)
root.config(background='lightblue')
root.mainloop()
####sssssss
