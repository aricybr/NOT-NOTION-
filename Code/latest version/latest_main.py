import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import tkinter.font as tkFont
import datetime
import json, hashlib
import sys
from typing import List, Dict


class Node:
    """
    Data model for a task, with serialization support.
    """
    def __init__(self, name: str, description: str, priority: str,
                 status: bool = False, date: str = None):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = date or datetime.date.today().isoformat()

    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "date": self.due_date
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
        chk = tk.Checkbutton(
            card,
            variable=var,
            command=lambda: self._toggle(var),
            bg='white',
            activebackground='white',
            borderwidth=0,
            width=4,  # roughly 4 character-widths wide
            height=2,  # roughly 2 lines tall
            padx=6,  # inner padding
            pady=6
        )
        chk.pack(side='left', padx=4, pady=4)

        info = tk.Frame(card, bg='white')
        info.pack(side='left', fill='x', expand=True, padx=6)
        nm_font = tkFont.Font(family='Segoe UI', size=12,
                              weight='bold', overstrike=self.node.status)
        tk.Label(info, text=self.node.name, font=nm_font, bg='white').pack(anchor='w')
        tk.Label(info, text=self.node.due_date,
                 font=('Segoe UI',10), bg='white').pack(anchor='w')
        tk.Label(info, text=self.node.description,
                 font=('Segoe UI',10), fg='grey', bg='white').pack(anchor='w')

        pill = tk.Label(card, text=self.node.priority,
                        bg=colors.get(self.node.priority,'grey'), fg='white',
                        font=('Segoe UI', 9), padx=5, pady=2)
        pill.pack(side='right')

        btns = tk.Frame(card, bg='white')
        btns.pack(side='right', padx=4)
        ttk.Button(btns, text='Edit', command=self._open_edit_dialog).pack(side='left')
        ttk.Button(btns, text='Delete', command=self._delete).pack(side='left', padx=(5, 0))

    def _open_edit_dialog(self):
        dlg = tk.Toplevel(self.parent)
        dlg.transient(self.parent)
        dlg.title('Edit Task')
        dlg.grid_columnconfigure(1, weight=1)

        ttk.Label(dlg, text='Task Name:').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        name_var = tk.StringVar(value=self.node.name)
        ttk.Entry(dlg, textvariable=name_var).grid(row=0, column=1, sticky='we', padx=5)

        ttk.Label(dlg, text='Due Date:').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        date_var = tk.StringVar(value=self.node.due_date)
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
                messagebox.showwarning('Input Error','Task Name cannot be empty.')
                return
            self.node.name = name
            self.node.due_date = date_var.get()
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


class DataStorage:
    """
    Handles saving and loading Node lists to/from a JSON file.
    """
    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = filepath

    def save_tasks(self, task_queue) -> None:
        data = [node.to_dict() for node in task_queue.get_all_tasks()]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_tasks(self) -> List[Node]:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Node(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []




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


class User:
    """
    Data model for an application user, with simple password-hash authentication.
    """
    def __init__(self, username: str, password_hash: str):
        self.username = username
        self.password_hash = password_hash

    def authenticate(self, password: str) -> bool:
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash

    def change_password(self, old: str, new: str) -> bool:
        if self.authenticate(old):
            self.password_hash = hashlib.sha256(new.encode()).hexdigest()
            return True
        return False

    def to_dict(self) -> dict:
        return {"username": self.username, "password_hash": self.password_hash}


class UserStorage:
    """
    Handles saving and loading User objects to/from a JSON file.
    """
    def __init__(self, filepath: str = "users.json"):
        self.filepath = filepath

    def load_users(self) -> Dict[str, User]:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {u["username"]: User(**u) for u in data}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_users(self, users: Dict[str, User]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in users.values()], f, ensure_ascii=False, indent=2)


def prompt_login_or_register(user_storage: UserStorage) -> bool:

    users = user_storage.load_users()
    login_success = False

    root = tk.Tk()
    root.title("Welcome — Log In or Register")
    root.geometry("400x200")
    root.resizable(False, False)

    ttk.Label(root, text="Username:").pack(pady=(20, 0))
    uname = ttk.Entry(root)
    uname.pack(fill="x", padx=20)

    ttk.Label(root, text="Password:").pack(pady=(10, 0))
    pwd = ttk.Entry(root, show="*")
    pwd.pack(fill="x", padx=20)

    def do_login():
        nonlocal login_success
        u = uname.get().strip(); p = pwd.get()
        if u in users and users[u].authenticate(p):
            login_success = True
            root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def on_closing():
        # Simply destroy the window; login_success stays False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=15)
    ttk.Button(btn_frame, text="Log In",    command=do_login).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Register",  command=lambda: _open_register(root, users, user_storage)).grid(row=0, column=1, padx=10)

    root.mainloop()
    return login_success


def _open_register(parent, users, user_storage):

    reg_win = tk.Toplevel(parent)
    reg_win.title("Register New Account")
    reg_win.geometry("300x220")
    reg_win.transient(parent)

    ttk.Label(reg_win, text="New Username:").pack(pady=(15,0))
    reg_uname = ttk.Entry(reg_win)
    reg_uname.pack(fill="x", padx=20)

    ttk.Label(reg_win, text="Password:").pack(pady=(10,0))
    reg_pwd = ttk.Entry(reg_win, show="*")
    reg_pwd.pack(fill="x", padx=20)

    ttk.Label(reg_win, text="Confirm Password:").pack(pady=(10,0))
    reg_pwd_confirm = ttk.Entry(reg_win, show="*")
    reg_pwd_confirm.pack(fill="x", padx=20)

    def save_registration():
        new_u = reg_uname.get().strip()
        new_p = reg_pwd.get()
        new_pc = reg_pwd_confirm.get()
        if not new_u or not new_p:
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        if new_p != new_pc:
            messagebox.showwarning("Input Error", "Passwords must match.")
            return
        if new_u in users:
            messagebox.showwarning("Input Error", "Username already exists.")
            return

        users[new_u] = User(new_u, hashlib.sha256(new_p.encode()).hexdigest())
        user_storage.save_users(users)
        messagebox.showinfo("Success", f"User '{new_u}' registered.")
        reg_win.destroy()

    ttk.Button(reg_win, text="Create Account", command=save_registration).pack(pady=15)


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
                datetime.date.fromisoformat(n.due_date),
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
            (self.dash_font, 15),
            (self.title_font, 20),
            (self.button_font, 12),
        ):
            font_obj.configure(size=max(base_size, int(base_size * scale)))

    def show(self, name: str):
        # View switching according to navigation
        mapping = {
            "All Tasks": self.view.show_all,
            "Today": self.view.show_today,
            "Upcoming": self.view.show_upcoming,
            "High Priority": self.view.show_high_priority,
            "Completed": self.view.show_completed,
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
    # 1) Bootstrap users
    user_store = UserStorage("users.json")
    users = user_store.load_users()
    if not users:
        default = User("admin", hashlib.sha256("password".encode()).hexdigest())
        user_store.save_users({"admin": default})

    # 2) Prompt login/register
    if not prompt_login_or_register(user_store):
        # User closed or failed to log in
        sys.exit(0)

    # 3) Load tasks & start UI
    task_queue = TaskQueue()
    storage     = DataStorage("tasks.json")
    for node in storage.load_tasks():
        task_queue.add_task(node)

    MainApp(task_queue, storage)
