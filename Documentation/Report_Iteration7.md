# Testing Report: Task Manager Testing

**What was tested**
- I tested a task management system with four main parts:
  - Node: The basic task item with name, description, and priority
  - TaskQueue: Manages a list of tasks with sorting by priority
  - DataStorage: Saves and loads tasks to/from JSON files
  - Integration: How all parts work together

**How I tested**
- Node Testing

  - Created a test task with name "Test Task" and priority "Medium"
  - Checked if properties were set correctly
  - Tested marking tasks as complete
  - Tested changing priority from "Medium" to "High"
  - Tested converting a task to dictionary format

**TaskQueue Testing**

- Added multiple tasks with different priorities
- Removed a task and verified it was gone
- Checked if sorting worked (High priority tasks first)

**DataStorage Testing**

- Created test tasks and saved them to a file
- Verified the file was created with data
- Loaded tasks from the file and checked values
- Tested handling of missing files

**Integration Testing**

- Created tasks, saved them to a file
- Loaded them into a new queue
- Verified all data remained correct

**Testing tools used**

- Python's assert statements to check expected values
- File system checks to verify storage
- Print statements to show test progress

**Results**

- All tests passed successfully
- The Node component correctly stores task information
- The TaskQueue properly manages tasks and sorts by priority
- The DataStorage component reliably saves and loads tasks
- The system works properly as a whole

**Summary**
- The task manager works as expected. It can create tasks, organize them by priority, save them to files, and load them again. The code successfully passed all the tests I ran.
