## Sprint6: User Authentication Module Documentation

This document explains the components and flow of the User authentication code, which provides hashing-based password authentication, user data persistence, and a simple Tkinter-based GUI for login and registration.


## 1. Overview

The module consists of:

- **User class**: Represents a user, storing username and password hash, and provides authentication and password change methods.
- **UserStorage class**: Handles loading and saving User data to a JSON file (users.json by default).
- **prompt_login_or_registe function**: Launches a Tkinter window allowing existing users to log in or new users to register.
- **_open_register helper**: Displays a registration dialog where new users can create accounts.

This setup ensures credentials are never stored in plain text and provides a minimal GUI for user interaction.



## 2. User Class

- **Constructor**: Accepts a username and a pre-computed SHA-256 password_hash.
- **authenticate(password)**: Hashes the input password and compares it to the stored hash, returning True if they match.
- **change_password(old, new)**: Verifies the old password; if valid, updates password_hash to the SHA-256 of the new password. Returns True on success.
- **to_dict()**: Serializes the user to a dictionary for JSON storage:

## 3. UserStorage Class

- **Constructor**: Accepts filepath for the JSON storage file. Default is users.json.
- **load_users()**:

  - Tries to open and parse the JSON file.
  - Constructs a User instance for each entry.
  - Returns a dict mapping username to User.
  - If the file is missing or invalid JSON, returns an empty dict.
- **save_users(users)**:

  - Accepts a dict of username: User entries.
  - Writes a list of user dicts (User.to_dict()) to the JSON file with indentation for readability.


## 4. Login/Register GUI Flow

### prompt_login_or_register(user_storage)

1. **Load Users**: Calls user_storage.load_users().
2. **Tkinter Setup**: Creates a non-resizable 400×200 window titled "Welcome — Log In or Register".
3. **Input Widgets**: Username and password fields (ttk.Entry).
4. **Buttons**:
   - **Log In**: Calls do_login() which:
     - Reads inputs.
     - Checks if username exists and calls User.authenticate.
     - On success, sets login_success = True and closes window; otherwise shows an error.
   - **Register**: Opens the registration dialog via _open_registe.
5. **Window Closing**: Overwrites the close action so that simply destroying the window leaves login_success = False.
6. **Return Value**: Blocks with root.mainloop() until closed, then returns login_success (True if login succeeded).

### _open_register(parent, users, user_storage)

1. **Create Toplevel**: Opens a child window titled "Register New Account" (300×220).
2. **Input Fields**: New username, password, and password confirmation.
3. **save_registration()**: Validates inputs:

   - All fields required.
   - Passwords must match.
   - Username must be unique.
   - On success:
     1. Creates new User with SHA-256 hashed password.
     2. Adds to users dict and calls user_storage.save_users().
     3. Shows success message and closes registration dialog.
4. **Button**: "Create Account" triggers save_registration().
