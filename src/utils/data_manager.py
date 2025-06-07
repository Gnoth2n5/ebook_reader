import json
import os


class DataManager:
    def __init__(self, json_file):
        self.json_file = json_file

    def load_ebooks(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_ebooks(self, ebooks):
        with open(self.json_file, "w") as f:
            json.dump(ebooks, f, indent=4)

    def count_all(self):
        return len(self.load_ebooks())

    def count_read(self):
        return len(
            [
                e
                for e in self.load_ebooks()
                if e.get("is_read") and not e.get("is_deleted")
            ]
        )

    def count_deleted(self):
        return len([e for e in self.load_ebooks() if e.get("is_deleted")])

    def count_favorite(self):
        return len(
            [
                e
                for e in self.load_ebooks()
                if e.get("is_favorite") and not e.get("is_deleted")
            ]
        )

    def count_recently_read(self, days=7):
        import datetime

        now = datetime.datetime.now()
        count = 0
        for e in self.load_ebooks():
            last_read = e.get("last_read")
            if last_read and not e.get("is_deleted"):
                try:
                    dt = datetime.datetime.fromisoformat(last_read)
                    if (now - dt).days <= days:
                        count += 1
                except Exception:
                    pass
        return count
