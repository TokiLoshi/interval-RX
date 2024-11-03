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

- [ ] Implement a simple REPL interface with commands for start, stop, and summary
- [ ] Test command handling to ensure smooth REPL interaction

#### Configure timer and intervals

- [ ] Set up timer mechanism to trigger reminders at regular intervals
- [ ] Add a integration for how long on this project
- [ ] Add customization of interval duration through a configuration file or REPL input

### Phase 2: Exercise and Tracking Features

#### Add start and stop commands

- [ ] Load Exercise Options on Terminal along with reps, frequency
- [ ] Allow users to specify or rotate through pre-set exercises with each alert

#### Install and Configure Tkinter for Alerts

- [ ] Display popup alerts using Tkinter to prompt exercise breaks.
- [ ] set up alert behaviour to dismiss alert and update progress

#### Add progress tracking

- [ ] Track completed and missed exercises in JSON file
- [ ] Each completed alert records time and completion status

#### End-of-day summary

- [ ] Display a summary when user enters stop command.
- [ ] Print completion rate and skipped intervals

### Phase3: Testing and Enhancements

#### Add test cases

-[ ] Write test cases to cover REPL command, timer intervals and JSON logging -[ ] Test Tkinter pop-up for stable alert handling

#### Identify and map out stretch features

- [ ] add sound alert
- [ ] add do not disturb mode
