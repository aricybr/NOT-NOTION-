import datetime
import os
from node import Node
from data_storage import DataStorage
from main import TaskQueue


# Test Node functionality
def test_node():
    # Create a test node
    test_node = Node(
        name="Test Task",
        description="This is a test task",
        priority="Medium"
    )

    # Test node initialization
    assert test_node.name == "Test Task", "Node name incorrectly set"
    assert test_node.description == "This is a test task", "Node description incorrectly set"
    assert test_node.priority == "Medium", "Node priority incorrectly set"
    assert test_node.status is False, "Node status should default to False"
    assert test_node.creation_date == datetime.date.today().isoformat(), "Default date should be today"

    # Test marking complete
    test_node.mark_complete()
    assert test_node.status is True, "Node should be marked complete"

    # Test changing priority
    test_node.change_priority("High")
    assert test_node.priority == "High", "Priority should be changed to High"

    # Test to_dict method
    node_dict = test_node.to_dict()
    assert isinstance(node_dict, dict), "to_dict should return a dictionary"
    assert node_dict["name"] == "Test Task", "Dictionary should contain correct name"
    assert node_dict["priority"] == "High", "Dictionary should contain correct priority"

    print("All Node tests passed!")


# Test TaskQueue functionality
def test_task_queue():
    task_queue = TaskQueue()

    # Create test nodes
    node1 = Node("Task 1", "Description 1", "High", False, "2025-05-01")
    node2 = Node("Task 2", "Description 2", "Medium", False, "2025-05-01")
    node3 = Node("Task 3", "Description 3", "Low", False, "2025-05-02")

    # Test adding tasks
    task_queue.add_task(node1)
    task_queue.add_task(node2)
    task_queue.add_task(node3)

    assert len(task_queue.get_all_tasks()) == 3, "Should have 3 tasks in queue"

    # Test removing a task
    task_queue.remove_task(node2)
    assert len(task_queue.get_all_tasks()) == 2, "Should have 2 tasks after removal"
    assert node2 not in task_queue.get_all_tasks(), "Removed task should not be in queue"

    # Test sorting
    node4 = Node("Task 4", "Description 4", "High", False, "2025-05-01")
    task_queue.add_task(node4)

    tasks = task_queue.get_all_tasks()
    assert tasks[0].priority == "High" and tasks[1].priority == "High", "High priority tasks should come first"
    assert tasks[2].priority == "Low", "Low priority should come last"

    print("All TaskQueue tests passed!")


# Test DataStorage functionality
def test_data_storage():
    test_file = "test_tasks.json"
    storage = DataStorage(test_file)
    task_queue = TaskQueue()

    # Add test tasks
    task_queue.add_task(Node("Test Task 1", "Description 1", "High"))
    task_queue.add_task(Node("Test Task 2", "Description 2", "Medium"))

    # Test saving
    storage.save_tasks(task_queue)
    assert os.path.exists(test_file), "File should be created when saving tasks"
    assert os.path.getsize(test_file) > 0, "File should contain data"

    # Test loading
    loaded_nodes = storage.load_tasks()
    assert len(loaded_nodes) == 2, "Should load 2 tasks"
    assert loaded_nodes[0].name == "Test Task 1", "First task should have correct name"
    assert loaded_nodes[0].priority == "High", "First task should have correct priority"


    os.remove(test_file)
    empty_nodes = storage.load_tasks()
    assert isinstance(empty_nodes, list), "Should return a list"
    assert len(empty_nodes) == 0, "Should return an empty list for non-existent file"

    print("All DataStorage tests passed!")


# Basic integration test
def test_integration():
    test_file = "integration_test.json"
    storage = DataStorage(test_file)
    task_queue = TaskQueue()

    # Add and save tasks
    task_queue.add_task(Node("Integration Test 1", "Test Description 1", "High"))
    task_queue.add_task(Node("Integration Test 2", "Test Description 2", "Low"))
    storage.save_tasks(task_queue)

    # Load tasks into a new queue
    new_queue = TaskQueue()
    loaded_nodes = storage.load_tasks()
    for node in loaded_nodes:
        new_queue.add_task(node)

    tasks = new_queue.get_all_tasks()
    assert len(tasks) == 2, "Should have 2 tasks after load"
    assert tasks[0].name == "Integration Test 1", "First task should have correct name"

    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)

    print("All integration tests passed!")


# Run all tests
if __name__ == "__main__":
    test_node()
    test_task_queue()
    test_data_storage()
    test_integration()
    print("All tests passed successfully!")
