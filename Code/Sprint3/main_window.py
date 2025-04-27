# import tkinter
import tkinter as tk
from tkinter import ttk


# create main window gui
def build_gui():
    root = tk.Tk()
    root.title("Not-Notion!")
    root.geometry("500x300")

    # Configure grid weights to align vertical and horizontal lines
    root.grid_rowconfigure(0, weight=0)   # header row (dashboard/not-notion)
    root.grid_rowconfigure(1, weight=1)   # content row (buttons/results)
    root.grid_columnconfigure(0, weight=0)  # left column (dashboard/buttons)
    root.grid_columnconfigure(1, weight=1)  # right column (not-notion/results)

    # Top-Left: Dashboard area
    # Create dashboard frame and label including color, font, size
    dash_frame = tk.Frame(root, bd=0.5, background="#00BFFF", relief="groove", padx=5, pady=5)
    dash_frame.grid(row=0, column=0, sticky="nsew")
    dash_label = ttk.Label(dash_frame, text="Dashboard", background="#00BFFF",
                           foreground="#F0FFFF", font=("Segoe UI", 12, "bold"))
    dash_label.pack(anchor="center")

    # Top-Right: Not-Notion title area
    # Create title frame and label including color, font, size
    title_frame = tk.Frame(root, bd=0.5, background="#1874CD", relief="groove", padx=5, pady=5)
    title_frame.grid(row=0, column=1, sticky="nsew")
    title_label = ttk.Label(title_frame, text="Not-Notion!", background="#1874CD",
                            foreground="#F0FFFF", font=("Segoe UI", 18, "bold"))
    title_label.pack(anchor="center")

    # Bottom-Left: Button-names area
    btn_frame = tk.Frame(root, bd=0.5, relief="groove", padx=5, pady=5)
    btn_frame.grid(row=1, column=0, sticky="nsew")
    for name in ("All Tasks", "Today", "Upcoming", "High Priority", "Completed"):
        btn_label = (ttk.Button(btn_frame, text=name))
        btn_label.pack(fill="x", pady=2)

    # Bottom-Right: Result display area
    result_frame = tk.Frame(root, bd=0.5, relief="groove", padx=5, pady=5)
    result_frame.grid(row=1, column=1, sticky="nsew")
    result_label = (ttk.Label(result_frame,
                              text="Here you will see the result after pressing the button",
                              foreground="#666"))
    result_label.pack(expand=True)

    root.mainloop()


if __name__ == "__main__":
    build_gui()
