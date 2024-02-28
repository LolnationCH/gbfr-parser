from customtkinter import *

class ActionButtonsFrame(CTkFrame):
  def __init__(self, parent, main_window):
    CTkFrame.__init__(self, parent)

    self.grid(row=1, column=0, columnspan=2, sticky="nsew")
    self.grid_rowconfigure(1, weight=1)

    self.resetButton = CTkButton(master=self, text="Reset")
    self.resetButton.grid(row=1, column=0)
    self.grid_columnconfigure(0, weight=1)
    self.resetButton.bind("<Button-1>", main_window.reset)

    self.saveRunButton = CTkButton(master=self, text="Save Run")
    self.saveRunButton.grid(row=1, column=1)
    self.grid_columnconfigure(1, weight=1)
    self.saveRunButton.bind("<Button-1>", main_window.save_run)