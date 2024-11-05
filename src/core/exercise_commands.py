from src.utils.json_helpers import get_exercises, save_exercises, get_exercise_names
from src.utils.input_helpers import get_numeric_input, get_user_input, get_yes_no, select_option
from datetime import datetime 
from src.utils.exercise_helpers import check_exercise_exists, get_exercise_options, print_exercises, print_field_values, modify_exercise_name
import json 

"""
Gets and displays exercises
"""
def show_exercises():
  data = get_exercises()
  
  if data is None:
    print("\nFailed to load exercises")
    return False 
  
  while True:
    # Show available options
    exercise_options = get_exercise_options(data)
    print("\n=== Your Routine Exercises ==== ")
    print_exercises(exercise_options)
    print("\n")

    # Get exercise selection 
    name = select_option(exercise_options)
    if name is False:
      return False
  
    # Find selected exercise 
    selected_exercise = None
    for exercise in data["exercises"]:
      if exercise["name"].lower() == name.lower():
        selected_exercise = exercise.copy()
        break

    if selected_exercise is None:
      print(f"\nCould not find exercise: {name}")
      print_exercises(exercise_options)
  
    field_options = {
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

    while True:
      print(f"\n=== Available fields for {name}: ===")
      for key, value in field_options.items():
        print(f"{key}: {value}")
  
      field = select_option(field_options)
      if field is False:
        print("Exiting...")
        break 

      try: 
        field_value = selected_exercise[field]
        print_field_values(field, field_value)
      except KeyError:
        print(f"Error: '{field}' not found")
    
      if not get_yes_no("\nDo you want to check another field? "):
        break 
  
    if not get_yes_no("Do you want to view a different exercise? "):
      break
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
    options = get_exercise_options(data)
    print("\n=== Current Exercises ===")
    print_exercises(options)
    print("\n")
  
  # Store new exercise
  exercise = {}

  # Get exercise fields
  name = get_user_input("\nExercise name: ")
  if name.lower() == "exit":
    return False 

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
  
  while True:
    # Show available options 
    exercise_options = get_exercise_options(data)
    print("\n=== Your Routine Exercises ===")
    print_exercises(exercise_options)
    print("\n")

    # Get exercise selection
    name = select_option(exercise_options)
    if name is False:
      print(f"Exiting...")
      return False

    selected_exercise = None
    for exercise in data["exercises"]:
      if exercise["name"].lower() == name.lower():
        selected_exercise = exercise.copy()
        break

    if selected_exercise is None:
      print(f"\nCould not find exercise: {name}. These are the exercises")
      print_exercises(data)
      continue   


    print(f"\n=== {name} ====\n")
    for key, value in selected_exercise.items():
      # print(f"{key}: {value}")
      print_field_values(key, value)
    print("\n")

    try:
      # Modify name if requested 
      if get_yes_no("Do you want to modify the name? "):
          new_name = modify_exercise_name(data, name, selected_exercise)
          if new_name is False:
            return False 
          old_name = name
          name = new_name
    
      # Modify equipment if requested 
      if  get_yes_no("Do you want to modify any equipment? "):
        new_equipment = get_user_input("What equipment will you be using (separate multple items with commas): ")
        selected_exercise["equipment"] = [item.strip() for item in new_equipment.split(",") if item.strip()]

      # Modify directions if requested 
      if get_yes_no("Do you want to modify the directions? "):
        new_directions = []
        print("\nEnter the new directions one step at a time")
        print("\nPress 'Enter' twice to complete this step")
        while True:
          step = input(">.. ")
          if not step:
            break
          new_directions.append(step)
          selected_exercise["directions"] = new_directions 
    
      # Modify reps, sets, frequency if requested 
      if get_yes_no("Do you want to modify the sets? "):
        selected_exercise["sets"] = get_numeric_input("New sets (numbers only): ")
    
      if get_yes_no("Do you want to modify the reps? "):
        selected_exercise["reps_per_set"] = get_numeric_input("New reps (numbers only): ")
    
      if get_yes_no("Do you want to adjust how many times a day you will do this exercise? "):
        selected_exercise["frequency"] = get_numeric_input("New daily frequency (numbers only): ")

      # Update total reps 
      selected_exercise["total_reps"] = (
          selected_exercise["sets"] * 
          selected_exercise["reps_per_set"] * 
          selected_exercise["frequency"]
      )

      # Modify other optional fields if requested 
      if get_yes_no("Do you want to modify the hold time? "):
        selected_exercise["hold_time"] = get_user_input("New hold time: ")
          
      if get_yes_no("Do you want to modify the resistance? "):
        selected_exercise["resistance"] = get_user_input("New resistance: ")

      if get_yes_no("Do you want to modify the weight? "):
        selected_exercise["weight"] = get_user_input("New weight: ")

      # Update modification date 
      modified_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
      selected_exercise["date_modified"] = modified_date
      
      # Display updated exercise 
      print(f"\n=== Updated Exercise: {selected_exercise["name"]}")
      for key, value in selected_exercise.items():
        print(f"{key} : {value}")

      # Update exercise in data 
      for i, exercise in enumerate(data["exercises"]):
        print(f"checking {exercise["name"]} turning it to lower {exercise["name"].lower()} and seeing if its the same as {name.lower()} for {name}")
        if exercise["name"].lower() == old_name.lower():
          print(f"we have a match and we are updating {exercise["name"].lower()}")
          data["exercises"][i] = selected_exercise
          print(f"Updated: {data["exercises"][i]}")
          break      
      
      # print(f"Data being passed to save: {data}")
      # Save updated data to data/exercises.json
      saved = save_exercises(data)
      if not saved:
        print("\nFailed to modify exercises, something went wrong, please try again")
        return False 

      # Show summary of the change 
      if old_name != selected_exercise["name"]:
        print(f"\nUpdated {name} to {selected_exercise["name"]}")
      print(f"\nYou will now be doing {selected_exercise['reps_per_set']} of {selected_exercise['name']} for {selected_exercise['sets']} sets {selected_exercise['frequency']} x times a day")

      # Check if user wants to modify another exercise
      if not get_yes_no("\nWould you like to modify another exercise? "):
        return True
      
      continue 
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
  
  if exercise_name.lower() == "exit":
    print("Exiting...")
    return False 
  
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

