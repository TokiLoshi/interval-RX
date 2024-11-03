from src.utils.json_helpers import get_exercises, save_exercises, get_exercise_names
from src.utils.input_helpers import get_numeric_input, get_user_input, get_yes_no 
from datetime import datetime 

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

  # TODO:
  # If exercise is alreay in the list user shouldn't be able to add it
  # make a check for this 
  
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
  for i, exercise in enumerate(exercises, 1): 
    print(f"{i}. {exercise}")
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

