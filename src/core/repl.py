from datetime import datetime 
from src.utils.json_helpers import get_exercises, save_exercises, get_exercise_names, get_progress
from src.utils.input_helpers import get_numeric_input, get_user_input, get_yes_no

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
        case "delete_exercise":
          delete_exercise()
        case _:
          help()
    except Exception as e:
      print(f"Error: {e}")
      print("Type 'help' to view available commands")

def start():
  # check last process log against today's date 
  # update exercises for the day 
  print("starting")

def help():
  print("=== Menu Options ======")
  print("- 'start' to start a timer")
  print("- 'stop' to stop a timer")
  print("- 'add_exercise' to add an exercise to your routine")
  print("- 'log_exercise' to log an exercise and update your progress")
  print("- 'delete_exercise' to delete an exercise and update your routine")
  print("- 'progress' to print your progress report")
  print("- 'intervals' to print your currently configured timers")

def stop():
  print(f"stopping...")

def intervals():
  print(f"You have a bunch of intervals")
  

# TODO: 
# figure out how to show these exercises if there are images on Tkinter 
# get user to add an image file / folder 
def add_exercise():
  print("\n=== Adding New Exercise ===")

  # Load in exercise data
  data = get_exercises()
  if data is None:
    print("Failed to load exercises")

  # Store users inputs 
  exercise = {}

  # Get exercise name and directions 
  name = get_user_input("Exercise name: ")
  exercise["name"] = name
  equipment = get_user_input("Equipment (separate multiple items with commas): ")
  exercise["equipment"] = [item.strip() for item in equipment.split(",") if item.strip()]
  print("\n Enter the directions one step at a time")
  print("\n Press 'Enter' twice to complete this step ->")
  directions = []
  while True:
    step = input(">.. ")
    if not step:
      break 
    directions.append(step)
  exercise["directions"] = directions 

  # Get reps, frequency and calculate totals 
  print(f"For this next 3 questions please only use numbers ")
  sets = get_numeric_input("How sets would you like to do? ")
  exercise["sets"] = sets
  reps = get_numeric_input("How many reps per set? ")
  exercise["reps_per_set"] = reps
  times_per_day = get_numeric_input("How many times a day would you like to do this exercise? ")
  exercise["frequency"] = times_per_day
  exercise["total_reps"] = reps * sets * times_per_day 

  # Check for hold times and resistance and update 
  hold_time = get_yes_no("Does this exercise have a hold time? Y/N ")
  if hold_time == "yes":
    exercise_hold_time = get_user_input("What is the hold time? ")
    exercise["hold_time"] = exercise_hold_time 
  else:
    exercise["hold_time"] = None 
  resistance = get_yes_no("Does this exercise have resistance? Y/N ")
  if resistance == "yes":
    exercise_resistance = get_user_input("How much resistance? ")
    exercise["resistance"] = exercise_resistance
  else:
    exercise["resistance"] = None 
  weights = get_yes_no("Is this exercise weighted? Y/N ") 
  if weights == "yes":
    exercise_weights = get_user_input("What is the weight for this exercise? ")
    exercise["weight"] = exercise_weights
  else: 
    exercise["weight"] = None
  
  # Add time stamps 
  current_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
  exercise["date_added"] = current_date 
  exercise["date_modified"] = current_date

  # Save new exercise to JSON 
  data["exercises"].append(exercise)
  
  saved = save_exercises(data)
  if not saved: 
    print("Failed to save exercises, something went wrong, please try again")
    return False
  
  print(f"Added {exercise["name"]}")
  print(f"You have elected to do {exercise["reps_per_set"]} reps and {exercise["sets"]} of {exercise["name"]} {exercise["frequency"]} x times daily")
  add_another_exercise = get_yes_no("Would you like to add another exercise? ")
  if add_another_exercise == "yes":
    add_exercise()
  return True

def modify_exercise():
  print("modifying exercise")
  # get exercises 
  # create dictionary as temporary store 
  # prompt user, which exercise would they like to modify 
  # give options to modify reps per repeat, total reps, name 
  # takes that argument and based on the case
  # Update the field
  # keep prompting until the user says save 
  # return a success message or error 

def print_progress():
  print("Your progress so far")
  all_progress = get_progress()
  progress = all_progress["progress"]
  if not progress:
    print("I'm sorry it doesn't look like you have made any progress yet.\nLog an exercise to get started")
  else:
    for success in progress:
      print(f"success: {success}")
  # open progress report 
  # you've done x/y reps for exercise  
  # and either a congratulatory message
  # or a prompt to update the timer 
  
def log_exercise():
  print("recording exercise")
  exercises = get_exercises()
  # get all the exercises 
  data = get_exercises()
  if data is None: 
    print("Failed to load exercises")
    return False
  
  # Get the exercise names 
  # Show the exercises to the user 
  # Ask which one they want to update 
  # Check that the name is valid 
  # Check the current date 
  # Load in the progress.json
  # If the name exists for the current date 
    # We must update the current information 
  # Otherwise we must add to the json with a new progress

def delete_exercise():
  print("=== Deleting exercise ===")
  
  # Load exercise data 
  data = get_exercises()
  if data is None:
    print("Failed to load exercises")
    return False
  
  # Get exercise to delete 
  print(f"You have the following exercises: ")
  exercises = get_exercise_names(data)
  for exercise in exercises: 
    print(f"{exercise}")
  exercise_name = get_user_input("Which would you like to delete? ")
  
  # Check validity and delete
  if exercise_name in exercises:
    data["exercises"] = [ex for ex in data["exercises"] if ex["name"] != exercise_name]
    # save the data 
    if not save_exercises(data):
      print("Failed to delete exercise")
      return False 
    else:
      print(f"Successfully deleted: {exercise_name}")
  else:
    print(f"Invalid exercise name")
    return False

