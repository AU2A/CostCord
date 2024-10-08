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
            self.data = json.load(f)

    def save(self):
        with open(self.filename, "w", encoding="utf8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def append(self, ID, name, price):
        now = datetime.datetime.now().strftime(self.time_format)
        if name == "測試":
            return now
        item = {
            "name": name,
            "price": price,
            "time": now,
        }
        ID = str(ID)
        self.load()
        if ID not in self.data:
            self.data[ID] = []
        self.data[ID].append(item)
        self.data[ID] = sorted(
            self.data[ID],
            key=lambda x: datetime.datetime.strptime(x["time"], self.time_format),
            reverse=True,
        )
        self.save()
        return now

    def get_channels(self):
        self.load()
        return self.data.keys()
