import json, os, datetime


class History:
    def __init__(self, filename="data/history.json"):
        self.filename = filename
        self.time_format = "%Y-%m-%d %H:%M:%S"
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf8") as f:
                json.dump({}, f, indent=2, ensure_ascii=False)

    def load(self):
        with open(self.filename, "r", encoding="utf8") as f:
            self.history = json.load(f)

    def save(self):
        with open(self.filename, "w", encoding="utf8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def append(self, ID, name, price):
        now = datetime.datetime.now().strftime(self.time_format)
        item = {
            "name": name,
            "price": price,
            "time": now,
        }
        ID = str(ID)
        self.load()
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

    def get_channels(self):
        self.load()
        return self.history.keys()
