import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import tkinter.font as tkFont

# Global list to store tasks
tasks = []


def build_gui():
    root = tk.Tk()
    root.title("Not-Notion!")
    root.geometry("600x400")

    # Base sizes
    base_width, base_height = 600, 400
    dash_base_size, title_base_size = 15, 20
    button_base_size, result_base_size = 12, 12

    # Fonts
    dash_font = tkFont.Font(family="Segoe UI", size=dash_base_size, weight="bold")
    title_font = tkFont.Font(family="Segoe UI", size=title_base_size, weight="bold")
    button_font = tkFont.Font(family="Segoe UI", size=button_base_size, slant="italic")
    result_font = tkFont.Font(family="Segoe UI", size=result_base_size)

    style = ttk.Style(root)
    style.configure("Italic.TButton", font=button_font)

    # Layout
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=10)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=10)

    # Dashboard / Title
    dash_frame = tk.Frame(root, bd=0.5, bg="#00BFFF", relief="groove", padx=5, pady=5)
    dash_frame.grid(row=0, column=0, sticky="nsew")
    ttk.Label(dash_frame, text="Dashboard", background="#00BFFF",
              foreground="#F0FFFF", font=dash_font).pack(anchor="center")

    title_frame = tk.Frame(root, bd=0.5, bg="#1874CD", relief="groove", padx=5, pady=5)
    title_frame.grid(row=0, column=1, sticky="nsew")
    ttk.Label(title_frame, text="Not-Notion!", background="#1874CD",
              foreground="#F0FFFF", font=title_font).pack(anchor="center")

    # Nav buttons
    btn_frame = tk.Frame(root, bd=0.5, relief="groove", padx=5, pady=5)
    btn_frame.grid(row=1, column=0, sticky="nsew")

    # Result area
    result_frame = tk.Frame(root, bd=0.5, relief="groove", padx=5, pady=5)
    result_frame.grid(row=1, column=1, sticky="nsew")

    def on_resize(e):
        if e.widget is root:
            # compute scale relative to your original geometry
            scale_w = e.width / base_width
            scale_h = e.height / base_height
            scale = min(scale_w, scale_h)

            # Dash (“Dashboard”) font
            new_dash = max(dash_base_size, int(dash_base_size * scale))
            dash_font.configure(size=new_dash)
            # Title (“Not-Notion!”) font
            new_title = max(title_base_size, int(title_base_size * scale))
            title_font.configure(size=new_title)
            # button font
            new_btn = max(button_base_size, int(button_base_size * scale))
            button_font.configure(size=new_btn)

    root.bind("<Configure>", on_resize)

    # Task Ops
    def show_all_tasks():
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        tasks.sort(key=lambda t: (t['date'], priority_order.get(t['priority'],1)))

        for w in result_frame.winfo_children():
            w.destroy()

        # Header in display
        header = tk.Frame(result_frame, bg='#F7FAFC')
        header.pack(fill='x', pady=(0, 10), padx=5)
        tk.Label(header,
                 text="All Tasks",
                 font=('Segoe UI', 14, 'bold'),
                 bg='#F7FAFC').pack(side='left')
        tk.Button(header,
                  text="Add Task",
                  command=open_task_dialog,
                  bg='#3182CE', fg='white',
                  relief='flat',
                  padx=14, pady=5).pack(side='right')

        # Task list
        list_container = tk.Frame(result_frame, bg='#F7FAFC')
        list_container.pack(fill='both', expand=True)

        colors = {'High': '#FF0000', 'Medium': '#FFA500', 'Low': '#00BFFF'}

        for idx, task in enumerate(tasks):
            # Card frame
            card = tk.Frame(list_container,
                            bg='white',
                            bd=1, relief='solid',
                            padx=10, pady=8)
            card.pack(fill='x', pady=5, padx=5)

            # Checkbox
            completed_var = tk.BooleanVar(value=task.get('completed', False))
            chk = tk.Checkbutton(card,
                                 variable=completed_var,
                                 command=lambda i=idx, v=completed_var: toggle_complete(i, v),
                                 bg='white',
                                 activebackground='white',
                                 borderwidth=0)
            chk.pack(side='left')

            # Texts
            text_frame = tk.Frame(card, bg='white')
            text_frame.pack(side='left', fill='x', expand=True, padx=8)

            # Task name with optional overstrike
            name_font = tkFont.Font(family='Segoe UI',
                                    size=12,
                                    weight='bold',
                                    overstrike=task.get('completed', False))
            tk.Label(text_frame,
                     text=task['name'],
                     font=name_font,
                     bg='white').pack(anchor='w')

            # Date label
            tk.Label(text_frame,
                     text=task['date'],
                     font=('Segoe UI', 10),
                     bg='white').pack(anchor='w')

            # Details / subtitle
            tk.Label(text_frame,
                     text=task.get('details', ''),
                     font=('Segoe UI', 10),
                     fg='grey',
                     bg='white').pack(anchor='w')

            # Priority pill
            pill = tk.Label(card,
                            text=task['priority'],
                            bg=colors.get(task['priority'], 'grey'),
                            fg='white',
                            font=('Segoe UI', 9),
                            padx=6, pady=2)
            pill.pack(side='right')

            # Edit/Delete buttons container
            btn_frame = tk.Frame(card, bg='white')
            btn_frame.pack(side='right', padx=5)

            ttk.Button(btn_frame,
                       text="Edit",
                       command=lambda i=idx: open_task_dialog(i)).pack(side='left')

            ttk.Button(btn_frame,
                       text="Delete",
                       command=lambda i=idx: delete_task(i)).pack(side='left', padx=(5, 0))

        # Summary bar
        total = len(tasks)
        completed = sum(1 for t in tasks if t.get('completed'))
        high = sum(1 for t in tasks if t.get('priority') == 'High')
        summary = tk.Frame(result_frame, bg='#EDF2F7', padx=5, pady=5)
        summary.pack(fill='x', pady=(10, 5))
        tk.Label(summary,
                 text=f"{total} tasks total   •   {completed} completed   •   {high} high priority",
                 font=('Segoe UI', 10),
                 fg='grey',
                 bg='#EDF2F7').pack(side='left')

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
        DateEntry(dialog, textvariable=date_var, date_pattern="yyyy-mm-dd")\
            .grid(row=1, column=1, sticky="we", padx=5, pady=5)

        # Priority
        ttk.Label(dialog, text="Priority:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        prio_var = tk.StringVar(value=tasks[index]['priority'] if index is not None else "Medium")
        ttk.Combobox(dialog, textvariable=prio_var, values=["Low","Medium","High"], state="readonly")\
            .grid(row=2, column=1, sticky="we", padx=5, pady=5)

        # Details (multiline)
        ttk.Label(dialog, text="Details:").grid(row=3, column=0, sticky="ne", padx=5, pady=5)
        details_txt = tk.Text(dialog, height=4)
        details_txt.grid(row=3, column=1, sticky="we", padx=5, pady=5)
        if index is not None:
            details_txt.insert("1.0", tasks[index].get("details",""))

        # Save/Cancel
        def save_task():
            name = name_var.get().strip()
            date = date_var.get()
            priority = prio_var.get()
            details = details_txt.get("1.0","end").strip()
            if not name:
                messagebox.showwarning("Input Error","Name cannot be empty.")
                return
            data = {"name": name, "date": date,"priority": priority,
                    "details": details, "completed": False}
            if index is None:
                tasks.append(data)
            else:
                tasks[index].update(data)
            dialog.destroy()
            show_all_tasks()

        ttk.Button(dialog, text="Save", command=save_task)\
            .grid(row=4, column=1, padx=5, pady=10)
        ttk.Button(dialog, text="Cancel",   command=dialog.destroy)\
            .grid(row=4, column=0, padx=5, pady=10)

    def delete_task(i):
        if messagebox.askyesno("Confirm Delete","Delete this task?"):
            tasks.pop(i)
            show_all_tasks()

    def toggle_complete(i,var):
        tasks[i]['completed'] = var.get()
        show_all_tasks()

    # Nav handler (just All Tasks for now)
    def on_nav_button(name):
        if name == "All Tasks":
            show_all_tasks()
        else:
            for w in result_frame.winfo_children(): w.destroy()
            ttk.Label(result_frame, text=f"'{name}' not done.", font=result_font)\
               .pack(expand=True)

    for name in ("All Tasks", "Today", "Upcoming", "High Priority", "Completed"):
        ttk.Button(btn_frame, text=name, style="Italic.TButton",
                   command=lambda n=name: on_nav_button(n))\
           .pack(fill="x", pady=2)

    show_all_tasks()

    root.mainloop()


if __name__ == "__main__":
    build_gui()
