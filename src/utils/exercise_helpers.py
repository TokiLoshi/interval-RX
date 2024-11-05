from src.utils.input_helpers import get_user_input
"""
Handles numbered dictionary of exercises from the data 
Returns a dictionary of stringified numbers and exercise names
"""
def get_exercise_options(data):
  options = {}
  for i, exercise in enumerate(data["exercises"], 1):
    options[str(i)] = exercise["name"] 
  return options

def check_exercise_exists(data, exercise_name):
   return any(exercise["name"].lower() == exercise_name.lower()
              for exercise in data["exercises"])

"""
Print helper for exercise functions
"""
def print_exercises(options):
  for number, exercise in options.items():
      print(f"{number}. {exercise}")
  print(" ")

"""
Print helper for items that are lists
"""
def print_field_values(field_name, value):
  if value is None:
    return
   
  if isinstance(value, list):
    print(f"\n{field_name}:")
    for i, item in enumerate(value, 1):
      print(f" {i}. {item}")
  else:
    print(f"{field_name}: {value}")


def modify_exercise_name(data, current_name, selected_exercise):
  while True:
    new_name = get_user_input("Edited exercise name (or 'exit' to cancel): ")
    if not new_name:
      return current_name 
    if new_name.lower() == "exit":
      print("Abandonning edits...")
      return False
    if new_name.lower() != current_name.lower and check_exercise_exists(data, selected_exercise):
      print(f"\n{new_name} already exists. Here are all the exercises you currently have")
      print_exercises(data)
    else:
      selected_exercise["name"] = new_name
      return new_name