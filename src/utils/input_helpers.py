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
            return "yes"
        if response in ["n", "no"]:
            return "no"
        print("Please enter a valid yes or no (Y/N)")
