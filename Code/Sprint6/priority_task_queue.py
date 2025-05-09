import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
from node import NodeUI, Node

class PriorityTaskQueue:
    """
    Filters and displays tasks in a parent frame using NodeUI cards.
    """
    def __init__(self, parent, task_queue, storage, result_font):
        self.parent = parent
        self.task_queue = task_queue
        self.storage = storage
        self.result_font = result_font
        self._last_view = self.show_all

    def show_all(self):
        # only unfinished tasks
        nodes = [n for n in self.task_queue.get_all_tasks()]
        self._display(nodes, "All Tasks")
        self._last_view = self.show_all

    def show_today(self):
        today = datetime.date.today().isoformat()
        nodes = [
            n for n in self.task_queue.get_all_tasks()
            if n.due_date == today and not n.status
        ]
        self._display(nodes, "Today's Tasks")
        self._last_view = self.show_today

    def show_upcoming(self):
        today = datetime.date.today()
        end = today + datetime.timedelta(days=3)
        nodes = [
            n for n in self.task_queue.get_all_tasks()
            if today <= datetime.date.fromisoformat(n.due_date) <= end
               and not n.status
        ]
        self._display(nodes, "Upcoming Tasks")
        self._last_view = self.show_upcoming

    def show_high_priority(self):
        nodes = [
            n for n in self.task_queue.get_all_tasks()
            if n.priority == 'High' and not n.status
        ]
        self._display(nodes, "High Priority Tasks")
        self._last_view = self.show_high_priority

    def show_completed(self):
        # this one stays the same
        nodes = [n for n in self.task_queue.get_all_tasks() if n.status]
        self._display(nodes, "Completed Tasks")
        self._last_view = self.show_completed

    def _display(self, nodes, title):
        # Clear existing UI
        for w in self.parent.winfo_children():
            w.destroy()

        # Header
        header = tk.Frame(self.parent, bg="#F7FAFC")
        header.pack(fill="x", pady=5, padx=5)
        tk.Label(header, text=title,
                 font=("Segoe UI", 20, 'bold'), bg="#F7FAFC").pack(side='left')
        tk.Button(header, text="Add Task", bg="#3182CE", fg='white',
                  relief='flat', font=20, command=self._open_add_dialog).pack(side='right')

        # Task cards
        list_frame = tk.Frame(self.parent, bg="#F7FAFC")
        list_frame.pack(fill="both", expand=True)
        for node in nodes:
            NodeUI(list_frame, node, self.storage, self._refresh)

        # Footer summary
        total = len(nodes)
        completed = sum(n.status for n in nodes)
        highp = sum(n.priority == 'High' for n in nodes)
        summary = tk.Frame(self.parent, bg='#EDF2F7', padx=5, pady=5)
        summary.pack(fill='x', pady=(8,4))
        tk.Label(summary,
                 text=f"{total} tasks • {completed} completed • {highp} high priority",
                 font=('Segoe UI',10), fg='grey', bg='#EDF2F7').pack(side='left')

    def _refresh(self):
        self._last_view()

    def _open_add_dialog(self):
        dlg = tk.Toplevel(self.parent)
        dlg.transient(self.parent)
        dlg.title('Create Task')
        dlg.grid_columnconfigure(1, weight=1)

        # Form fields
        ttk.Label(dlg, text='Task Name:').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dlg, textvariable=name_var).grid(row=0, column=1, sticky='we', padx=5)

        ttk.Label(dlg, text='Due Date:').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        date_var = tk.StringVar(value=datetime.date.today().isoformat())
        DateEntry(dlg, textvariable=date_var, date_pattern='yyyy-mm-dd')\
            .grid(row=1, column=1, sticky='we', padx=5)

        ttk.Label(dlg, text='Priority:').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        prio_var = tk.StringVar(value='Medium')
        ttk.Combobox(dlg, textvariable=prio_var,
                     values=['Low','Medium','High'], state='readonly')\
            .grid(row=2, column=1, sticky='we', padx=5)

        ttk.Label(dlg, text='Description:').grid(row=3, column=0,
                                                  sticky='ne', padx=5, pady=5)
        desc_txt = tk.Text(dlg, height=4)
        desc_txt.grid(row=3, column=1, sticky='we', padx=5)

        def save_new():
            name = name_var.get().strip()
            if not name:
                messagebox.showwarning('Input Error', 'Task Name cannot be empty.')
                return
            # Explicitly use Node class for creation
            new_node = Node(
                name,
                desc_txt.get('1.0', 'end').strip(),
                prio_var.get(),
                False,
                date_var.get()
            )
            self.task_queue.add_task(new_node)
            self.storage.save_tasks(self.task_queue)
            dlg.destroy()
            self._refresh()

        ttk.Button(dlg, text='Save', command=save_new).grid(row=4, column=1, padx=5, pady=10)
