import json, os, datetime


class History:
    def __init__(self):
        self.time_format = "%Y-%m-%d %H:%M:%S"
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists("data/history.json"):
            with open("data/history.json", "w", encoding="utf8") as f:
                json.dump({}, f, indent=2, ensure_ascii=False)
        with open("data/history.json", "r", encoding="utf8") as f:
            self.history = json.load(f)

    def append(self, ID, name, price):
        now = datetime.datetime.now().strftime(self.time_format)
        item = {
            "name": name,
            "price": price,
            "time": now,
        }
        if ID not in self.history:
            self.history[ID] = []
        self.history[ID].append(item)
        self.history[ID] = sorted(
            self.history[ID],
            key=lambda x: datetime.datetime.strptime(x["time"], self.time_format),
            reverse=True,
        )
        self.save()
        return now

    def save(self):
        with open("data/history.json", "w", encoding="utf8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)
