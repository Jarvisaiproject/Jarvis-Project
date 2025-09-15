import json
import os
from datetime import datetime

class SummariesManager:
    def __init__(self, file_path="data/summaries.json"):
        self.file_path = file_path
        os.makedirs("data", exist_ok=True)
        self.summaries = self.load()

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
            except json.JSONDecodeError:
                return []
        return []

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.summaries, f, indent=4)

    def add(self, query, source, summary):
        entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "query": query,
            "source": source,
            "summary": summary
        }
        self.summaries.append(entry)
        self.save()

    def get_all(self):
        return self.summaries

    def search(self, keyword):
        results = [
            s for s in self.summaries 
            if keyword.lower() in s["summary"].lower() or keyword.lower() in s["query"].lower()
        ]
        return results if results else []
    
    def delete(self, keyword):
        before = len(self.summaries)
        self.summaries = [
            s for s in self.summaries 
            if keyword.lower() not in s["summary"].lower() 
            and keyword.lower() not in s["query"].lower()
        ]
        self.save()
        after = len(self.summaries)
        return before - after  # number of deleted summaries

    def clear(self):
        count = len(self.summaries)
        self.summaries = []
        self.save()
        return count

