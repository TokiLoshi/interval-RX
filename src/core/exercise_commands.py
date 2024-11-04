from src.utils.json_helpers import get_exercises, save_exercises, get_exercise_names
from src.utils.input_helpers import get_numeric_input, get_user_input, get_yes_no, check_exercise_exists 
from datetime import datetime 

"""
Print helper for exercise functions
"""
def print_exercises(data):
  for i, exercise in enumerate(data["exercises"]):
      print(f"{i}. {exercise["name"]}")

"""
Gets and displays exercises
"""
def show_exercises():
  data = get_exercises()
  
  if data is None:
    print("\nFailed to load exercises")
    return False 
  
  print("\n=== Your Routine Exercises ==== ")
  print_exercises(data)
  print("\n")

  while True:
    name = get_user_input("Which exercise would you like to know more about? ")
    if name.lower() == "exit": 
      print(f"Exiting...\n")
      return False 
    if check_exercise_exists(data, name):
      break
    print(f"\n'{name}' not found. Please enter a valid exercise name\n")
  
  selected_exercise = {}
  for exercise in data["exercises"]:
    if exercise["name"].lower() == name.lower():
      selected_exercise = exercise.copy()
      break
  
  options = {
    "1" : "equipment",
    "2" : "directions",
    "3" : "sets",
    "4" : "reps_per_set",
    "5" : "total_reps",
    "6" : "hold_time",
    "7" : "resistance",
    "8" : "weight",
    "9" : "date_added",
    "10" : "date_modified"
  }

  print(f"\nWhat do you want to check about {name}?")
  
  while True:
    print(f"\n=== Available fields for {name}: ===")
    for key, value in options.items():
      print(f"{key}: {value}")
    
    field = get_user_input("\nEnter the number of the field you want to learn more about: ")
    if field.lower() == "exit": 
      return False 
    
    if field not in options:
      print(f"{field} is not an options, please try again\n")
    
    else:
      print(f"{options[field]} is {selected_exercise[options[field]]}")
      if not get_yes_no("\nDo you want to check another field? "):
        break 
  
  if get_yes_no("Do you want to view a different exercise? "):
    return show_exercises()
  return True

"""
Adds a new exercise to data/exercises.json
Exercises comprise of name, equipment, directions sets, 
reps, frequency and optionally a hold_time, resistance, 
weight. The current date added and date modified are 
also stored as data
"""
def add_exercise():
  # Load in exercise data
  data = get_exercises()
  if data is None:
    print("Failed to load exercises")

  if len(data["exercises"]) == 0: 
    print("\nYou don't have any exercises yet. Lets change that!\n")
  else:  
    print("\n=== Current Exercises ===")
    print_exercises(data)
    print("\n")
  
  # Store new exercise
  exercise = {}

  # Get exercise fields
  name = get_user_input("\nExercise name: ")

  # Check user isn't trying to duplicate exercise
  if check_exercise_exists(data, name):
    print(f"\n{name} already exists. Here are all the exercises you currently have: ")
    print_exercises(data)
    return False 
  
  print(f"\n=== Adding New Exercise: {name} ===")

  exercise["name"] = name
  equipment = get_user_input("\nEquipment (separate multiple items with commas): ")
  exercise["equipment"] = [item.strip() for item in equipment.split(",") if item.strip()]
  
  print("\nEnter the directions one step at a time")
  print("\nPress 'Enter' twice to complete this step ->")
  directions = []
  while True:
    step = input(">.. ")
    if not step:
      break 
    directions.append(step)
  exercise["directions"] = directions 

  print(f"\nFor this next 3 questions please only use numbers ")
  sets = get_numeric_input("How sets would you like to do? ")
  exercise["sets"] = sets
  
  reps = get_numeric_input("How many reps per set? ")
  exercise["reps_per_set"] = reps
  
  times_per_day = get_numeric_input("How many times a day would you like to do this exercise? ")
  exercise["frequency"] = times_per_day
  
  exercise["total_reps"] = reps * sets * times_per_day 

  # Optional fields 
  if get_yes_no("Does this exercise have a hold time? Y/N "):
    exercise["hold_time"] = get_user_input("What is the hold time? ")
  else:
    exercise["hold_time"] = None 
  
  if get_yes_no("Does this exercise have resistance? Y/N "):
    exercise["resistance"] = get_user_input("How much resistance? ")
  else:
    exercise["resistance"] = None 
  
  if get_yes_no("Is this exercise weighted? Y/N "):
    exercise["weight"] = get_user_input("What is the weight for this exercise? ")
  else: 
    exercise["weight"] = None
  
  # Current date and time also stored as date modified  
  current_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
  exercise["date_added"] = current_date 
  exercise["date_modified"] = current_date

  # Save new exercise to JSON 
  data["exercises"].append(exercise)
  
  saved = save_exercises(data)
  if not saved: 
    print("\nFailed to save exercises, something went wrong, please try again")
    return False
  
  print(f"\nAdded {exercise["name"]}")
  print(f"\nYou have elected to do {exercise["reps_per_set"]} reps and {exercise["sets"]} of {exercise["name"]} {exercise["frequency"]} x times daily")
  
  if get_yes_no("Would you like to add another exercise? "):
    # Optionally keep adding exercises 
    return add_exercise()
  return True

