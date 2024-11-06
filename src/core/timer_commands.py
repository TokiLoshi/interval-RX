import threading 
import time 
from src.core.progress_commands import print_progress
import datetime

def start():
  # check last process log against today's date 
  # update exercises for the day 
  print("starting")
  print_progress()

def stop():
  print(f"stopping...")


def intervals():
  print(f"You have a bunch of intervals")