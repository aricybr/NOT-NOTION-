
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import datetime

from node import Node
from data_storage import DataStorage
from priority_task_queue import PriorityTaskQueue

class TaskQueue:
    """
    Pure logic that only adds/deletes/sorts tasks.
    """
    def __init__(self):
        self._nodes = []

    def add_task(self, node: Node):
        self._nodes.append(node)
        self._sort()

    def remove_task(self, node: Node):
        self._nodes.remove(node)

    def get_all_tasks(self) -> list[Node]:
        return list(self._nodes)

    def _sort(self):
        order = {"High": 0, "Medium": 1, "Low": 2}
        self._nodes.sort(
            key=lambda n: (
                datetime.date.fromisoformat(n.creation_date),
                order.get(n.priority, 1)
            )
        )

class MainApp:
    """
    Class responsible for screen setup / navigation / linkage with persistence / main loop startup.
    """
    def __init__(self, task_queue: TaskQueue, storage: DataStorage):
        self.scr_width, self.scr_height = 600, 400
        self.task_queue = task_queue
        self.storage    = storage

        # Root window
        self.root = tk.Tk()
        self.root.title("Not-Notion!")
        self.root.geometry(f"{self.scr_width}x{self.scr_height}")

        # Fonts & Button Styles
        self._setup_fonts()

        # Layout Creation
        self._build_layout()

        # Execute _on_resize when resizing window
        self.root.bind("<Configure>", self._on_resize)

        # UI component for task list
        self.view = PriorityTaskQueue(
            parent=self.result_frame,
            task_queue=self.task_queue,
            storage=self.storage,
            result_font=self.result_font
        )

        # Initial display
        self.show("All Tasks")

        # GUI startup
        self.root.mainloop()

    def _setup_fonts(self):
        self.dash_font   = tkFont.Font(family="Segoe UI", size=15, weight="bold")
        self.title_font  = tkFont.Font(family="Segoe UI", size=20, weight="bold")
        self.button_font = tkFont.Font(family="Segoe UI", size=12, slant="italic")
        self.result_font = tkFont.Font(family="Segoe UI", size=12)
        style = ttk.Style(self.root)
        style.configure("Italic.TButton", font=self.button_font)

    def _build_layout(self):
        # Grid Ratio Setting
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=10)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=10)

        # Dashboard
        dash = tk.Frame(self.root, bg="#00BFFF", padx=5, pady=5)
        dash.grid(row=0, column=0, sticky="nsew")
        ttk.Label(dash, text="Dashboard", font=self.dash_font,
                  background="#00BFFF", foreground="#F0FFFF").pack()

        # Title
        title = tk.Frame(self.root, bg="#1874CD", padx=5, pady=5)
        title.grid(row=0, column=1, sticky="nsew")
        ttk.Label(title, text="Not-Notion!", font=self.title_font,
                  background="#1874CD", foreground="#F0FFFF").pack()

        # Navigation buttons
        nav = tk.Frame(self.root, padx=5, pady=5)
        nav.grid(row=1, column=0, sticky="nsew")
        for name in ("All Tasks", "Today", "Upcoming", "High Priority", "Completed"):
            ttk.Button(nav,
                       text=name,
                       style="Italic.TButton",
                       command=lambda n=name: self.show(n))\
               .pack(fill="x", pady=2)

        # Task display area
        self.result_frame = tk.Frame(self.root, padx=5, pady=5)
        self.result_frame.grid(row=1, column=1, sticky="nsew")

    def _on_resize(self, event):
        # Called when the root window is resized
        if event.widget is not self.root:
            return
        scale = min(event.width / self.scr_width,
                    event.height / self.scr_height)
        for font_obj, base_size in (
            (self.dash_font,   15),
            (self.title_font,  20),
            (self.button_font, 12),
        ):
            font_obj.configure(size=max(base_size, int(base_size * scale)))

    def show(self, name: str):
        # View switching according to navigation
        mapping = {
            "All Tasks":     self.view.show_all,
            "Today":         self.view.show_today,
            "Upcoming":      self.view.show_upcoming,
            "High Priority": self.view.show_high_priority,
            "Completed":     self.view.show_completed,
        }
        func = mapping.get(name)
        if func:
            func()
        else:
            for w in self.result_frame.winfo_children():
                w.destroy()
            ttk.Label(self.result_frame,
                      text=f"'{name}' view not found",
                      font=self.result_font).pack(expand=True)


if __name__ == "__main__":
    task_queue = TaskQueue()
    storage = DataStorage("tasks.json")

    for node in storage.load_tasks():
        task_queue.add_task(node)

    MainApp(task_queue, storage)
