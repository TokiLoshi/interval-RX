import json 

def get_progress():
  print("Loading progress...")
  try:
    with open("data/progress.json", "r") as file:
      data = file.read()
      if not data:
        return {"progress": []}
      return json.load(file)
  except FileNotFoundError: 
    default_data = {"progress": []}
    with open("data/progress.json", "w") as file: 
      json.dump(default_data, file, indent=2)
    return default_data 
  except json.JSONDecodeError:
    print("Error: something is wrong with the progress file")
    return None
  except Exception as e:
    print(f"Getting an unknown exception loading progress: {e}")
    return None 

def get_exercises():
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
    print("Error something is wrong with the exercises files")
    return None
  except Exception as e:
    print(f"Getting an unknown exception loading exercises: {e}")
    return None
  
def save_progress(data): 
  try: 
    with open("data/progress.json", "w") as file: 
      json.dump(data, file, indent=2)
    return True
  except Exception as e:
    print(f"Error saving progress: {e}")
    return False

def save_exercises(data):
  for i, exercise in enumerate(data["exercises"], 1):
    print(f"{i} {exercise['name']}")
  try:
    with open("data/exercises.json", "w") as file:
      json.dump(data, file, indent=2)
    return True
  except Exception as e:
    print(f"Error saving exercises: {e}")
    return False
  
def get_exercise_names(data):
  exercises = data["exercises"]
  exercise_names = [exercise["name"] for exercise in exercises]
  return exercise_names