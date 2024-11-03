from src.utils.json_helpers import get_exercises, get_progress, save_progress, get_exercise_names
from src.utils.input_helpers import get_user_input, get_numeric_input
from datetime import datetime 

def print_progress():
  print("Your progress so far")

  # Get progress
  all_progress = get_progress()
  progress = all_progress["progress"]

  # Validate progress
  if not progress:
    print("I'm sorry it doesn't look like you have made any progress yet.\nLog an exercise to get started")
  else:
    for success in progress:
      print(f"success: {success}")
  # TODO:
  # add either a congratulatory message
  # or a prompt to update the timer 
 


def log_exercise():
  print("=== Recording Exercise ===")
  
  # Load exercises and progress
  data = get_exercises()
  if data is None: 
    print("Failed to load exercises")
    return False
  
  # check for current data
  progress_data = get_progress() 
  if progress_data is None: 
    print("Failed to load progress")
    return False 
  
  # Get current date
  current_date = datetime.now().strftime("%d/%m/%Y")

  if "progress" not in progress_data:
    progress_data["progress"] = {}
  if current_date not in progress_data["progress"]:
    progress_data["progress"][current_date] = {"exercises": []}

  # Show available exercises 
  exercises = get_exercise_names(data)
  
  print("You have the following exercises: ")
  for i, exercise in enumerate(exercises, 1): 
    print(f"{i}. {exercise}")

  # Get the exercise to update 
  exercise_name = get_user_input("Which exercise did you do? ")
  if exercise_name not in exercises:
    print(f"Invalid exercise name, these are your exercises: ")
    for i, exercise in enumerate(exercises, 1): 
      print(f"{i}. {exercise}") 
    return False 
  
  todays_exercises = progress_data["progress"][current_date]["exercises"]
  existing_exercise = next((ex for ex in todays_exercises if ex["name"] == exercise_name), None)

  # Get sets 
  sets = get_numeric_input("How many sets did you do? ")
  reps = get_numeric_input("How many reps did you do? ")
  total_reps = sets * reps
  
  notes = get_user_input("Do you have any notes to share? ")
  notes = notes if notes.strip() else None

  current_time = datetime.now().strftime("%H:%M:%S")
  exercise_entry = {
    "name" : exercise_name,
    "sets_completed" : sets, 
    "reps_completed" : reps, 
    "total_reps" : total_reps,
    "last_updated" : current_time,
    "notes" : [notes] if notes else []
  }

  if existing_exercise:
    print(f"You're making progress, it's great that you're doing more of these! Let's go! Tell me more...")
    existing_exercise["sets_completed"] += sets 
    existing_exercise["reps_completed"] += reps
    existing_exercise["total_reps"] += total_reps
    if notes:
      existing_exercise["notes"].append(notes)
    existing_exercise["last_updated"] = current_time
    exercise_info = exercise_entry
  else:
    todays_exercises.append(exercise_entry)  
  
  if not save_progress(progress_data):
    print("Failed to save progress")
    return False 
  
  print("Saved progress! Well done and keep going!")
  print(f"Updated {exercise_info}")
  return True
