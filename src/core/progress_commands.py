from src.utils.json_helpers import get_exercises, get_progress, save_progress, get_exercise_names
from src.utils.input_helpers import get_user_input, get_numeric_input, select_option, get_yes_no
from src.utils.exercise_helpers import get_exercise_options, print_exercises, print_field_values
from datetime import datetime 

def print_progress(current_date=None):
  # Some functions pass in dates, others won't 
  if current_date is None:
    current_date = datetime.now().strftime("%d/%m/%Y")
  
  # Get progress
  all_progress = get_progress()
  progress = all_progress["progress"]

  # get exercise data 
  all_exercises = get_exercises()
  if all_exercises is None: 
    print("\nFailed to load exercises")
    return False 

  print(f"\n===== Your progress for today: {current_date} =====\n")

  # Validate progress
  if not progress or current_date not in progress:
    print("\nNo exercises completed yet today. Here's what you need to do today:")
    for exercise in all_exercises["exercises"]:
      print(f"\n========== {exercise['name']} ==========")
      print(f"--> Target: {exercise['sets']} of {exercise['reps_per_set']} reps")
      print(f"--> {exercise['frequency']} x times today")
    print("\n")
    return True 
  
  completed_exercises = progress[current_date]["exercises"]

  # Lookup dictionary 
  completed_lookup = {
    ex["name"]: ex for ex in completed_exercises 
  }
  total_exercises = len(all_exercises["exercises"])
  completed_count = 0 

  print(f"\n====== Today's Progress: {current_date} ===========")

  for exercise in all_exercises["exercises"]:
    exercise_name = exercise["name"]
    completed = completed_lookup.get(exercise_name)
    print(f"\n{exercise_name}")

    if completed:
      sets_done = completed["sets_completed"]
      reps_done = completed["reps_completed"]
      total_done = completed["total_reps"]
      target_sets = exercise["sets"]
      target_reps = exercise["reps_per_set"]
      target_frequency = exercise["frequency"]

      # Remaining work 
      sets_left = target_sets - sets_done
      reps_left = (target_sets * target_reps) - reps_done 
      completion_percentage = (total_done / (target_sets * target_reps * target_frequency)) * 100 

      print(f"\n--> Sets: {sets_done}/{target_sets} completed.")
      print(f"--> {reps_done}/{target_reps} completed.")
      print(f"--> Progress: {completion_percentage}")

      if completed.get("notes"):
        print("Notes:...")
        for note in completed["notes"]:
          print(f"  . { note}")

      if sets_left > 0 or reps_left > 0:
        print(f"--> Remaining: {sets_left} sets, {reps_left}")
      else: 
        print("** Complete! :)")
        completed_count += 1
        print(f"Last updated: {completed['last_updated']}")
    else:
      print(f"\nNot started yet")
      print(f"Target: {exercise['sets']} sets of {exercise['reps_per_set']} reps")
      print(f"To be completed {exercise['frequency']} x times today")


  print(f"==== Daily Summary ===")
  progress_total = (completed_count / total_exercises) * 100
  print(f"{progress_total:.1f}% of exercises completed")
  if completed_count == total_exercises:
    print(f"Congratulations you're done for the day!")
  else:
    remaining = total_exercises = completed_count
    print(f"Keep going! You have {remaining} exercises to go")
  return True

def log_exercise():
  print("=== Recording Exercise ===")
  
  # Load exercises and progress
  data = get_exercises()
  if data is None: 
    print("Failed to load exercises")
    return False
  
  while True: 
    # Show available options 
    exercise_options = get_exercise_options(data)
    print("\n=== Your Routine Exercises ===")
    print_exercises(exercise_options)
    print("\n")

    # Get exercise selection
    print("\nExcellent! Which Exercise did you do?")
    name = select_option(exercise_options)
    if name is False:
      print("Exiting...")
      return False
    
    selected_exercise = None 
    for exercise in data["exercises"]:
      if exercise["name"].lower() == name.lower():
        selected_exercise = exercise.copy()
        break 
    
    if selected_exercise is None: 
      print(f"\nCould not find exercise: {name}")
      print_exercises(exercise_options)
      continue

    print(f"\n=== Logging: {name} ===")
    for key, value in selected_exercise.items():
      print_field_values(key, value)
    print("\n")
    
    # Load progress data 
    progress_data = get_progress() 
    if progress_data is None: 
      print("Failed to load progress")
      return False 
    
    # Get current date
    current_date = datetime.now().strftime("%d/%m/%Y")
    current_time = datetime.now().strftime("%H:%M:%S")
    
    if current_date not in progress_data["progress"]:
      progress_data["progress"][current_date] = {
        "exercises" : []
      } 
    
    sets = get_numeric_input("\nHow many sets did you do? ")
    reps = get_numeric_input("\nHow many reps did you do? ")
    hold_time = get_user_input("\nHow long did you hold if for? ")
    total_reps = sets * reps 
    daily_count = 1
    notes = get_user_input("\nDo you have any notes to share? ")
    notes = notes if notes.strip() else None

    current_time = datetime.now().strftime("%H:%M:%S")
    
    exercise_entry = {
      "name" : name,
      "sets_completed" : sets, 
      "reps_completed" : reps, 
      "total_reps" : total_reps,
      "hold_time" : hold_time,
      "frequency" : daily_count,
      "last_updated" : current_time,
      "notes" : [notes] if notes else []
    }

    # Find existing data for today if it exists
    todays_exercises = progress_data["progress"][current_date]["exercises"]
    existing_exercise = next(
      (ex for ex in todays_exercises if ex["name"].lower() == name.lower()),
      None
    )

    if existing_exercise:
      print(f"\nYou're making progress, it's great that you're doing more of these! Let's go! Tell me more...")
      existing_exercise["sets_completed"] += sets 
      existing_exercise["reps_completed"] += reps
      existing_exercise["total_reps"] += total_reps
      if hold_time:
        existing_exercise["hold_time"] += hold_time
      existing_exercise["frequency"] += daily_count
      if notes:
        existing_exercise["notes"].append(notes)
      existing_exercise["last_updated"] = current_time
      exercise_info = exercise_entry
    else:
      todays_exercises.append(exercise_entry)
      exercise_info = exercise_entry  
  
    if not save_progress(progress_data):
      print("\nFailed to save progress")
      return False 
    
    print("\nSaved progress! Well done and keep going!\n")
    print_progress(current_date)
    if not get_yes_no("\nWould you like to log another exercise? "):
      return True
  
