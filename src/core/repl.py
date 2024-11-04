from datetime import datetime 
from src.core.timer_commands import start, stop, intervals
from src.core.exercise_commands import show_exercises, add_exercise, delete_exercise, modify_exercise
from src.core.progress_commands import print_progress, log_exercise

def repl():
  while True:
    try:
      line = input(">>> ")
      match line:
        case "start" | "1":
          start()
        case "stop" | "2":
          stop()
        case "add_exercise" | "3":
          add_exercise()
        case "show_exercises" | "4":
          show_exercises()
        case "modify_exercise" | "5":
          modify_exercise()
        case "delete_exercise" | "6":
          delete_exercise()
        case "log_exercise" | "7":
          log_exercise()
        case "progress" | "8":
          print_progress()
        case "intervals" | "9":
          intervals()
        case "exit" | "0":
          break
        case _:
          help()
    except Exception as e:
      print(f"Error: {e}")
      print("Type 'help' to view available commands")

def help():
  print("\n=== IntervalRX Menu Options ======\n")
  print("1. 'start' to start a timer")
  print("2. 'stop' to stop a timer")
  print("3. 'add_exercise' to add an exercise to your routine")
  print("4. 'show_exercises' to see all of your exercises")
  print("5. 'modify_exercise' to modify an exercise and update your routine")
  print("6. 'delete_exercise' to delete an exercise and update your routine")
  print("7. 'log_exercise' to log an exercise and update your progress")
  print("8. 'progress' to print your progress report")
  print("9. 'intervals' to print your currently configured timers")
  print("0. 'exit' to stop running IntervalRX\n")
