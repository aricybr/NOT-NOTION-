# Sprint5: Class Update

## Code Organization
The code is organized into separate classes, each having a specific responsibility. This modular approach ensures maintainability and scalability of the application. 
Below is a high-level summary of how the code is organized:

### Data Management:
- Node class: Represents the data (task).

- TaskQueue class: Manages tasks and sorting.

- DataStorage class: Handles saving and loading tasks from JSON.

### UI Components:

- NodeUI class: Responsible for rendering and interacting with a single task.

- PriorityTaskQueue class: Displays tasks based on various filters.

### Application Flow:

- MainApp class: Sets up the application window, UI components, and manages the application’s flow.


## Class Breakdown
### 1. Node Class: 
represents a task in the system. Each task contains essential information like name, description, priority, status (completed or not), and creation date.

- **Attributes:**
  - vname: The name of the task (string).
  - description: The detailed description of the task (string).
  - priority: Task priority (Low, Medium, High).
  - status: A boolean indicating whether the task is completed or not.
  - creation_date: The date when the task was created.
- **Methods:**
  - mark_complete: Sets the status of the task to True (completed).
  - change_priority: Allows changing the task's priority.
  - to_dict: Serializes the task into a dictionary format for saving/loading purposes.

### 2. NodeUI Class: 
is responsible for rendering a task as a user interface (UI) element (card) that allows interaction. It provides functionalities like toggling the task’s completion status, editing, and deleting tasks.

- **Attributes:**
  - parent: The parent Tkinter widget that will hold this UI element.
  - node: The Node object associated with this UI card.
  - storage: The storage object responsible for saving the tasks.
  - refresh: A callback function that refreshes the task list UI after any change.

- **Methods:**
  - _render: Displays the task UI as a card with labels for task name, description, priority, and buttons for editing and deleting.
  - _open_edit_dialog: Opens a dialog for editing the task's properties (name, description, priority, and date).
  - _delete: Deletes the task after user confirmation.
  - _toggle: Toggles the task's completion status and updates the UI accordingly.

### 3. PriorityTaskQueue Class: 
responsible for filtering and displaying tasks based on various criteria, such as all tasks, tasks for today, upcoming tasks, high-priority tasks, and completed tasks.

- **Attributes:**
  - parent: The parent widget where the task cards will be displayed.
  - task_queue: The TaskQueue object containing all tasks.
  - storage: The storage object for saving tasks.
  - result_font: Font used for displaying task-related information.

- **Methods:**
  - show_all: Displays all tasks in the task queue.
  - show_today: Displays only the tasks that were created today.
  - show_upcoming: Displays tasks due within the next 3 days.
  - show_high_priority: Displays tasks with high priority.
  - show_completed: Displays tasks that are marked as completed.
  - _display: Clears the UI and renders tasks based on the selected filter.
  - _refresh: Refreshes the task display based on the selected filter.
  - _open_add_dialog: Opens a dialog for creating a new task.

## 4. TaskQueue Class: 
manages the logic related to adding, removing, and sorting tasks in the queue. It ensures tasks are organized according to their creation date and priority.

- **Attributes:**
  - _nodes: A list that holds all the Node objects (tasks).

- **Methods:**
  - add_task: Adds a task to the queue and sorts the tasks based on priority and creation date.
  - remove_task: Removes a specific task from the queue.
  - get_all_tasks: Returns all tasks in the queue.
  - _sort: Sorts the tasks based on their creation date and priority.

## 5. DataStorage Class: 
is responsible for saving and loading tasks to/from a JSON file. This class allows the persistence of tasks across application sessions.

- **Attributes:**
  - filepath: The path of the JSON file where tasks are saved.

- **Methods:**
  - save_tasks: Saves all tasks in the task queue to the specified JSON file.
  - load_tasks: Loads tasks from the JSON file and converts them back into Node objects.

## 6. MainApp Class: 
is the core of the application, responsible for setting up the Tkinter window, managing layout, handling UI components, and linking everything together (task management, storage, and display).

- **Attributes:**
  - scr_width, scr_height: Initial window dimensions.
  - task_queue: The TaskQueue instance holding all tasks.
  - storage: The DataStorage instance for task persistence.
  - root: The Tkinter root window.
  - view: The PriorityTaskQueue instance for displaying tasks.

- **Methods:**
  - _setup_fonts: Sets up the fonts used throughout the app.
  - _build_layout: Builds the UI layout, including the dashboard, title, navigation buttons, and task display area.
  - _on_resize: Adjusts the font size and layout when the window is resized.
  - show: Switches the task display based on the selected navigation button.
