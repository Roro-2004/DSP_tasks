import numpy as np
import matplotlib.pyplot as plt
from tkinter import Button, IntVar, Label, Radiobutton, simpledialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox


Fs = 4000  # 4 kHz
X = []  # Global variable to store DFT complex values

def read_signal_file(file_path):
    try:
        data = np.loadtxt(file_path, skiprows=3, usecols=1)  
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

    
    button7 = tk.Button(root, text="quant signals", command=open_choice_menu)
    button7.pack(pady=10)
    button8 = tk.Button(root, text="correlation", command=test_normalized_cross_correlation)
    button8.pack(pady=10)
    button8 = tk.Button(root, text="remove dc in time domain", command=compute_and_compare_with_dc_removal)
    button8.pack(pady=10)
    button8 = tk.Button(root, text="remove dc in freq domain", command=compute_and_compare_with_dc_removall)
    button8.pack(pady=10)
    button8 = tk.Button(root, text="smoothing", command=compute_moving_average)
    button8.pack(pady=10)
    button8 = tk.Button(root, text="convolution", command=convolution)
    button8.pack(pady=10)
    
    
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
    label_signal1_signal2.pack(pady=10)  
    ind, samples = add()
    txt = "signal 1 + signal 3 "+ SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task2\\Signal1+signal3.txt",ind, samples )
    label_signal1_signal2= tk.Label(rep_window, text=txt, font=('Arial', 14))
    label_signal1_signal2.pack(pady=10)  
