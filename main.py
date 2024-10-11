import tkinter as tk


def task1_sub_tasks():
    # delete data in the main page
    for widget in root.winfo_children():
        widget.destroy()
    
    root.title("Task 1 sub tasks")
    signal_button = tk.Button(root, text="Signal Representation", command=signal_representation)
    signal_button.pack(pady=10)

    sine_cosine_button = tk.Button(root, text="Sine/Cosine Representation", command=sine_cosine_generation)
    sine_cosine_button.pack(pady=10)


def signal_representation():
    rep_window = tk.Tk()
    rep_window.title("Signal representation")
    rep_window.geometry("700x400")
    

def sine_cosine_generation():
    print("Sine/Cosine Representation button clicked")

# main window properties
root = tk.Tk()
root.title("Tasks")
root.geometry("400x400")


task_1_button = tk.Button(root, text="Task 1", command=task1_sub_tasks)
task_1_button.pack(pady=20)


root.mainloop()
