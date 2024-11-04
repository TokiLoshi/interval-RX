"""
Handles numbered dictionary of exercises from the data 
Returns a dictionary of stringified numbers and exercise names
"""
def get_exercise_options(data):
  options = {}
  for i, exercise in enumerate(data["exercises"], 1):
    options[str(i)] = exercise["name"] 
  return options

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