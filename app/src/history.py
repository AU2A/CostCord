import json
import os
import datetime


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

    def append(self, ID, name, price, past_days):
        now = datetime.datetime.now() - datetime.timedelta(days=past_days)
        now = now.strftime(self.time_format)
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
            self.data[ID]["expenses"] = []
        self.data[ID]["expenses"].append(item)
        self.data[ID]["expenses"] = sorted(
            self.data[ID]["expenses"],
            key=lambda x: datetime.datetime.strptime(x["time"], self.time_format),
            reverse=True,
        )
        self.save()
        return now

    def append_monthly_payments(self, channelID):
        self.load()
        if channelID not in self.data:
            return []
        payments = []
        for item in self.data[channelID]["monthly-payments"]:
            if item["on"]:
                payments.append((item["name"], item["price"]))
        return payments

    def get(self, ID, length):
        ID = str(ID)
        self.load()
        if ID not in self.data:
            return []
        return self.data[ID]["expenses"][:length]

    def get_channels(self):
        self.load()
        return self.data.keys()
