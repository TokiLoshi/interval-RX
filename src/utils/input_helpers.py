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
        if response == "exit":
           return False
        if response in ["y", "yes"]:
            return True
        if response in ["n", "no"]:
            return False
        print("Please enter a valid yes or no (Y/N)")

"""
Handles selection of exercises using number inputs from user 
"""
def select_option(options):
   while True: 
      selection = get_user_input("\nEnter an option: ").strip()
      # check for exit
      if isinstance(selection, str) and selection.lower() == "exit":
         return False 
      
      # check if selection is a number
      if selection in options: 
         return options[selection]
      
      # check if selection is an exercise name
      for key, value in options.items():
         if selection.lower() == value.lower():
            return options[key]
      print(f"\n{selection} is not an option, please enter a valid exercise by name or number")