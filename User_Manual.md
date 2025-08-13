# Time Tracking and Productivity Analyzer

This is a command-line Python tool to help you track how you spend your time, how productive you are, and how well you're meeting deadlines.

## Features

- Load time tracking data from a CSV file
- Calculate total hours and productive hours
- Analyze time spent on each project
- Show how much break time you take
- Check how well you're meeting deadlines
- Give tips to improve productivity

## Files

- `Time_Tracker.py` – Main program file
- `Tracker_Test.py` – Unit tests for main features
- `data1.csv` to `data5.csv` – Example CSV files with tracking data
- `User_Manual.md` – This user guide

## CSV File Format

Each row should follow this format:

Start,End,Project,Deadline,Productive 
2025-07-21 09:00,2025-07-21 11:00,AI Assistant,2025-08-01,Yes

- `Start` and `End` – The time you started and ended a task (use `YYYY-MM-DD HH:MM`)
- `Project` – The project or task name
- `Deadline` – When the project is due (can be empty)
- `Productive` – Yes if it was productive time, No otherwise

## How to Use

1. Open a terminal and navigate to the folder with `Time_Tracker.py`
2. To load data and view the productivity report:

python Time_Tracker.py load --file data1.csv

## Running Unit Tests

Run the test file to make sure everything works:

python Tracker_Test.py

## Requirements

- Python 3.8 or later
- Uses only standard libraries: `csv`, `datetime`, `argparse`, `unittest`, `collections`