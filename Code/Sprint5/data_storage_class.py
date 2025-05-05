import json
from node import Node

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

    def load_tasks(self) -> list[Node]:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Node(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
