from datetime import datetime 
from src.core.timer_commands import start, stop, intervals
from src.core.exercise_commands import add_exercise, delete_exercise, modify_exercise
from src.core.progress_commands import print_progress, log_exercise

def repl():
  while True:
    try:
      line = input(">>> ")
      match line:
        case "exit":
          break
        case "start":
          start()
        case "stop":
          stop()
        case "add_exercise":
          add_exercise()
        case "progress":
          print_progress()
        case "intervals":
          intervals()
        case "log_exercise":
          log_exercise()
        case "modify_exercise":
          modify_exercise()
        case "delete_exercise":
          delete_exercise()
        case _:
          help()
    except Exception as e:
      print(f"Error: {e}")
      print("Type 'help' to view available commands")

def help():
  print("=== IntervalRX Menu Options ======")
  print("- 'start' to start a timer")
  print("- 'stop' to stop a timer")
  print("- 'add_exercise' to add an exercise to your routine")
  print("- 'log_exercise' to log an exercise and update your progress")
  print("- 'modify_exercise' to modify an exercise and update your routine")
  print("- 'delete_exercise' to delete an exercise and update your routine")
  print("- 'progress' to print your progress report")
  print("- 'intervals' to print your currently configured timers")
  print("- 'exit' to stop running IntervalRX")
