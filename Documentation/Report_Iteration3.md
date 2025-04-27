## Sprint3: Initial GUI Setup

### Objects
- build_gui():
This function creates and manages the main window and layout of the Not-Notion application.

- Variables (Inside build_gui):
  - root — the main tkinter window.
  - dash_frame — frame container for the Dashboard title.
  - title_frame — frame container for the Not-Notion title.
  - btn_frame — frame container for sidebar buttons (All Tasks, Today, etc.).
  - result_frame — frame container for displaying output after button clicks (currently static text).

### Functions
- build_gui()
  - Creates the main tkinter window with a fixed size.
  - Configures a 2x2 grid layout (top/bottom, left/right).

- Adds:
  - A Dashboard title area.
  - A Not-Notion title area.
  - A sidebar with task buttons (All Tasks, Today, Upcoming, High Priority, Completed).
  - A main content area for displaying results.

- Sets up the window to loop and stay open (root.mainloop()).

### Driver
- Main Execution Block (if __name__ == "__main__":): 
Calls build_gui() to launch the GUI.

### Current Limitations
- Buttons do not have attached functionality yet (they do not trigger actions).
- No user login or authentication features yet.
- No task management logic (adding, removing, changing tasks) yet.
- No data storage for saving or loading tasks.

### Planned Next Steps
- Add command actions to the task buttons to control tasks.
- Create a task management system linked to the GUI.
- Implement save/load features for persistence.
- Add user authentication system (optional enhancement).


