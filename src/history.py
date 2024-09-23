import json, os, datetime


class History:
    def __init__(self):
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists("data/history.json"):
            with open("data/history.json", "w", encoding="utf8") as f:
                json.dump({"history": []}, f, indent=2, ensure_ascii=False)
        with open("data/data.json", encoding="utf8") as f:
            self.history = json.load(f)["history"]

    def append(self, item):
        self.history.append(item)
        self.history = sorted(
            self.history,
            key=lambda x: datetime.strptime(x["time"], "%Y-%m-%d %H:%M:%S"),
            reverse=True,
        )
        self.save()

    def save(self):
        with open("data/history.json", "w", encoding="utf8") as f:
            json.dump({"history": self.history}, f, indent=2, ensure_ascii=False)
