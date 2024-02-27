class Run:
  time_elapsed = 0
  parse_total = 0
  dps = 0

  def __init__(self, time_elapsed=0, parse_total=0):
    self.time_elapsed = time_elapsed
    self.parse_total = parse_total
    self.dps = time_elapsed / parse_total if parse_total != 0 else 0

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