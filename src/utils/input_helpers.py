# Validates user input 
def get_user_input(prompt):
  get_input = input(prompt)
  cleaned_prompt = " ".join(get_input.strip().split())
  return cleaned_prompt

def get_numeric_input(prompt):
  while True: 
    try:
      return int(get_user_input(prompt))
    except ValueError:
      print("Please enter a valid number")

def get_yes_no(prompt):
    while True:
        response = get_user_input(prompt).lower()
        if response in ["y", "yes"]:
            return True
        if response in ["n", "no"]:
            return False
        print("Please enter a valid yes or no (Y/N)")

def check_exercise_exists(data, exercise_name):
   return any(exercise["name"].lower() == exercise_name.lower()
              for exercise in data["exercises"])

"""
Handles selection of exercises using number inputs from user 
"""
def select_exercise(options):
   while True: 
      selection = get_user_input("\nEnter an exercise: ")

      print(f"Selection: {selection}")
      if isinstance(selection, str) and selection.lower() == "exit":
         return False 
      if selection in options or selection.lower() in options:
         return options[selection]
      print(f"\n{selection} is not an option, please enter a valid exercise by name or number")