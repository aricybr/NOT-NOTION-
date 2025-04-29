# import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


def build_gui():
    root = tk.Tk()
    root.title("Not-Notion!")
    root.geometry("500x300")

    # Define base dimensions & font sizes
    base_width = 500
    base_height = 300

    dash_base_size = 14
    title_base_size = 18
    button_base_size = 12
    result_base_size = 12

    # Create named Font objects
    dash_font = tkFont.Font(family="Segoe UI", size=dash_base_size, weight="bold")
    title_font = tkFont.Font(family="Segoe UI", size=title_base_size, weight="bold")
    button_font = tkFont.Font(family="Segoe UI", size=button_base_size, slant="italic")
    result_font = tkFont.Font(family="Segoe UI", size=result_base_size)

    # Style for buttons
    style = ttk.Style(root)
    style.configure("Italic.TButton", font=button_font)

    # Layout
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=6)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=4)

    dash_frame = tk.Frame(root, bd=0.5, bg="#00BFFF", relief="groove", padx=5, pady=5)
    dash_frame.grid(row=0, column=0, sticky="nsew")
    ttk.Label(dash_frame, text="Dashboard", background="#00BFFF",
              foreground="#F0FFFF", font=dash_font).pack(anchor="center")

    title_frame = tk.Frame(root, bd=0.5, bg="#1874CD", relief="groove", padx=5, pady=5)
    title_frame.grid(row=0, column=1, sticky="nsew")
    ttk.Label(title_frame, text="Not-Notion!", background="#1874CD",
              foreground="#F0FFFF", font=title_font).pack(anchor="center")

    btn_frame = tk.Frame(root, bd=0.5, relief="groove", padx=5, pady=5)
    btn_frame.grid(row=1, column=0, sticky="nsew")
    for name in ("All Tasks", "Today", "Upcoming", "High Priority", "Completed"):
        ttk.Button(btn_frame, text=name, style="Italic.TButton").pack(fill="x", pady=2)

    result_frame = tk.Frame(root, bd=0.5, relief="groove", padx=5, pady=5)
    result_frame.grid(row=1, column=1, sticky="nsew")
    ttk.Label(result_frame,
              text="Here you will see the result after pressing the button",
              font=result_font, foreground="#666").pack(expand=True)

    # Resize handler
    def on_resize(event):
        # only respond when the root window itself resizes
        if event.widget is root:
            w_scale = event.width / base_width
            h_scale = event.height / base_height
            scale = min(w_scale, h_scale)

            # compute the excess multiplier above 1.0
            extra = max(0.0, scale - 1.0)

            # new size = base_size + (base_size * extra)
            dash_font.configure(size=max(dash_base_size,
                                         int(dash_base_size + dash_base_size * extra)))
            title_font.configure(size=max(title_base_size,
                                          int(title_base_size + title_base_size * extra)))
            button_font.configure(size=max(button_base_size,
                                           int(button_base_size + button_base_size * extra)))
            result_font.configure(size=max(result_base_size,
                                           int(result_base_size + result_base_size * extra)))

    root.bind("<Configure>", on_resize)
    root.mainloop()


if __name__ == "__main__":
    build_gui()
