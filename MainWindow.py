import json
import customtkinter
from customtkinter import *
from datetime import datetime

from CTkListbox import CTkListbox
from Run import Run

parse_text = "%s:%s  -  %s  -  %s DPS"

app = CTk()

class MainWindow:
  time_elapsed = 0
  parse_total = 0
  last_timer_mem = 0x0
  runs = []
  runs_file = f'runs/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json'

  def __init__(self, isInError=False):
    customtkinter.set_appearance_mode("Dark")
    app.geometry("450x150")
    app.attributes("-topmost", True)
    app.title("GBFR Parser")

    if isInError:
        app.errLabel = CTkLabel(
            master=app,
            text="GBFR process not found!!\nLaunch your game before launching the parser.",
            font=("Arial", 20))
        app.errLabel.place(relx=0.5, rely=0.5, anchor="center")

    else:
        app.label = CTkLabel(master=app, text=parse_text % (0, "00", 0, 0), font=("Arial", 20))
        app.label.place(relx=0.5, rely=0.1, anchor="center")

        app.resetButton = CTkButton(master=app, text="Reset")
        app.resetButton.place(relx=0.3, rely=0.3, anchor="center")
        app.resetButton.bind("<Button-1>", self.reset)

        app.saveRunButton = CTkButton(master=app, text="Save Run")
        app.saveRunButton.place(relx=0.7, rely=0.3, anchor="center")
        app.saveRunButton.bind("<Button-1>", self.save_run)

        app.runsLabel = CTkLabel(master=app, text="Runs saved: 0", font=("Arial", 20))
        app.runsLabel.place(relx=0.01, rely=0.5)

  def mainLoop(self):
    app.mainloop()

  def reset(self, event):
    self.last_timer_mem = 0x0
    self.update(0,0)

  def update(self, time_elapsed=0, parse_total=0):
    self.time_elapsed = time_elapsed
    self.parse_total = parse_total

    if time_elapsed == 0 or parse_total == 0:
        app.label.configure(text=parse_text % (0, "00", 0, 0))
        return

    seconds = self.time_elapsed % 60 if self.time_elapsed % 60 > 9 else "0%s" % (self.time_elapsed % 60)
    damage = self.parse_total
    dps = self.parse_total // self.time_elapsed if int(seconds) > 0 else damage
    app.label.configure(text=parse_text % (
        self.time_elapsed // 60,
        seconds,
        f"{damage:,}",
        f"{dps:,}"))

  def setParseTotal(self, parse_total):
    self.parse_total = parse_total

  def getParseTotal(self):
    return self.parse_total

  def setTimeElapsed(self, time_elapsed):
    self.time_elapsed = time_elapsed

  def getTimeElapsed(self):
    return self.time_elapsed

  def save_run(self, event=None):
    new_Run = Run(self.time_elapsed, self.parse_total)
    self.runs.append(new_Run)

    app.runsLabel.configure(text=f"Runs saved: {len(self.runs)}")

    os.makedirs(os.path.dirname(self.runs_file), exist_ok=True)
    if os.path.isfile(self.runs_file):
      with open(self.runs_file, "r") as f:
        runs = json.load(f)
        runs = [Run().fromJson(run) for run in runs]
        runs.append(new_Run)
    else:
      runs = [new_Run]

    with open(self.runs_file, "w") as f:
      f.write(json.dumps([run.toJSON() for run in runs], indent=4))

    self.reset()