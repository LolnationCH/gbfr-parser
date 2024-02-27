class Run:
  time_elapsed = 0
  parse_total = 0
  dps = 0

  def __init__(self, time_elapsed=0, parse_total=0):
    self.time_elapsed = time_elapsed
    seconds = self.time_elapsed % 60 if self.time_elapsed % 60 > 9 else "0%s" % (self.time_elapsed % 60)
    self.parse_total = parse_total
    damage = self.parse_total
    self.dps = self.parse_total // self.time_elapsed if int(seconds) > 0 else damage

  def toJSON(self):
    return {
      "time": self.time_elapsed,
      "damage": self.parse_total,
      "dps": self.dps
    }

  def fromJson(self, json_obj):
    self.time_elapsed = json_obj["time"]
    self.parse_total = json_obj["damage"]
    self.dps = json_obj["dps"]
    return self