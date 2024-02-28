from customtkinter import *

import SaveData

time_text = "%s:%s"
damage_text = "%s"
dps_text = "%s DPS"

class StatLabel(CTkFrame):

  def __init__(self, parent, mission_name):
    CTkFrame.__init__(self, parent)
    self.mission_name = mission_name

    self.timeLabel = CTkLabel(master=self, text=time_text % ("00", "00"), font=("Arial", 20))
    self.timeLabel.grid(row=1, column=0, columnspan=2)
    self.grid_columnconfigure(0, weight=50)

    self.damageLabel = CTkLabel(master=self, text=damage_text % " 0", font=("Arial", 20))
    self.damageLabel.grid(row=1, column=2)
    self.grid_columnconfigure(2, weight=50)

    self.dpsLabel = CTkLabel(master=self, text=dps_text % " 0", font=("Arial", 20))
    self.dpsLabel.grid(row=1, column=3)
    self.grid_columnconfigure(3, weight=50)

    self.grid_rowconfigure(1, weight=1)

  def update(self, time_elapsed=0, parse_total=0):
    seconds = time_elapsed % 60 if time_elapsed % 60 > 9 else "0%s" % (time_elapsed % 60)
    damage = parse_total
    dps = parse_total // time_elapsed if int(seconds) > 0 else damage

    avg_dps = SaveData.getAverageDPSForARun(self.mission_name)
    avg_time = SaveData.getAverageTimeForARun(self.mission_name)

    dps_color = "green" if dps > avg_dps else "red"
    time_color = "green" if time_elapsed < avg_time else "red"

    self.timeLabel.configure(text=time_text % (time_elapsed // 60, seconds), text_color=time_color)
    self.damageLabel.configure(text=damage_text % f"{damage:,}")
    self.dpsLabel.configure(text=dps_text % f"{dps:,}", text_color=dps_color)
