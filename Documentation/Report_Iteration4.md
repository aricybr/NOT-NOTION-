## Sprint4: Code-Add Task Function

### Function
- build_gui(): Initializes the root window, frames, font objects, and event bindings.
  
- on_resize(e): Dynamically scales font sizes as the window resizes. Uses the original 600×400 window as a baseline.
  
- show_all_tasks(): Main renderer for task cards in the display area.
  - Sorts tasks by date and priority
  - Creates a card for each task:
    - Checkbox (completed)
    - Name (with strikethrough if completed)
    - Date, details, priority pill
    - Edit/Delete buttons
  - Displays a summary bar at the bottom

- open_task_dialog(index=None): Handles both task creation and editing.
  - Centers popup over main window
  - Pre-fills task data if editing
  - Fields: name, date, priority, details
  - Saves to global tasks list

- delete_task(i): Prompts the user for confirmation and removes a task from the list.

- toggle_complete(i, var): Toggles the "completed" status of a task when the checkbox is clicked.

- on_nav_button(name): Switches views depending on the selected navigation button. (Currently, only "All Tasks" shows actual content.)

### Features Implemented
- Responsive design (font scaling)
- Add/Edit/Delete tasks
- Completion tracking with checkboxes
- Task sorting (by date, then priority)
- Priority indicators (color pills)
- Summary bar (counts total, completed, and high priority)
- Centered popup dialogs

### Planned Enhancements
- Add file-based or database-based task storage
- Implement filtering for "Today", "Upcoming", etc.
- Add theme customization (dark/light mode)
- Implement user login and session features
