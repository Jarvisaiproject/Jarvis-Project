import json
import os
import shutil
from datetime import datetime

class HistoryManager:
    def __init__(self, file_path="data/history.json", limit=500, archive_size=300):
        self.file_path = file_path
        self.limit = limit
        self.archive_size = archive_size
        os.makedirs("data", exist_ok=True)
        os.makedirs("data/backup", exist_ok=True)
        os.makedirs("data/archive", exist_ok=True)  # new folder for archive
        self.history = self.load()

    def backup_file(self):
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_name = f"data/backup/history_{timestamp}.json"
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
        return []

    def save(self):
        # Rotate if history grows too big
        if len(self.history) > self.limit:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            archive_name = f"data/archive/history_archive_{timestamp}.json"

            # Take the oldest `archive_size` entries
            old_entries = self.history[:self.archive_size]

            # Save them into one archive file
            with open(archive_name, "w") as f:
                json.dump(old_entries, f, indent=4)

            # Keep the rest
            self.history = self.history[self.archive_size:]

        # Always save the current history file
        with open(self.file_path, "w") as f:
            json.dump(self.history, f, indent=4)

    def add(self, user_input, jarvis_response):
        entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "you": user_input,
            "jarvis": jarvis_response
        }
        self.history.append(entry)
        self.save()

    def get_all(self):
        return self.history

    def restore_last_backup(self):
        backup_folder = "data/backup"
        if not os.path.exists(backup_folder):
            return "No backup folder found."

        backups = [f for f in os.listdir(backup_folder) if f.startswith("history_")]
        if not backups:
            return "No history backups found."

        backups.sort(reverse=True)
        latest = backups[0]
        backup_path = os.path.join(backup_folder, latest)

        shutil.copy(backup_path, self.file_path)
        self.history = self.load()
        return f"Restored history from {latest}"
    
    def delete(self, keyword):
        before = len(self.history)
        self.history = [
            h for h in self.history 
            if keyword.lower() not in h["you"].lower() and keyword.lower() not in h["jarvis"].lower()
        ]
        self.save()
        after = len(self.history)
        return before - after

    def clear(self):
        count = len(self.history)
        self.history = []
        self.save()
        return count

