import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def signal_representation():
    try:

        # Clear the main window to display the new page
        for widget in root.winfo_children():
            widget.destroy()

 
        # Read signal data from the file
        with open(r'C:\\Users\\96650\\Desktop\\Signals-20241011T095133Z-001\\Signals\\signal1.txt', 'r') as f:
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
    sine_cosine_button = tk.Button(root, text="Sine/Cosine Representation", command=sine_cosine_generation)
    sine_cosine_button.pack(pady=10)

    # Back Button to go to the Main Menu
    back_button = tk.Button(root, text="Back", command=main_menu)
    back_button.pack(pady=20)

def sine_cosine_generation():
    # Create the main window
    rep_window = tk.Tk()
    rep_window.title("Signal Representation")
    rep_window.geometry("700x700")
    
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

            # Time array based on the sampling frequency
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
            ax.set_ylim(-amplitude * 1.5, amplitude * 1.5)  # Adjust y-limits based on amplitude
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
    # Time array based on the sampling frequency and duration
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

def validate():
    ind, samp, t = generate_signal("sin", 3, 1.96349540849362, 360, 720)
    print("sine " + SignalSamplesAreEqual("D:/uni/DSP/DSP_tasks/SinOutput.txt", ind, samp))
    ind, samp, t = generate_signal("cos", 3, 2.35619449019235, 200, 500)
    print("cosine " + SignalSamplesAreEqual("D:/uni/DSP/DSP_tasks/CosOutput.txt", ind, samp))

# Main window properties
root = tk.Tk()
root.title("Tasks")
root.geometry("900x600")  # Adjusted size to fit everything properly

task_1_button = tk.Button(root, text="Task 1", command=task1_sub_tasks)
task_1_button.pack(pady=20)

root.mainloop()
####sssssss
