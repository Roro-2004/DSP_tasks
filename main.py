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
    print("Sine/Cosine Representation button clicked")

def main_menu():
    # Clear the main window for the main menu
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Tasks")

    # Task 1 Button to go to Task 1 Sub Tasks
    task_1_button = tk.Button(root, text="Task 1", command=task1_sub_tasks, width=20)
    task_1_button.pack(pady=20)

# Main window properties
root = tk.Tk()
root.title("Tasks")
root.geometry("900x600")  # Adjusted size to fit everything properly

# Start with the Main Menu
main_menu()

# Set background color
root.config(background='lightblue')

root.mainloop()
####sssssss
