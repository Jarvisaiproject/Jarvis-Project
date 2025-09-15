import json
import os
import shutil
from datetime import datetime

class NotesManager:
    def __init__(self, file_path="data/notes.json"):
        self.file_path = file_path
        os.makedirs("data", exist_ok=True)
        os.makedirs("data/backup", exist_ok=True)
        self.notes = self.load()

    def backup_file(self):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_name = f"data/backup/notes_{timestamp}.json"
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
        return {"daily": [], "weekly": [], "monthly": [], "yearly": []}

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.notes, f, indent=4)

    def add(self, category, note):
        if category not in self.notes:
            self.notes[category] = []
        self.notes[category].append(note)
        self.save()

    def get(self, category):
        return self.notes.get(category, [])

    def get_all(self):
        return self.notes

    def restore_last_backup(self):
        backup_folder = "data/backup"
        if not os.path.exists(backup_folder):
            return "No backup folder found."

        backups = [f for f in os.listdir(backup_folder) if f.startswith("notes_")]
        if not backups:
            return "No notes backups found."

        backups.sort(reverse=True)
        latest = backups[0]
        backup_path = os.path.join(backup_folder, latest)

        shutil.copy(backup_path, self.file_path)
        self.notes = self.load()
        return f"Restored notes from {latest}"
    
    def delete(self, category, keyword):
        if category not in self.notes:
            return 0
        before = len(self.notes[category])
        self.notes[category] = [
            n for n in self.notes[category] if keyword.lower() not in n.lower()
        ]
        self.save()
        after = len(self.notes[category])
        return before - after

    def clear(self, category=None):
        if category:
            count = len(self.notes.get(category, []))
            self.notes[category] = []
        else:
            count = sum(len(v) for v in self.notes.values())
            self.notes = {"daily": [], "weekly": [], "monthly": [], "yearly": []}
        self.save()
        return count

