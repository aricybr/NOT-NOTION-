import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import tkinter.font as tkFont

class Node:
    """
    Data model for a task, with serialization support.
    """
    def __init__(self, name: str, description: str, priority: str,
                 status: bool = False, creation_date: str = None):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.creation_date = creation_date or datetime.date.today().isoformat()

    def mark_complete(self):
        self.status = True

    def change_priority(self, new_priority: str):
        self.priority = new_priority

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "creation_date": self.creation_date
        }

class NodeUI:
    """
    Renders a single Node as a card with edit, delete, and toggle functionality.
    """
    def __init__(self, parent, node: Node, storage, refresh_callback):
        self.parent = parent
        self.node = node
        self.storage = storage
        self.refresh = refresh_callback
        self._render()

    def _render(self):
        colors = {'High': '#FF0000', 'Medium': '#FFA500', 'Low': '#00BFFF'}
        card = tk.Frame(self.parent, bg='white', bd=1, relief='solid', padx=8, pady=6)
        card.pack(fill='x', pady=4, padx=4)

        var = tk.BooleanVar(value=self.node.status)
        chk = tk.Checkbutton(card, variable=var,
                             command=lambda: self._toggle(var),
                             bg='white', activebackground='white', borderwidth=0)
        chk.pack(side='left')

        info = tk.Frame(card, bg='white')
        info.pack(side='left', fill='x', expand=True, padx=6)
        nm_font = tkFont.Font(family='Segoe UI', size=12,
                              weight='bold', overstrike=self.node.status)
        tk.Label(info, text=self.node.name, font=nm_font, bg='white').pack(anchor='w')
        tk.Label(info, text=self.node.creation_date,
                 font=('Segoe UI',10), bg='white').pack(anchor='w')
        tk.Label(info, text=self.node.description,
                 font=('Segoe UI',10), fg='grey', bg='white').pack(anchor='w')

        pill = tk.Label(card, text=self.node.priority,
                        bg=colors.get(self.node.priority,'grey'), fg='white',
                        font=('Segoe UI',9), padx=5, pady=2)
        pill.pack(side='right')

        btns = tk.Frame(card, bg='white')
        btns.pack(side='right', padx=4)
        ttk.Button(btns, text='Edit', command=self._open_edit_dialog).pack(side='left')
        ttk.Button(btns, text='Delete', command=self._delete).pack(side='left', padx=(5,0))

    def _open_edit_dialog(self):
        dlg = tk.Toplevel(self.parent)
        dlg.transient(self.parent)
        dlg.title('Edit Task')
        dlg.grid_columnconfigure(1, weight=1)

        ttk.Label(dlg, text='Name:').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        name_var = tk.StringVar(value=self.node.name)
        ttk.Entry(dlg, textvariable=name_var).grid(row=0, column=1, sticky='we', padx=5)

        ttk.Label(dlg, text='Date:').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        date_var = tk.StringVar(value=self.node.creation_date)
        DateEntry(dlg, textvariable=date_var,
                  date_pattern='yyyy-mm-dd').grid(row=1, column=1, sticky='we', padx=5)

        ttk.Label(dlg, text='Priority:').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        prio_var = tk.StringVar(value=self.node.priority)
        ttk.Combobox(dlg, textvariable=prio_var,
                     values=['Low','Medium','High'], state='readonly').grid(
            row=2, column=1, sticky='we', padx=5)

        ttk.Label(dlg, text='Description:').grid(row=3, column=0,
                                                  sticky='ne', padx=5, pady=5)
        desc_txt = tk.Text(dlg, height=4)
        desc_txt.grid(row=3, column=1, sticky='we', padx=5)
        desc_txt.insert('1.0', self.node.description)

        def save():
            name = name_var.get().strip()
            if not name:
                messagebox.showwarning('Input Error','Name cannot be empty.')
                return
            self.node.name = name
            self.node.creation_date = date_var.get()
            self.node.priority = prio_var.get()
            self.node.description = desc_txt.get('1.0','end').strip()
            self.storage.save_tasks(self.refresh.__self__.task_queue)
            dlg.destroy()
            self.refresh()

        ttk.Button(dlg, text='Save', command=save).grid(row=4, column=1, padx=5, pady=10)

    def _delete(self):
        if messagebox.askyesno('Confirm Delete','Delete this task?'):
            self.refresh.__self__.task_queue.remove_task(self.node)
            self.storage.save_tasks(self.refresh.__self__.task_queue)
            self.refresh()

    def _toggle(self, var):
        self.node.status = var.get()
        self.storage.save_tasks(self.refresh.__self__.task_queue)
        self.refresh()
