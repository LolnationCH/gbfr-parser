import json
import os

from Run import Run

def _getOldRuns():
  os.makedirs(os.path.dirname("./runs"), exist_ok=True)
  old_runs = []
  for filename in os.listdir("runs"):
    if filename.endswith(".json"):
      with open(f"runs/{filename}", "r") as f:
        runs = json.load(f)
        runs = [Run().fromJson(run) for run in runs]
        old_runs.extend(runs)
  return old_runs

def _getDictionaryOfRuns(old_runs):
  run_dict = {}
  for run in old_runs:
    if run.name in run_dict:
      run_dict[run.name].append(run)
    else:
      run_dict[run.name] = [run]
  return run_dict

def _calculateAverages(runs):
  average_dps = {}
  average_time = {}
  for name, runs in run_dict.items():
    total_dps = 0
    total_time = 0
    for run in runs:
      total_dps += run.dps
      total_time += run.time_elapsed

    average_dps[name] = total_dps // len(runs)
    average_time[name] = total_time // len(runs)

  return average_dps,average_time

old_runs = _getOldRuns()
run_dict = _getDictionaryOfRuns(old_runs)
average_dps,average_time = _calculateAverages(run_dict)

def getAverageDPSForARun(runName):
  return average_dps[runName]

def getAverageTimeForARun(runName):
  return average_time[runName]

if __name__ == '__main__':
  print(average_dps)
  print(average_time)