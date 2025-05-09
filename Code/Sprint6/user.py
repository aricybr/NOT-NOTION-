import hashlib
import json
from typing import Dict
import tkinter as tk
from tkinter import ttk, messagebox


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
