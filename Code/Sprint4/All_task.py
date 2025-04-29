import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# Global list to store tasks
tasks = []


# Task Ops
def show_all_tasks():
    for w in result_frame.winfo_children():
        w.destroy()

    create_btn = ttk.Button(result_frame, text="Create Task",
                            style="Italic.TButton",
                            command=open_task_dialog)
    create_btn.pack(anchor="ne", pady=(0, 10))

    for idx, task in enumerate(tasks):
        row = tk.Frame(result_frame)
        row.pack(fill="x", pady=2)

        completed_var = tk.BooleanVar(value=task.get("completed", False))
        chk = ttk.Checkbutton(row, variable=completed_var,
                              command=lambda i=idx, v=completed_var: toggle_complete(i, v))
        chk.pack(side="left")

        details_txt = (
            f"{task['name']} | {task['date']} | {task['priority']}\n"
            f"      Details: {task.get('details', '')}"
        )
        ttk.Label(row, text=details_txt, justify="left", font=task_font).pack(side="left", padx=5)

        ttk.Button(row, text="Edit", command=lambda i=idx: open_task_dialog(i)).pack(side="right", padx=2)
        ttk.Button(row, text="Delete", command=lambda i=idx: delete_task(i)).pack(side="right")


def open_task_dialog(index=None):
    dialog = tk.Toplevel(root)
    dialog.title("Edit Task" if index is not None else "Create Task")
    dialog.resizable(True, False)
    dialog.update_idletasks()
    # main window position and size
    px = root.winfo_x()
    py = root.winfo_y()
    pw = root.winfo_width()
    ph = root.winfo_height()
    # dialog “requested” size
    dw = dialog.winfo_reqwidth()
    dh = dialog.winfo_reqheight()
    # calculate position: center of root minus half of dialog
    x = px + (pw // 2) - (dw // 2)
    y = py + (ph // 2) - (dh // 2)
    dialog.geometry(f"+{x}+{y}")
    dialog.transient(root)
    dialog.grid_columnconfigure(1, weight=1)

    # Name
    ttk.Label(dialog, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    name_var = tk.StringVar(value=tasks[index]['name'] if index is not None else "")
    ttk.Entry(dialog, textvariable=name_var).grid(row=0, column=1, sticky="we", padx=5, pady=5)

    # Date
    ttk.Label(dialog, text="Date:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    date_var = tk.StringVar(value=tasks[index]['date'] if index is not None else "")
    DateEntry(dialog, textvariable=date_var, date_pattern="yyyy-mm-dd") \
        .grid(row=1, column=1, sticky="we", padx=5, pady=5)

    # Priority
    ttk.Label(dialog, text="Priority:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    prio_var = tk.StringVar(value=tasks[index]['priority'] if index is not None else "Medium")
    ttk.Combobox(dialog, textvariable=prio_var, values=["Low", "Medium", "High"], state="readonly") \
        .grid(row=2, column=1, sticky="we", padx=5, pady=5)

    # Details (multiline)
    ttk.Label(dialog, text="Details:").grid(row=3, column=0, sticky="ne", padx=5, pady=5)
    details_txt = tk.Text(dialog, height=4)
    details_txt.grid(row=3, column=1, sticky="we", padx=5, pady=5)
    if index is not None:
        details_txt.insert("1.0", tasks[index].get("details", ""))

    # Save/Cancel
    def save_task():
        name = name_var.get().strip()
        date = date_var.get()
        priority = prio_var.get()
        details = details_txt.get("1.0", "end").strip()
        if not name:
            messagebox.showwarning("Input Error", "Name cannot be empty.")
            return
        data = {"name": name, "date": date, "priority": priority,
                "details": details, "completed": False}
        if index is None:
            tasks.append(data)
        else:
            tasks[index].update(data)
        dialog.destroy()
        show_all_tasks()

    ttk.Button(dialog, text="Save", command=save_task) \
        .grid(row=4, column=1, padx=5, pady=10)
    ttk.Button(dialog, text="Cancel", command=dialog.destroy) \
        .grid(row=4, column=0, padx=5, pady=10)


def delete_task(i):
    if messagebox.askyesno("Confirm Delete", "Delete this task?"):
        tasks.pop(i)
        show_all_tasks()


def toggle_complete(i, var):
    tasks[i]['completed'] = var.get()


# Nav handler (just All Tasks for now)
def on_nav_button(name):
    if name == "All Tasks":
        show_all_tasks()
    else:
        for w in result_frame.winfo_children(): w.destroy()
        ttk.Label(result_frame, text=f"'{name}' not done.", font=result_font) \
            .pack(expand=True)


for name in ("All Tasks", "Today", "Upcoming", "High Priority", "Completed"):
    ttk.Button(btn_frame, text=name, style="Italic.TButton",
               command=lambda n=name: on_nav_button(n)) \
        .pack(fill="x", pady=2)

show_all_tasks()

