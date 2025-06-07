import json
import os


class DataManager:
    def __init__(self, json_file):
        self.json_file = json_file

    def load_ebooks(self):
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError):
                return []
        return []

    def save_ebooks(self, ebooks):
        try:
            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump(ebooks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving ebooks: {e}")

    def count_all(self):
        return len([e for e in self.load_ebooks() if not e.get("is_deleted", False)])

    def count_read(self):
        return len([
            e for e in self.load_ebooks()
            if e.get("is_read", False) and not e.get("is_deleted", False)
        ])

    def count_deleted(self):
        return len([e for e in self.load_ebooks() if e.get("is_deleted", False)])

    def count_favorite(self):
        return len([
            e for e in self.load_ebooks()
            if e.get("is_favorite", False) and not e.get("is_deleted", False)
        ])

    def count_recently_read(self, days=7):
        import datetime
        now = datetime.datetime.now()
        count = 0
        for e in self.load_ebooks():
            last_read = e.get("last_read")
            if last_read and not e.get("is_deleted", False):
                try:
                    dt = datetime.datetime.fromisoformat(last_read)
                    if (now - dt).days <= days:
                        count += 1
                except Exception:
                    pass
        return count

    def mark_as_read(self, filename):
        ebooks = self.load_ebooks()
        for ebook in ebooks:
            if ebook.get("filename") == filename:
                ebook["is_read"] = True
                import datetime
                ebook["last_read"] = datetime.datetime.now().isoformat()
                break
        self.save_ebooks(ebooks)

    def toggle_favorite(self, filename):
        ebooks = self.load_ebooks()
        for ebook in ebooks:
            if ebook.get("filename") == filename:
                ebook["is_favorite"] = not ebook.get("is_favorite", False)
                break
        self.save_ebooks(ebooks)
        return ebooks