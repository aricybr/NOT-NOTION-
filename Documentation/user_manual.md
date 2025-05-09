# Not-Notion Task Manager User Manual

## 1. Introduction

Not-Notion is a cross-platform desktop application for personal task management. It provides an intuitive interface for creating, organizing, and tracking tasks by due date, priority, and completion status. Tasks are stored locally in JSON files, ensuring persistence between sessions.

## 2. System Requirements

- **Operating System:** Windows, macOS, or Linux
- **Python Version:** 3.7 or later
- **Required Packages:** `tkinter`, `tkcalendar`, `hashlib`, `json`

## 3. Installation

1. **Clone or Download** the project repository to your local machine.
2. **Install dependencies** (if not already present)
3. **Verify** that `tkinter` is available (usually included with standard Python distributions).

## 4. Launching the Application

1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the main script:
4. The **Login / Register** window appears. If running for the first time, a default admin account is created (`username: admin`, `password: password`).

## 5. User Authentication

### 5.1 Registering a New Account

1. Click **Register** in the login window.
2. Enter a new username, password, and confirm the password.
3. Click **Create Account**. A success message confirms registration.

### 5.2 Logging In

1. In the login window, enter your **Username** and **Password**.
2. Click **Log In**. If credentials are valid, the main dashboard opens. Invalid credentials trigger an error message.
3. Closing or canceling the login window exits the application.

## 6. Main Dashboard Overview

Upon successful login, the main window displays two panels:

- **Left Panel (Dashboard & Navigation):**

  - Dashboard header
  - Navigation buttons:

    - All Tasks
    - Today
    - Upcoming
    - High Priority
    - Completed

- **Right Panel (Task View):**

  - Displays task cards according to the selected view.
  - The header shows the view title and an **Add Task** button.
  - A footer summary indicates total tasks, completed tasks, and high-priority count.

## 7. Navigating Task Views

- **All Tasks:** Shows every task regardless of status.
- **Today's Tasks:** Lists tasks due on the current date and not yet completed.
- **Upcoming Tasks:** Tasks due within the next three days, excluding completed tasks.
- **High Priority Tasks:** All incomplete tasks marked as High priority.
- **Completed Tasks:** All tasks marked as complete (regardless of due date).

Click any navigation button to switch views. The view title updates accordingly.

## 8. Task Management

### 8.1 Adding a New Task

1. In any view, click **Add Task**.
2. In the dialog, fill in:
   - **Task Name** (required)
   - **Due Date** (defaults to today; use the calendar picker)
   - **Priority** (Low, Medium, High)
   - **Description** (optional details)
3. Click **Save**. The task appears in the current view and is persisted to `tasks.json`.

### 8.2 Editing a Task

1. On the task card, click **Edit**.
2. In the Edit dialog, modify any field.
3. Click **Save**. Changes update immediately and are saved.

### 8.3 Deleting a Task

1. Click **Delete** on a task card.
2. Confirm the deletion.
3. The task is removed and the list refreshes.

### 8.4 Marking Tasks Complete/In Progress

- Click the checkbox on the task card to toggle completion.
- Completed tasks move into the **Completed** view and are shown with strikethrough text.

## 9. Task Card Details

Each task card displays:

- **Checkbox:** Toggle status.
- **Task Name:** Bold; strikethrough if completed.
- **Due Date:** Under the name.
- **Description:** In smaller, grey text.
- **Priority Pill:** Color-coded (High = red, Medium = orange, Low = blue).
- **Edit / Delete Buttons** on the right.

## 10. Application Behavior

- **Sorting:** Tasks are sorted by due date (earliest first) and then by priority (High → Medium → Low).
- **Responsive Design:** Resizing the window scales fonts proportionally for readability.
- **Persistence:** All tasks and user accounts are stored in JSON files (`tasks.json`, `users.json`).

## 11. Troubleshooting & FAQs

- **Login fails:** Ensure correct credentials or register a new account.
- **Tasks not saving:** Check file permissions for `tasks.json` in the application directory.
- **UI layout issues:** Resize or maximize the window; fonts adjust automatically.
