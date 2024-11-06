import json 

def get_progress():
  print("\nLoading progress...")
  try:
    with open("data/progress.json", "r") as file:
      data = file.read()
      if not data:
        default_data = {"progress" : {}}
        save_progress(default_data)
      file.seek(0)
      return json.load(file)
  except FileNotFoundError: 
    print("\nFile not found adding some default data to the file")
    default_data = {"progress": {}}
    with open("data/progress.json", "w") as file: 
      json.dump(default_data, file, indent=2)
    return default_data 
  except json.JSONDecodeError:
    print("\nError: something is wrong with the progress file")
    return None
  except Exception as e:
    print(f"\nGetting an unknown exception loading progress: {e}")
    return None 

def get_exercises():
  print("\nLoading exercises...")
  # open the exercises file 
  try:
    with open("data/exercises.json", "r") as file:
      data = file.read()
      if not data: 
        return {"exercises": []}
      file.seek(0)
      return json.load(file)
  except FileNotFoundError:
    default_data = {"exercises": []}
    with open("data/exercises.json", "w") as file:
      json.dump(default_data, file, indent=2)
    return default_data
  except json.JSONDecodeError:
    print("\nError something is wrong with the exercises files")
    return None
  except Exception as e:
    print(f"\nGetting an unknown exception loading exercises: {e}")
    return None
  
def save_progress(data): 
  try: 
    with open("data/progress.json", "w") as file: 
      json.dump(data, file, indent=2)
    return True
  except Exception as e:
    print(f"\nError saving progress: {e}")
    return False

def save_exercises(data):
  for i, exercise in enumerate(data["exercises"], 1):
    print(f"{i} {exercise['name']}")
  try:
    with open("data/exercises.json", "w") as file:
      json.dump(data, file, indent=2)
    return True
  except Exception as e:
    print(f"\nError saving exercises: {e}")
    return False
  
def get_exercise_names(data):
  exercises = data["exercises"]
  exercise_names = [exercise["name"] for exercise in exercises]
  return exercise_names