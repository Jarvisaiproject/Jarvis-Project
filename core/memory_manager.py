import json
import os
import shutil
from datetime import datetime

class MemoryManager:
    def __init__(self, file_path="data/memory.json"):
        self.file_path = file_path
        os.makedirs("data", exist_ok=True)
        os.makedirs("data/backup", exist_ok=True)
        self.memory = self.load()

    def backup_file(self):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_name = f"data/backup/memory_{timestamp}.json"
            shutil.copy(self.file_path, backup_name)

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
            except json.JSONDecodeError:
                self.backup_file()
        return {}

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.memory, f, indent=4)

    def set(self, key, value):
        self.memory[key] = value
        self.save()

    def get(self, key, default=None):
        return self.memory.get(key, default)

    def get_all(self):
        return self.memory

    def restore_last_backup(self):
        backup_folder = "data/backup"
        if not os.path.exists(backup_folder):
            return "No backup folder found."

        backups = [f for f in os.listdir(backup_folder) if f.startswith("memory_")]
        if not backups:
            return "No memory backups found."

        backups.sort(reverse=True)
        latest = backups[0]
        backup_path = os.path.join(backup_folder, latest)

        shutil.copy(backup_path, self.file_path)
        self.memory = self.load()
        return f"Restored memory from {latest}"
    
    def delete(self, key):
        if key in self.memory:
            del self.memory[key]
            self.save()
            return True
        return False

    def clear(self):
        count = len(self.memory)
        self.memory = {}
        self.save()
        return count