def add():
    try:

        file1 = filedialog.askopenfilename(title="Select First Signal File", filetypes=[("Text Files", "*.txt")])
        if not file1:
            raise ValueError("No file selected for Signal 1.")

        
        file2 = filedialog.askopenfilename(title="Select Second Signal File", filetypes=[("Text Files", "*.txt")])
        if not file2:
            raise ValueError("No file selected for Signal 2.")

    
        signal1 = read_signal_file(file1)
        signal2 = read_signal_file(file2)

        
        if len(signal1) != len(signal2):
            raise ValueError("The two signals must have the same length.")

        
        result_signal = signal1 + signal2
        index = np.arange(len(result_signal))  

        
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
        
        file1 = filedialog.askopenfilename(title="Select First Signal File", filetypes=[("Text Files", "*.txt")])
        if not file1:
            raise ValueError("No file selected for Signal 1.")

        
        file2 = filedialog.askopenfilename(title="Select Second Signal File", filetypes=[("Text Files", "*.txt")])
        if not file2:
            raise ValueError("No file selected for Signal 2.")

        
        signal1 = read_signal_file(file1)
        signal2 = read_signal_file(file2)

        
        if len(signal1) != len(signal2):
            raise ValueError("The two signals must have the same length.")

        
        result_signal = signal2 - signal1
        index = np.arange(len(result_signal))  

        
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
def normalize():
    def on_submit():
        try:
            
            range_type = combobox.get()
            if range_type not in ["[-1, 1]", "[0, 1]"]:
                raise ValueError("Please select a valid normalization range.")
            
            
            file1 = filedialog.askopenfilename(title="Select Signal File", filetypes=[("Text Files", "*.txt")])
            if not file1:
                raise ValueError("No file selected for the signal.")
            
            
            signal = read_signal_file(file1)
            min_val = np.min(signal)
            max_val = np.max(signal)

        
            if range_type == "[-1, 1]":
                normalized_signal = 2 * (signal - min_val) / (max_val - min_val) - 1
            elif range_type == "[0, 1]":
                normalized_signal = (signal - min_val) / (max_val - min_val)
            else:
                raise ValueError("Invalid range_type. Choose '[-1, 1]' or '[0, 1]'.")

            
            index = np.arange(len(signal))

            
            plt.figure(figsize=(10, 6))
            plt.plot(index, normalized_signal, label='Normalized Signal', linewidth=3, color='black')
            plt.title(f"Normalized Signal (Range: {range_type})")
            plt.xlabel("Index")
            plt.ylabel("Signal Value")
            plt.legend()
            plt.grid(True)
            plt.show()
            if range_type =="[-1, 1]":
                print("signal 1 normalized"+ SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task2\\normalize of signal 1 (from -1 to 1)-- output.txt", index, normalized_signal))
            else:
                print("signal 2  normalized"+ SignalSamplesAreEqual("D:\\uni\\DSP\\DSP_tasks\\task2\\normlize signal 2 (from 0 to 1 )-- output.txt",index, normalized_signal))
        except ValueError as e:
            messagebox.showerror("Error", str(e))


    for widget in root.winfo_children():
        widget.destroy()
    
    label = Label(root, text="Select Normalization Range", font=("Arial", 14))
    label.pack(pady=10)

    combobox = Combobox(root, values=["[-1, 1]", "[0, 1]"], font=("Arial", 12))
    combobox.set("[-1, 1]")  
    combobox.pack(pady=10)

    
    submit_button = Button(root, text="Submit", font=("Arial", 14), bg="lightblue", command=on_submit)
    submit_button.pack(pady=20)
def browse_and_read_signal_file():
    
    try:
        file_path = filedialog.askopenfilename(
            title="Select Signal File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )

        if not file_path:
            messagebox.showinfo("No File Selected", "Please select a valid file.")
            return None, None  

        
        with open(file_path, 'r') as f:
            for _ in range(3):  
                next(f)
            time, amplitude = [], []
            for line in f:
                t, a = map(float, line.split())
                time.append(t)
                amplitude.append(a)

        return np.array(time), np.array(amplitude)  

    except FileNotFoundError:
        messagebox.showerror("Error", "The specified file was not found.")
        return None, None
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return None, None
    

    
def accumulate_signal():
    try:
       
        for widget in root.winfo_children():
            widget.destroy()

        
        time, amplitude = browse_and_read_signal_file()

        
        time = np.array(time, dtype=np.float64)
        amplitude = np.array(amplitude, dtype=np.float64)

    
        modified_amplitude = []
        sum = 0  
        for value in amplitude:
            sum += value  
            modified_amplitude.append(sum) 

        
        modified_amplitude = np.array(modified_amplitude)

       
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Plot original signal
        ax1.plot(time, amplitude, label='Original Signal', color='blue')
        ax1.set_title('Original Signal')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Amplitude')
        ax1.grid(True)
        ax1.legend()

        # Plot accumulated signal
        ax2.plot(time, modified_amplitude, label='Accumulated Signal', color='green')
        ax2.set_title('Accumulated Signal')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Amplitude')
        ax2.grid(True)
        ax2.legend()

        # Embed the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        # Button to compare with an output file
        compare_button = tk.Button(
            root, text="Compare with Output File", 
            command=lambda: compare_signals(time, modified_amplitude)
        )
        compare_button.pack(pady=20)

        # Back Button to return to Task 1 Sub Tasks menu
        back_button = tk.Button(root, text="Back", command=task1_sub_tasks)
        back_button.pack(pady=20)

    except FileNotFoundError:
        messagebox.showerror("Error", "The specified file was not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def square_signal():
    try:
        
        for widget in root.winfo_children():
            widget.destroy()

        time, amplitude = browse_and_read_signal_file()

        amplitude = np.array(amplitude, dtype=np.float64)

        
        modified_amplitude = amplitude ** 2


    
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        
        ax1.plot(time, amplitude, label='Original Signal', color='blue')
        ax1.set_title('Original Signal')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Amplitude')
        ax1.grid(True)
        ax1.legend()

        
        ax2.plot(time, modified_amplitude, label='Squared Signal', color='green')
        ax2.set_title('Squared Signal')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Amplitude')
        ax2.grid(True)
        ax2.legend()

        
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        compare_button = tk.Button(root, text="Compare with Output File", command=lambda: compare_signals(time, modified_amplitude ))
        compare_button.pack(pady=20)

        
        back_button = tk.Button(root, text="Back", command=task1_sub_tasks)
        back_button.pack(pady=20)

    except FileNotFoundError:
        messagebox.showerror("Error", "The specified file was not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def multiply_signal():
    try:
        # Clear the main window to display the new page
        for widget in root.winfo_children():
            widget.destroy()

        time, amplitude = browse_and_read_signal_file()
        
    
        # Ask for the constant to multiply the signal
        constant = float(simpledialog.askstring("Input", "Enter a constant to multiply the signal by:"))

        # Modify the signal
        modified_amplitude = np.array(amplitude) * constant

        # Create a figure with two subplots (side-by-side)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Original signal
        ax1.plot(time, amplitude, label='Original Signal', color='blue')
        ax1.set_title('Original Signal')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Amplitude')
        ax1.grid(True)
        ax1.legend()

        # Modified signal
        ax2.plot(time, modified_amplitude, label='Modified Signal', color='red')
        ax2.set_title('Modified Signal')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Amplitude')
        ax2.grid(True)
        ax2.legend()

        # Embed the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        # Comparison Button to compare with output file
        compare_button = tk.Button(root, text="Compare with Output File", command=lambda: compare_signals(time, modified_amplitude))
        compare_button.pack(pady=20)

        # Back Button to return to Task 1 Sub Tasks menu
        back_button = tk.Button(root, text="Back", command=task1_sub_tasks)
        back_button.pack(pady=20)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for the constant.")
    except FileNotFoundError:
        messagebox.showerror("Error", "The specified file was not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def compare_signals(time, modified_amplitude):
    try:
        # File dialog to select the output file
        output_file_path = filedialog.askopenfilename(
            title="Select Output File", 
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )

        if not output_file_path:  # If no file is selected, return
            messagebox.showinfo("No File Selected", "Please select a valid output file.")
            return

        # Read the output signal data from the file
        with open(output_file_path, 'r') as f:
            for _ in range(3):  # Skip the first 3 lines
                next(f)
            output_amplitude = []
            for line in f:
                _, a = map(float, line.split())
                output_amplitude.append(a)

        # Compare the modified signal with the output signal
        discrepancies = sum(np.abs(np.array(modified_amplitude) - np.array(output_amplitude)) )

        if discrepancies == 0:
            messagebox.showinfo("Comparison Result", "The modified signal matches the output signal.")
        else:
            messagebox.showinfo("Comparison Result", f"The modified signal has {discrepancies} discrepancies with the output signal.")

    except FileNotFoundError:
        messagebox.showerror("Error", "The specified output file was not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
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
     button4 = tk.Button(rep_window, text="normalize signals", command=normalize)
     button4.pack(pady=10)
     button5 = tk.Button(rep_window, text="multiply signals", command=multiply_signal)
     button5.pack(pady=10)
     button6 = tk.Button(rep_window, text="square signals", command=square_signal)
     button6.pack(pady=10)
     button6 = tk.Button(rep_window, text="accumilate signals", command=accumulate_signal)
     button6.pack(pady=10)
     button7 = tk.Button(rep_window, text="quant signals", command=open_choice_menu)
     button7.pack(pady=10)
     dft_button = tk.Button(rep_window, text="DFT", command=calculate_dft_and_display)
     dft_button.pack(pady=10)
     idft_button = tk.Button(rep_window, text="IDFT", command=calculate_idft_and_display)
     idft_button.pack(pady=10)
     DCT_button = tk.Button(rep_window, text="DCT", command=calculate_dct_and_display)
     DCT_button.pack(pady=10)
     sharpening_button = tk.Button(rep_window, text="sharpning signal", command=DerivativeSignal)
     sharpening_button.pack(pady=10)
     folding_button = tk.Button(rep_window, text="folding signal", command=folding_signal)
     folding_button.pack(pady=10)
     button8 = tk.Button(rep_window, text="Shift fold Signal", command=process_signal)
     button8.pack(pady=10)


def folding_signal():
    """Handles the button click event for folding a signal."""
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        messagebox.showerror("Input Error", "Please select a signal file.")
        return

    # Read the signal from the file
    signal, indices = read_signal_with_indices_from_txt(file_path)  # Updated to return indices
    if signal is None or indices is None:
        messagebox.showerror("Error", "Could not read the signal from the file.")
        return

    # Perform the folding operation
    result_signal = fold_signal(signal)

    
    # Optional: Save the indices and folded signal to a file
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_path:
        with open(save_path, 'w') as file:
            file.write("Index, Folded Value\n")
            for idx, value in zip(indices, result_signal):
                file.write(f"{idx}, {int(value)}\n")
        messagebox.showinfo("Success", f"Folded signal saved to {save_path}")
        for value in result_signal:
            print(value)
    print(SignalSamplesAreEqual("c://Users//96650//Desktop//signals//Output_fold.txt",signal,result_signal))
    
def calculate_dct_and_display():
    # Let user select a signal file
    index, signal =browse_and_read_signal_file()

    # Ask user for the number of coefficients (m) to save
    m = simpledialog.askinteger("Input", "Enter the number of DCT coefficients to save:")
    if m is None or m <= 0:
        messagebox.showerror("Input Error", "Invalid number of coefficients.")
        return

    # Compute the DCT
    dct_coefficients = DCT(signal, m)

    # Save the first m coefficients to a new file
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not output_file:
        messagebox.showerror("File Error", "No output file selected.")
        return

    with open(output_file, "w") as f:
        f.write("0\n")  # Add header or meta information if needed
        f.write("1\n")
        f.write(f"{len(dct_coefficients)}\n")  # Write the number of coefficients (m)
        for index, coeff in enumerate(dct_coefficients):
            f.write(f"{index} {coeff:.6f}\n")

    # Display the result
    print("DCT Coefficients:")
    for index, coeff in enumerate(dct_coefficients):
        print(f"{index}: {coeff:.6f}")

    messagebox.showinfo("Success", f"DCT coefficients saved to {output_file}")

    # Compare the output file with the original signal
    print(SignalSamplesAreEqual("c://Users//96650//Desktop//signals//DCT_output.txt", range(len(dct_coefficients)), dct_coefficients))  # Compare output file with the DCT coefficients
def DCT(signal, m):
    N = len(signal)
    dct_coefficients = np.zeros(N)  # Initialize DCT coefficient array

    for k in range(N):  # k ranges from 1 to N
        summation = 0
        for n in range(N):  # n ranges from 1 to N
            summation += signal[n] * np.cos((np.pi / (4 * N)) * (2 * n - 1) * (2 * k - 1))
        dct_coefficients[k] = np.sqrt(2 / N) * summation

    # Save only the first m coefficients if specified
    if m is not None and m < N:
        dct_coefficients = dct_coefficients[:m]

    return dct_coefficients
def QuantizationTest1(file_name,Your_EncodedValues,Your_QuantizedValues):
    expectedEncodedValues=[]
    expectedQuantizedValues=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V2=str(L[0])
                V3=float(L[1])
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                line = f.readline()
            else:
                break
    if( (len(Your_EncodedValues)!=len(expectedEncodedValues)) or (len(Your_QuantizedValues)!=len(expectedQuantizedValues))):
        print("QuantizationTest1 Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_EncodedValues)):
        if(Your_EncodedValues[i]!=expectedEncodedValues[i]):
            print("QuantizationTest1 Test case failed, your EncodedValues have different EncodedValues from the expected one") 
            return
    for i in range(len(expectedQuantizedValues)):
        if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
            continue
        else:
            print("QuantizationTest1 Test case failed, your QuantizedValues have different values from the expected one") 
            return
    print("QuantizationTest1 Test case passed successfully")
def fold_signal(signal):
    n = len(signal)
    folded_signal = [0]*n

    for i in range(n):
        folded_signal[i] = signal[n - 1 - i]

    return folded_signal

def delay_or_advance_signal(signal, indices, k):
    """Delays or advances the signal by k steps."""
    n = len(signal)
    
    # If k is positive, delay the signal (shift right)
    if k > 0:
        shifted_signal = [0] * k + signal[:-k]  # Delay by k steps
        shifted_indices = indices[k:]  # Adjust indices for the delayed signal
    # If k is negative, advance the signal (shift left)
    elif k < 0:
        shifted_signal = signal[k:] + [0] * (-k)  # Advance by -k steps
        shifted_indices = indices[:k]  # Adjust indices for the advanced signal
    else:
        shifted_signal = signal  # No shift if k == 0
        shifted_indices = indices

    return shifted_indices, shifted_signal

def Shift_Fold_Signal(file_name,Your_indices,Your_samples):      
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    print("Current Output Test file is: ")
    print(file_name)
    print("\n")

    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Shift_Fold_Signal Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Shift_Fold_Signal Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Shift_Fold_Signal Test case failed, your signal have different values from the expected one") 
            return
    print("Shift_Fold_Signal Test case passed successfully")



def process_signal():
    """Handles the folding and shifting process."""
    # Ask for the value of k from the user
    k = simpledialog.askinteger("Input", "Enter the value of k (positive for delay, negative for advance):"  )
    if k is None:
        messagebox.showerror("Input Error", "No value entered for k.")
        return

    # Ask user to select a signal file
    input_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not input_file:
        messagebox.showerror("Error", "No input file selected.")
        return

    # Read the signal and indices from the file
    signal, indices = read_signal_with_indices_from_txt(input_file)
    if signal is None or indices is None:
        messagebox.showerror("Error", "Could not read the signal from the file.")
        return

    # Process signal: fold and shift
    folded_signal = fold_signal(signal)
    folded_indices = fold_signal(indices)
    shifted_indices, shifted_signal = delay_or_advance_signal(folded_signal, folded_indices, k)

    # Compare with expected output
    expected_file = "c://Users//96650//Desktop//signals//Output_ShifFoldedby500.txt" if k > 0 else "c://Users//96650//Desktop//signals//Output_ShiftFoldedby-500.txt"
    Shift_Fold_Signal(expected_file, shifted_indices, shifted_signal)
    
  


def QuantizationTest2(file_name,Your_IntervalIndices,Your_EncodedValues,Your_QuantizedValues,Your_SampledError):
    expectedIntervalIndices=[]
    expectedEncodedValues=[]
    expectedQuantizedValues=[]
    expectedSampledError=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==4:
                L=line.split(' ')
                V1=int(L[0])
                V2=str(L[1])
                V3=float(L[2])
                V4=float(L[3])
                expectedIntervalIndices.append(V1)
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                expectedSampledError.append(V4)
                line = f.readline()
            else:
                break
    if(len(Your_IntervalIndices)!=len(expectedIntervalIndices)
     or len(Your_EncodedValues)!=len(expectedEncodedValues)
      or len(Your_QuantizedValues)!=len(expectedQuantizedValues)
      or len(Your_SampledError)!=len(expectedSampledError)):
        print("QuantizationTest2 Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_IntervalIndices)):
        if(Your_IntervalIndices[i]!=expectedIntervalIndices[i]):
            print("QuantizationTest2 Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(Your_EncodedValues)):
        if(Your_EncodedValues[i]!=expectedEncodedValues[i]):
            print("QuantizationTest2 Test case failed, your EncodedValues have different EncodedValues from the expected one") 
            return
        
    for i in range(len(expectedQuantizedValues)):
        if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
            continue
        else:
            print("QuantizationTest2 Test case failed, your QuantizedValues have different values from the expected one") 
            return
    for i in range(len(expectedSampledError)):
        if abs(Your_SampledError[i] - expectedSampledError[i]) < 0.01:
            continue
        else:
            print("QuantizationTest2 Test case failed, your SampledError have different values from the expected one") 
            return
    print("QuantizationTest2 Test case passed successfully")
def read_signal_with_indices_from_txt(file_path):
    """Reads the signal and its indices from a text file."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        indices = []
        signal = []

        for line in lines[3:]:  # Skip the first 3 rows as per your framework
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            indices.append(int(parts[0]))  # Assuming the first column is the index
            signal.append(float(parts[1]))  # Assuming the second column is the signal value

        return signal, indices
    except Exception as e:
        print(f"Error reading signal: {e}")
        return None, None
def quantize_signal(signal, num_levels):
    min_val, max_val = min(signal), max(signal)

   
    quantization_levels = np.linspace(min_val, max_val, num_levels + 1)
    quantization_levels = (quantization_levels[:-1] + quantization_levels[1:]) / 2
    num_bits = int(np.ceil(np.log2(num_levels)))

  
    binary_codes = [format(i, f'0{num_bits}b') for i in range(num_levels)]

    quantized_signal = []
    encoded_signal = []
    interval_indices = []

    
    for value in signal:
        
        idx = (np.abs(quantization_levels - value)).argmin()
        interval_indices.append(idx)
        quantized_value = quantization_levels[idx]
        quantized_signal.append(quantized_value)
        encoded_signal.append(binary_codes[idx])

   
    error =  np.array(quantized_signal) - np.array(signal)
    avg_power_error = np.mean(error ** 2)

    return interval_indices, encoded_signal, quantized_signal, error, avg_power_error

# Plotting function
def display_plot(interval_indices, encoded_values, quantized_values, error):
    root = tk.Tk()
    root.title("Values Table")

    # Create a Treeview widget
    tree = ttk.Treeview(root, columns=("Interval Index", "Encoded Value", "Quantized Value", "Error"), show="headings")

    # Define headings
    tree.heading("Interval Index", text="Interval Index")
    tree.heading("Encoded Value", text="Encoded Value")
    tree.heading("Quantized Value", text="Quantized Value")
    tree.heading("Error", text="Error")

    # Set column widths
    tree.column("Interval Index", width=120)
    tree.column("Encoded Value", width=120)
    tree.column("Quantized Value", width=120)
    tree.column("Error", width=120)

    # Insert data into the treeview
    for i in range(len(interval_indices)):
        tree.insert("", "end", values=(interval_indices[i], encoded_values[i], quantized_values[i], error[i]))

    # Pack the treeview into the window
    tree.pack(expand=True, fill="both")

# Menu for choosing levels or bits
def open_choice_menu():
    rep_window = tk.Toplevel()
    rep_window.title("Quantization of Signals")
    rep_window.geometry("300x200")

    # Initialize choice_var with a default value to make sure it updates
    choice_var = IntVar(value=1)

    # Frame for radio buttons
    radio_frame = tk.Frame(rep_window)
    radio_frame.pack(pady=20)

    # Define the radio buttons with choice_var variable and values 1 and 2
    Radiobutton(radio_frame, text="Number of Levels", variable=choice_var, value=1).pack(anchor="center")
    Radiobutton(radio_frame, text="Number of Bits", variable=choice_var, value=2).pack(anchor="center")

    def confirm_choice():
        choice = choice_var.get()  # Get current value of choice_var
        print("Selected choice:", choice)  # Debug print to verify selection
        rep_window.destroy()

        #for widget in root.winfo_children():
            #widget.destroy()

        levels = None  # Initialize `levels` here to avoid `UnboundLocalError`
        
        if choice == 1:
            user_input = simpledialog.askinteger("Input", "Enter the number of levels:")
            levels = user_input
        elif choice == 2:
            user_input = simpledialog.askinteger("Input", "Enter the number of bits:")
            levels = 2 ** user_input if user_input else None
            bit_length = user_input
            print("Number of bits:", user_input)
            print("Number of levels:", levels)

        if levels is not None:
            process_quantization(levels)
        else:
            messagebox.showwarning("Warning", "Invalid input.")

    tk.Button(rep_window, text="Confirm", command=confirm_choice).pack(pady=10)
# Main quantization processing function
def process_quantization(levels):
    ind, signal = browse_and_read_signal_file()  # Load the signal from file
    print("Original Signal:", signal)

    # Quantize signal and get results
    interval_indices, encoded_values, quantized_values, error, avg_power_error = quantize_signal(signal, levels)
    one_based_interval_index = [x + 1 for x in interval_indices]
    print(interval_indices)
    print(encoded_values)
    print(quantized_values)
    print(error)
    # Display plot
    display_plot(one_based_interval_index, encoded_values, quantized_values, error)

    # Save results to files
    QuantizationTest1("c://Users//96650//Desktop//signals//Task3 Files//Quan1_Out.txt", encoded_values, quantized_values)
    QuantizationTest2("c://Users//96650//Desktop//signals//Task3 Files//Quan2_Out.txt",one_based_interval_index,  encoded_values, quantized_values, error)
def DerivativeSignal():
        InputSignal = [
            "1f", "2f", "3f", "4f", "5f", "6f", "7f", "8f", "9f", "10f", "11f", "12f", "13f", "14f", "15f", "16f", 
            "17f", "18f", "19f", "20f", "21f", "22f", "23f", "24f", "25f", "26f", "27f", "28f", "29f", "30f", "31f", 
            "32f", "33f", "34f", "35f", "36f", "37f", "38f", "39f", "40f", "41f", "42f", "43f", "44f", "45f", "46f", 
            "47f", "48f", "49f", "50f", "51f", "52f", "53f", "54f", "55f", "56f", "57f", "58f", "59f", "60f", "61f", 
            "62f", "63f", "64f", "65f", "66f", "67f", "68f", "69f", "70f", "71f", "72f", "73f", "74f", "75f", "76f", 
            "77f", "78f", "79f", "80f", "81f", "82f", "83f", "84f", "85f", "86f", "87f", "88f", "89f", "90f", "91f", 
            "92f", "93f", "94f", "95f", "96f", "97f", "98f", "99f", "100f"
]

# Remove the 'f' and convert to float
        CleanedSignal = [float(value[:-1]) for value in InputSignal]
        expectedOutput_first = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        expectedOutput_second = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        """
        Write your Code here:
        Start
        """
            # Calculate first derivative
        FirstDrev = [CleanedSignal[i] - CleanedSignal[i - 1] for i in range(1, len(CleanedSignal))]

            # Calculate second derivative
        SecondDrev = [CleanedSignal[i + 1] - 2 * CleanedSignal[i] + CleanedSignal[i - 1] for i in range(1, len(CleanedSignal) - 1)]

        
        """
        End
        """
        
        """
        Testing your Code
        """
        if( (len(FirstDrev)!=len(expectedOutput_first)) or (len(SecondDrev)!=len(expectedOutput_second))):
            print("mismatch in length") 
            return
        first=second=True
        for i in range(len(expectedOutput_first)):
            if abs(FirstDrev[i] - expectedOutput_first[i]) < 0.01:
                continue
            else:
                first=False
                print("1st derivative wrong")
                return
        for i in range(len(expectedOutput_second)):
            if abs(SecondDrev[i] - expectedOutput_second[i]) < 0.01:
                continue
            else:
                second=False
                print("2nd derivative wrong") 
                return
        if(first and second):
            print("Derivative Test case passed successfully")
        else:
            print("Derivative Test case failed")
        return

def calculate_dft_and_display():
    global X  # Declare global to modify it
    # Browse and read input signal file
    time, amplitude = browse_and_read_signal_file()
    if time is None or amplitude is None:
        return

    # Calculate the DFT using the exponential form
    N = len(amplitude)
    X = [0] * N
    frequencies = [k * Fs / N for k in range(N)]  # Non-negative frequencies

    for k in range(N):
        for n in range(N):
            X[k] += amplitude[n] * np.exp(-1j * 2 * np.pi * k * n / N)

    # Calculate magnitudes and phases
    magnitudes = np.abs(X)
    phases = np.angle(X)

    # Compare with expected values
    expected_amplitudes, expected_phases = browse_and_read_expected_values()
    if expected_amplitudes is None or expected_phases is None:
        return

    # Output formatted results
    formatted_output = []
    for index, (magnitude, phase) in enumerate(zip(magnitudes, phases)):
        if index in [3, 5]:
            formatted_output.append(f"{magnitude:.14f}f {phase:.14f}f")
        else:
            if phase.is_integer():
                formatted_output.append(f"{int(magnitude)} {int(phase)}")
            elif magnitude.is_integer():
                formatted_output.append(f"{int(magnitude)} {phase:.14f}f")
            else:
                formatted_output.append(f"{magnitude:.13f}f {phase:.14f}f")

    output_file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    title="Save Formatted Output",
                                                    filetypes=[("Text Files", "*.txt"),
                                                               ("All Files", ".*")])
    if output_file_path:
        with open(output_file_path, 'w') as f:
            for line in formatted_output:
                f.write(line + '\n')

    if SignalCompareAmplitude(magnitudes, expected_amplitudes) and SignalComparePhaseShift(phases, expected_phases):
        messagebox.showinfo("Comparison Result", "The calculated DFT matches the expected results.")
    else:
        messagebox.showerror("Comparison Result", "The calculated DFT does not match the expected results.")

    # Display the DFT result
    display_dft_result(frequencies, magnitudes, phases)

def calculate_idft_and_display():
    global X  # Access the global DFT results
    if not X:
        messagebox.showerror("Error", "No DFT data available for IDFT calculation.")
        return

    N = len(X)
    idft_signal = []

    for n in range(N):
        # IDFT formula using exponential form
        X_k = sum(X[k] * np.exp(1j * 2 * np.pi * k * n / N) for k in range(N)) / N
        idft_signal.append(X_k.real)

    # Display the IDFT result
    display_idft_result(idft_signal)

def display_idft_result(idft_signal):
    plt.figure(figsize=(10, 4))
    plt.plot(idft_signal, marker='o', linestyle='-')
    plt.title('Inverse Discrete Fourier Transform (IDFT) Result')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

def browse_and_read_expected_values():
    file_path = filedialog.askopenfilename(
        title="Select Expected Values File",
        filetypes=(("Text Files", ".txt"), ("All Files", ".*"))
    )
    if not file_path:
        messagebox.showinfo("No File Selected", "Please select a valid file.")
        return None, None

    try:
        with open(file_path, 'r') as f:
            expected_amplitudes = []
            expected_phases = []
            for _ in range(3):
                next(f)

            for line in f:
                parts = line.split()
                if len(parts) != 2:
                    messagebox.showerror("Error", f"Line format error: '{line.strip()}' - Expected two values.")
                    return None, None
                try:
                    amp = float(parts[0].rstrip('f'))
                    phase = float(parts[1].rstrip('f'))
                    expected_amplitudes.append(amp)
                    expected_phases.append(phase)
                except ValueError:
                    messagebox.showerror("Error", f"Invalid number format in line: '{line.strip()}'")
                    return None, None

        return np.array(expected_amplitudes), np.array(expected_phases)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None, None

def browse_and_read_signal_file():
    file_path = filedialog.askopenfilename(
        title="Select Signal File",
        filetypes=(("Text Files", ".txt"), ("All Files", ".*"))
    )
    if not file_path:
        messagebox.showinfo("No File Selected", "Please select a valid file.")
        return None, None

    try:
        with open(file_path, 'r') as f:
            for _ in range(3):  
                next(f)
            time, amplitude = [], []
            for line in f:
                t, a = map(float, line.split())
                time.append(t)
                amplitude.append(a)
        return np.array(time), np.array(amplitude)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None, None

def display_dft_result(frequencies, magnitudes, phases):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.stem(frequencies, magnitudes, linefmt='b-', markerfmt='bo', basefmt=" ")
    ax1.set_title('Frequency vs Amplitude')
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Amplitude')
    ax1.grid(True)

    ax2.stem(frequencies, phases, linefmt='orange', markerfmt='o', basefmt=" ")
    ax2.set_title('Frequency vs Phase')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Phase (radians)')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

def SignalCompareAmplitude(SignalInput=[], SignalOutput=[]):
    if len(SignalInput) != len(SignalOutput):
        return False
    for i in range(len(SignalInput)):
        if abs(SignalInput[i] - SignalOutput[i]) > 1e-10:  
            print(f"Mismatch at index {i}: {SignalInput[i]} vs {SignalOutput[i]}")
            return False
    return True

def RoundPhaseShift(P):
    while P < 0:
        P += 2 * np.pi
    return float(P % (2 * np.pi))

def SignalComparePhaseShift(SignalInput=[], SignalOutput=[]):
    if len(SignalInput) != len(SignalOutput):
        return False
    for i in range(len(SignalInput)):
        A = RoundPhaseShift(SignalInput[i])
        B = RoundPhaseShift(SignalOutput[i])
        if abs(A - B) > 0.0001:
            print(f"Phase mismatch at index {i}: {A} vs {B}")
            return False
    return True

def Compare_Signals(file_name,Your_indices,Your_samples):      
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    print("Current Output Test file is: ")
    print(file_name)
    print("\n")
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Shift_Fold_Signal Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Shift_Fold_Signal Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Correlation Test case failed, your signal have different values from the expected one") 
            return
    print("Correlation Test case passed successfully")

def normalized_cross_correlation(X1, X2):
    X1 = np.array(X1)
    X2 = np.array(X2)

    N = len(X1)  # Signal length

    # Pre-compute squared sums for normalization
    X1_squared_sum = np.sum(X1 ** 2)
    X2_squared_sum = np.sum(X2 ** 2)
    normalization = np.sqrt(X1_squared_sum * X2_squared_sum)

    # Compute the cross-correlation numerator
    r12 = []
    for j in range(N):
        numerator = sum(X1[i] * X2[(i + j) % N] for i in range(N))  # Periodic signals
        r12.append(numerator / normalization)

    return np.array(r12)

def test_normalized_cross_correlation():
    """
    Test normalized cross-correlation using browsed signal files and compare results.
    """
    # Assuming browse_and_read_signal_file() loads the signals
    signal1_indices, signal1_samples = browse_and_read_signal_file()
    if signal1_indices is None or signal1_samples is None:
        return

    signal2_indices, signal2_samples = browse_and_read_signal_file()
    if signal2_indices is None or signal2_samples is None:
        return

    # Compute normalized cross-correlation
    normalized_cc = normalized_cross_correlation(signal1_samples, signal2_samples)
   
    # Compare with expected output (assuming Compare_Signals is correctly implemented)
    expected_file_path = filedialog.askopenfilename(
        title="Select Expected Output File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if not expected_file_path:
        messagebox.showerror("Error", "No file selected!")
        return

    # Assuming Compare_Signals compares the output with expected values
    Compare_Signals(expected_file_path, signal1_indices, normalized_cc)

def compare_with_expected_output(smoothed_signal, expected_file_path):
    """
    Compares the computed smoothed signal with the expected output stored in a file.
    """
    try:
        expected_output = read_signal_file(expected_file_path)
    except ValueError as e:
        messagebox.showerror("Error", f"Could not read the expected output file: {e}")
        return

    # Round the smoothed signal to 3 decimal places
    rounded_smoothed_signal = np.round(smoothed_signal, 3)

    # Compare the signals
    if np.allclose(rounded_smoothed_signal, expected_output, atol=1e-5):
        messagebox.showinfo("Comparison Result", "Test Passed: Computed signal matches the expected signal.")
    else:
        messagebox.showerror("Comparison Result", f"Test Failed: Computed signal does not match the expected signal.\n\n"
                                                  f"Computed: {rounded_smoothed_signal}\n"
                                                  f"Expected: {expected_output}")
def remove_dc_time_domain(signal):
    """
    Removes the DC component (mean value) from the signal in the time domain.
    """
    mean_value = np.mean(signal)
    return signal - mean_value
def compute_and_compare_with_dc_removal():
    """
    Computes the signal with the DC component removed (time domain) and compares it with the expected output.
    Optionally smooth the signal.
    """
    # Step 1: Load the input signal
    from tkinter import filedialog

    input_file_path = filedialog.askopenfilename(title="Select Input Signal File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not input_file_path:
        messagebox.showerror("Error", "No input file selected!")
        return

    try:
        signal = read_signal_file(input_file_path)
    except ValueError as e:
        messagebox.showerror("Error", f"Could not read the input file: {e}")
        return

    # Step 2: Remove DC and smooth signal (time domain only)
    signal_no_dc =remove_dc_time_domain(signal)

    # Step 3: Load the expected output file
    expected_file_path = filedialog.askopenfilename(title="Select Expected Output File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not expected_file_path:
        messagebox.showerror("Error", "No expected output file selected!")
        return

    # Step 4: Compare the computed signal with the expected signal (only time domain DC removal)
    compare_with_expected_output(signal_no_dc, expected_file_path)
def dft(signal):
    N = len(signal)
    X = np.zeros(N, dtype=complex)
    
    for k in range(N):
        # Sum of exponentials for each frequency component
        X[k] = np.sum(signal * np.exp(-2j * np.pi * k * np.arange(N) / N))
    return X

def idft(X):
    N = len(X)
    x_reconstructed = np.zeros(N, dtype=complex)
    
    for n in range(N):
        # Sum of exponentials for each time-domain component
        x_reconstructed[n] = np.sum(X * np.exp(2j * np.pi * n * np.arange(N) / N)) / N
    return x_reconstructed

def remove_dc_frequency_domain_highpass(signal):
    # Compute the DFT of the signal
    signal_dft = dft(signal)
    
    # Set the DC component (index 0) to zero
    signal_dft[0] = 0
    
    # Compute the inverse DFT to return to the time domain
    return np.real(idft(signal_dft))
def compute_and_compare_with_dc_removall():
    """
    Computes the signal with the DC component removed (time domain) and compares it with the expected output.
    Optionally smooth the signal.
    """
    # Step 1: Load the input signal
    from tkinter import filedialog

    input_file_path = filedialog.askopenfilename(title="Select Input Signal File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not input_file_path:
        messagebox.showerror("Error", "No input file selected!")
        return

    try:
        signal = read_signal_file(input_file_path)
    except ValueError as e:
        messagebox.showerror("Error", f"Could not read the input file: {e}")
        return

    # Step 2: Remove DC and smooth signal (time domain only)
    signal_no_dc =remove_dc_frequency_domain_highpass(signal)

    # Step 3: Load the expected output file
    expected_file_path = filedialog.askopenfilename(title="Select Expected Output File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not expected_file_path:
        messagebox.showerror("Error", "No expected output file selected!")
        return

    # Step 4: Compare the computed signal with the expected signal (only time domain DC removal)
    compare_with_expected_output(signal_no_dc, expected_file_path)
def compute_moving_average():
    """
    Computes the moving average for a signal read from a file using read_signal_file.
    """
    from tkinter import filedialog

    # Prompt the user to select a file
    file_path = filedialog.askopenfilename(title="Select Signal File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return

    # Read the signal from the file using the provided function
    try:
        signal = read_signal_file(file_path)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    # Prompt the user to enter the window size
    window_size_input = simpledialog.askstring("Window Size", "Enter the moving average window size (positive integer):")
    if not window_size_input:
        messagebox.showerror("Error", "Window size is required!")
        return

    # Validate and convert the window size to an integer
    try:
        window_size = int(window_size_input)
        if window_size <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid window size. Please enter a positive integer.")
        return

    # Ensure the window size is not greater than the signal length
    if window_size > len(signal):
        messagebox.showerror("Error", "Window size cannot be larger than the signal length.")
        return

    # Compute the moving average
    smoothed_signal = [
        np.mean(signal[i:i + window_size]) 
        for i in range(len(signal) - window_size + 1)
    ]
    expected_file_path = filedialog.askopenfilename(title="Select Expected Output File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not expected_file_path:
        messagebox.showerror("Error", "No expected output file selected!")
        return

    # Step 4: Compare the computed signal with the expected signal (only time domain DC removal)
    compare_with_expected_output(smoothed_signal, expected_file_path)

def read_signall_file(filename):
    """Reads the signal file and returns the indices and samples, skipping the first 3 lines."""
    try:
        with open(filename, 'r') as f:
            for _ in range(3):  
                next(f)
            time, amplitude = [], []
            for line in f:
                t, a = map(float, line.split())
                time.append(t)
                amplitude.append(a)
        return np.array(time), np.array(amplitude)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None, None

def ConvTest(Your_indices,Your_samples): 
    """
    Test inputs
    InputIndicesSignal1 =[-2, -1, 0, 1]
    InputSamplesSignal1 = [1, 2, 1, 1 ]
    
    InputIndicesSignal2=[0, 1, 2, 3, 4, 5 ]
    InputSamplesSignal2 = [ 1, -1, 0, 0, 1, 1 ]
    """
    
    expected_indices=[-2, -1, 0, 1, 2, 3, 4, 5, 6]
    expected_samples = [1, 1, -1, 0, 0, 3, 3, 2, 1 ]

    
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Conv Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Conv Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Conv Test case failed, your signal have different values from the expected one") 
            return
    print("Conv Test case passed successfully")

def compute_convolution(signal_data, signal_indices, signal_data_2, signal_indices_2):
   # global signal_data, signal_indices, signal_data_2, signal_indices_2

    if signal_data is None or signal_data_2 is None:
        messagebox.showerror("Error", "Both signals must be loaded.")
        return


    # Manual computation of convolution
    len_signal1 = len(signal_data)
    len_signal2 = len(signal_data_2)
    convolved_signal = []
    for n in range(len_signal1 + len_signal2 - 1):
            conv_sum = 0
            for k in range(len_signal1):
                if 0 <= n - k < len_signal2:
                    conv_sum += signal_data[k] * signal_data_2[n - k]
            convolved_signal.append(conv_sum)

        # Calculate correct indices for the convolved signal
    start_index = int(signal_indices[0] + signal_indices_2[0])
    convolved_indices = list(range(start_index, start_index + len(convolved_signal)))
    return convolved_indices, convolved_signal
        
def compute_convolution_from_files(file1, file2):
    """Compute the convolution of two signals read from files."""
    try:
        # Load signals and indices using read_signal_file
        indices1, signal1 = read_signall_file(file1)
        indices2, signal2 = read_signall_file(file2)

        # Compute the convolution and return results
        return compute_convolution(signal1, indices1, signal2, indices2)

    except Exception as e:
        messagebox.showerror("Error", f"Error reading input files: {e}")
        return None, None

def convolution():
    """Convolution GUI function to allow the user to select files and compute convolution."""
    # Create file dialog for the first signal file
    file1 = filedialog.askopenfilename(title="Select First Signal File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not file1:
        messagebox.showerror("Error", "No first file selected!")
        return

    # Create file dialog for the second signal file
    file2 = filedialog.askopenfilename(title="Select Second Signal File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not file2:
        messagebox.showerror("Error", "No second file selected!")
        return

    # Call the convolution function to get the result
    indices1, signal1 = read_signall_file(file1)
    indices2, signal2 = read_signall_file(file2)
    print(indices1)
    print(signal1)
    print(indices2)
    print(signal2)
    result_indices, result_samples = compute_convolution(signal1,indices1,signal2,indices2)
    print(result_indices)
    print(result_samples)
    ConvTest(result_indices, result_samples)

        
root = tk.Tk()
root.title("Tasks")
root.geometry("900x600")  

task_1_button = tk.Button(root, text="main menue", command=task1_sub_tasks)
task_1_button.pack(pady=20)

task_2_button = tk.Button(root, text="validate", command=menue)
task_2_button.pack(pady=20)
root.config(background='lightblue')
root.mainloop()
####sssssssssss