import json
import customtkinter
from customtkinter import *
from datetime import datetime

from Run import Run
from gui.ActionButtonsFrame import ActionButtonsFrame
from gui.StatLabel import StatLabel

time_text = "%s:%s"
damage_text = "%s"
dps_text = "%s DPS"


app = CTk()

class MainWindow:
  time_elapsed = 0
  parse_total = 0
  last_timer_mem = 0x0
  runs = []
  runs_file = f'runs/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json'
  mission_name = "The Tale of Bahamut's Rage"

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
        app.StatLabel = StatLabel(app, self.mission_name)
        app.StatLabel.grid(sticky="nsew")
        app.grid_rowconfigure(0, weight=1)
        app.grid_columnconfigure(0, weight=1)

        app.buttonFrame = ActionButtonsFrame(app, self)
        app.grid_rowconfigure(1, weight=1)

        app.runsLabel = CTkLabel(master=app, text="Runs saved: 0", font=("Arial", 20))
        app.runsLabel.grid(row=2, column=0)

  def mainLoop(self):
    app.mainloop()

  def reset(self, event):
    self.last_timer_mem = 0x0
    self.update(0,0)

  def update(self, time_elapsed=0, parse_total=0):
    self.time_elapsed = time_elapsed
    self.parse_total = parse_total
    app.StatLabel.update(time_elapsed, parse_total)

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
    if (new_Run.IsEmpty()):
        return
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

    self.reset(None)