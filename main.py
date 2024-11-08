from src.core.repl import repl 
from src.core.timer_commands import DeskTimer
import signal

def handle_interrupt(signum, frame): 
  print("\nKeyboard interrupt, shutting dowin...")
  exit(0)

def main():
  print("\n========= Welcome to IntervalRX =========\n")
  print("\nEnter 'start' to start an interval or 'help' to get the menu options\n")
  signal.signal(signal.SIGINT, handle_interrupt)
  try:
    desk_timer = DeskTimer()
    repl(desk_timer)
    print("\n=========    Happy coding :)   =========\n")
  except KeyboardInterrupt:
    print("============= See you later ============")


if __name__ == "__main__":
  main()