"""
User can modify name, reps, sets, frequency,
if reps or sets or frequency are changed total_sets will be updated
user can also modify hold_time, resistance and weight 
date added stays the same and date modified updates. 
Returns True if modififaction was successful and False if it was not
"""
def modify_exercise():
  # Load exercises from data/exercises.json file 
  data = get_exercises()
  if data is None:
    print("\nFailed to load exercises")
    return False 

  print("\n=== Current Exercises ===")
  print_exercises(data)
  print("\n")

  while True:
    name = get_user_input("Exercise name (or 'exit' to cancel): ")
    if name.lower() == "exit":
      print(f"\nAbandonning edits...\n")
      return False
    if check_exercise_exists(data, name):
      break 
    else:
      print(f"\n'{name}' not found. Please select an existing exercise. These are the exercises in your routine: ")
      print_exercises(data)  
  
  # Update exercise name 
  modified_exercise = {}
  for exercise in data["exercises"]:
    if exercise["name"].lower() == name.lower():
      modified_exercise = exercise.copy()
      break

  print(f"\n=== {name} ====\n")
  for key, value in modified_exercise.items():
    print(f"{key}: {value}")
  print("\n")

  # Try update properties 
  try:
    if get_yes_no("Do you want to modify the name? "):
      while True:
        new_name = get_user_input("Edited exercise name (or 'exit' to cancel): ")
        if not new_name:
          new_name = name 
          break
        if new_name.lower() == "exit":
          print(f"\nAbandonning edits...")
          return False 
        if new_name.lower() != name.lower() and check_exercise_exists(data, new_name):
          print(f"\n{new_name} already exists. Here are all the exercises you currently have")
          print_exercises(data)
        else:
          modified_exercise["name"] = new_name 
          break
    
    # Update equipment 
    if  get_yes_no("Do you want to modify any equipment? "):
      new_equipment = get_user_input("What equipment will you be using (separate multple items with commas): ")
      modified_exercise["equipment"] = [item.strip() for item in new_equipment.split(",") if item.strip()]
    
    if get_yes_no("Do you want to modify the directions? "):
      new_directions = []
      print("\nEnter the new directions one step at a time")
      print("\nPress 'Enter' twice to complete this step")
      while True:
        step = input(">.. ")
        if not step:
          break
        new_directions.append(step)
      modified_exercise["directions"] = new_directions 
    
    if get_yes_no("Do you want to modify the sets? "):
      modified_exercise["sets"] = get_numeric_input("New sets (numbers only): ")
    
    if get_yes_no("Do you want to modify the reps? "):
      modified_exercise["reps_per_set"] = get_numeric_input("New reps (numbers only): ")
    
    if get_yes_no("Do you want to adjust how many times a day you will do this exercise? "):
      modified_exercise["frequency"] = get_numeric_input("New daily frequency (numbers only): ")

    modified_exercise["total_reps"] = (
      modified_exercise["sets"] * 
      modified_exercise["reps_per_set"] * 
      modified_exercise["frequency"]
      )

    if get_yes_no("Do you want to modify the hold time? "):
      modified_exercise["hold_time"] = get_user_input("New hold time: ")
    
    if get_yes_no("Do you want to modify the resistance? "):
      modified_exercise["resistance"] = get_user_input("New resistance: ")

    if get_yes_no("Do you want to modify the weight? "):
      modified_exercise["weight"] = get_user_input("New weight: ")

    modified_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    modified_exercise["date_modified"] = modified_date
    
    print(f"\n=== Updated Exercise: {modified_exercise["name"]}")
    for key, value in modified_exercise.items():
      print(f"{key} : {value}")

    for i, exercise in enumerate(data["exercises"]):
      if exercise["name"].lower() == name.lower():
        data["exercises"][i] = modified_exercise
        break      
        
    saved = save_exercises(data)
    if not saved:
      print("\nFailed to modify exercises, something went wrong, please try again")
      return False 
    
    if name != modified_exercise["name"]:
      print(f"\nUpdated {name} to {modified_exercise["name"]}")
    print(f"\nYou will now be doing {modified_exercise['reps_per_set']} of {modified_exercise['name']} for {modified_exercise['sets']} sets {modified_exercise['frequency']} x times a day")

    if get_yes_no("\nWould you like to modify another exercise? "):
      return modify_exercise() 
    return True  
  except Exception as e:
    print("\nError updating fields: ", e)
    return False

"""
deletes an exercise entry from data/exercises.json
"""
def delete_exercise():
  print("\n=== Deleting exercise ===")
  
  # Load exercise data 
  data = get_exercises()
  if data is None:
    print("\nFailed to load exercises")
    return False
  
  # Get exercise to delete 
  print(f"\nYou have the following exercises: ")
  exercises = get_exercise_names(data)
  for i, exercise in enumerate(exercises, 1): 
    print(f"{i}. {exercise}")
  print("\n")

  exercise_name = get_user_input("Which would you like to delete? ")
  
  # Check validity and delete
  if exercise_name in exercises:
    data["exercises"] = [ex for ex in data["exercises"] if ex["name"] != exercise_name]
    # save the data 
    if not save_exercises(data):
      print("\nFailed to delete exercise")
      return False 
    else:
      print(f"\nSuccessfully deleted: {exercise_name}")
  else:
    print(f"\nInvalid exercise name")
    return False

