import numpy as np
import matplotlib.pyplot as plt
from tkinter import Button, IntVar, Label, Radiobutton, simpledialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox


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


        modified_amplitude = np.cumsum(amplitude)

        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        
        ax1.plot(time, amplitude, label='Original Signal', color='blue')
        ax1.set_title('Original Signal')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Amplitude')
        ax1.grid(True)
        ax1.legend()

        
        ax2.plot(time, modified_amplitude, label='Accumulated Signal', color='green')
        ax2.set_title('Accumulated Signal')
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

def quantize_signal(signal, num_levels):
    min_val, max_val = min(signal), max(signal)

    # Calculate quantization levels as midpoints of each interval
    quantization_levels = np.linspace(min_val, max_val, num_levels + 1)
    quantization_levels = (quantization_levels[:-1] + quantization_levels[1:]) / 2
    num_bits = int(np.ceil(np.log2(num_levels)))

    # Create binary codes for each level
    binary_codes = [format(i, f'0{num_bits}b') for i in range(num_levels)]

    # Initialize lists to store results
    quantized_signal = []
    encoded_signal = []
    interval_indices = []

    # Quantize the signal
    for value in signal:
        # Find the closest quantization level
        idx = (np.abs(quantization_levels - value)).argmin()
        interval_indices.append(idx)
        quantized_value = quantization_levels[idx]
        quantized_signal.append(quantized_value)
        encoded_signal.append(binary_codes[idx])

    # Calculate error and average power error
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
    display_plot(interval_indices, encoded_values, quantized_values, error)

    # Save results to files
    QuantizationTest1("D:\\uni\\DSP\\DSP_tasks\\task3\\Quan1_Out.txt", encoded_values, quantized_values)
    QuantizationTest2("D:\\uni\\DSP\\DSP_tasks\\task3\\Quan2_Out.txt",one_based_interval_index,  encoded_values, quantized_values, error)
root = tk.Tk()
root.title("Tasks")
root.geometry("900x600")  

task_1_button = tk.Button(root, text="main menue", command=task1_sub_tasks)
task_1_button.pack(pady=20)

task_2_button = tk.Button(root, text="validate", command=menue)
task_2_button.pack(pady=20)
root.config(background='lightblue')
root.mainloop()
####sssssss
