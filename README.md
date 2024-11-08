# IntervalRX

Your prescription to move more during the day and break bad posture habits.

## What is it

IntervalRx is a REPL-based project using timers, a Tkinter GUI, and schedulers to remind you when it’s time to take a mobility break. It helps you stay consistent with your physiotherapy exercises while working at your desk, so you get the most out of your physio.

## How to Run it

Instructions coming soon.

## Roadmap

### Phase1: Project Setup and Core Functionality

#### Project set up basics

- [x] Initialize project files, create virtual env, repo and install dependencies
- [x] Set up basic file structure for code organization

#### Set up REPL

- [x] Implement a simple REPL interface with commands for start, stop, and summary

#### Configure timer and intervals

- [x] Set up timer mechanism to trigger reminders at regular intervals

### Phase 2: Exercise and Tracking Features

#### Add start and stop commands

- [x] Load Exercise Options on Terminal along with reps, frequency

#### Install and Configure Tkinter for Alerts

- [x] Display popup alerts using Tkinter to prompt exercise breaks.
- [x] set up alert behaviour to dismiss alert

#### Add progress tracking

- [x] Track completed and missed exercises in JSON file
- [x] Each completed alert records time

#### End-of-day summary

- [x] Display a summary when user enters stop command.
- [ ] Print completion rate and skipped intervals

#### Roadmap for future features

- [ ] add sound alert
- [ ] add do not disturb mode
- [ ] allow for autocomplete
- [ ] add testing
- [ ] reconfigure procedural fucntions for OOP (turn exercise and commands into a class for scalability)
- [ ] create multiple timers
- [ ] add streaks
