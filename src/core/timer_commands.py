import datetime, timedelta  
from src.core.progress_commands import print_progress
import tkinter as tk 

class DeskTimer:
  def __init__(self):
    self.timer_running = False 
    self.total_time = 0
    self.work_interval = 30
    self.root = None
    self.reminder_window = None
    self.next_reminder_time = None
    self.check_reminder_id = None

  # Start the timer 
  def start(self):
    if not self.timer_running: 
      # Initialize main window 
      self.root = tk.Tk()
      self.root.title("Desk Timer")
      self.root.geometry("300x100")
      self.status_label = tk.Label(self.root, text="Timer is running...")
      self.status_label.pack(pady=20)

      # Set up timer
      self.timer_running = True
      self.next_reminder_time = datetime.now() + timedelta(seconds=self.work_interval)
      print(f"Timer started...{datetime.now()}")
      self._check_reminder()

      self.root.protocol("WM_DELETE_WINDOW", self.stop)
      self.root.update()
      return "Timer started"
    return "Timer is already running"

  def stop(self):
    if self.timer_running:
      print("Stopping timer")
      self.timer_running = False
      print(f"Total desktime: {self.total_time / 60:.2} minutes")
      
      # Cancel any pending reminders 
      if self.root and self.check_reminder_id:
        self.root.after_cancel(self.check_reminder_id)
        self.reminder_id = None

      # Clean up windows:
      if self.reminder_window:
        self.reminder_window.destroy()
        self.reminder_window = None 

      if self.root:
        self.root.destroy()
        self.root = None
      return "Timer Stopped"
    return "Timer is not running "
  
  def _check_reminder(self):
    if not self.reminder.running or not self.root:
      return 
    current_time = datetime.now()
    time_until = self.next_reminder_time - current_time

    self.status.label.config(
      text=f"Next reminder in: {time_until} seconds\nTotalTime: {self.total_time/60:.1f}"
    )

    # Show reminder if it's time 
    if current_time >= self.next_reminder_time:
      self.total_time += self.work_interval
      self._show_reminder()
      self.next_reminder_time = current_time + timedelta(seconds=self.work_interval)

    # Schedule next check and update GUI
    if self.timer_running and self.root:
      try:
        self.check_reminder_id = self.root.after(1000, self._check_reminder)
        self.root.update()
      except tk.TclError:
        self.timer_running = False 

  def _show_reminder(self):
    if not self.reminder_window and self.root:
      try:
        self.reminder_window = tk.Toplevel(self.root)
        self.reminder_window.title("Time to move")
        self.reminder_window.geometry("300x200")
        self.reminder_window.transient(self.root)

        message = tk.Label(self.reminder_window, 
                           text=f"Time to fix that shoulder!\n\nYou've been sitting for {self.work_interval/50:.1f} minutes", 
                           wraplength=250)
        message.pack(pady=20)
        done_button = tk.Button(
          self.reminder_window,
          text="Done",
          command=self.close_reminder
        )

        done_button.pack(pady=10)

      except tk.TclError as e:
        print(f"Error showing reminder: {e}")
        self.reminder_window = None
      
    else:
      print("Window isn't available")

  def _close_reminder(self):
    if self.reminder_window:
      try:
        if self.reminder_window:
          self.reminder_window.destroy()
          self.reminder_window = None
      except tk.TclError as e:
        print(f"Error closing reminder: {e}")
