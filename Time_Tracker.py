"""
Time Tracking and Productivity Analyzer

This CLI-based tool helps users track time spent on projects, calculate productivity,
analyze deadline performance, and generate actionable reports.

Usage:
    python tracker.py load --file data.csv
    python tracker.py report

Department: Computer science
Group: 30
"""

# Import required libraries
from datetime import datetime,timedelta             # For working with date and time
import csv                                # For reading CSV files
import argparse                           # For bcvuilding a command-line interface
from collections import defaultdict       # For default dictionary to accumulate durations

# Define the main class for the productivity tracker
class ProductivityTracker:
    def __init__(self):
        self.entries = []                 # Stores all the task entries from the CSV
        self.Total_hours = 0              # Total time tracked
        self.Totalprod_hours = 0          # Total productive time
        self.efficiency = 0               # Efficiency percentage
        self.break_time = 0               # Total break time
        self.goals_percent = 0            # Percentage of productive goals achieved
        self.on_time_percent = 0          # Percentage of tasks completed on time
        self.most_time_project = ""       # Project with most time spent
        self.project_time = {}            # Dictionary of xg5   names and their durations
        self.project_deadlines = {}       # Dictionary of deadlines left for each project
        self.time_break = "medium"        # Break time rating: low, medium, or high

    # Load the CSV file into memory
    def load_csv(self, filepath):
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)     # Read CSV into dictionary rows
            for row in reader:
                try:
                    # Parse Start and End times into datetime objects
                    row['Start'] = datetime.strptime(row['Start'], "%Y-%m-%d %H:%M")
                    row['End'] = datetime.strptime(row['End'], "%Y-%m-%d %H:%M")
                    
                    # Parse deadline if it exists
                    deadline = row.get('Deadline')
                    if deadline:
                        row['Deadline'] = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
                    else:
                        row['Deadline'] = None
                    
                    # Calculate duration in hours
                    row['Duration'] = (row['End'] - row['Start']).total_seconds() / 3600
                    
                    # Add the row to the entries list
                    self.entries.append(row)
                except Exception as e:
                    print(f'Skipping row due to error: {e}')   # Handle any errors in row parsing
                
    # Calculate total and productive hours and efficiency
    def calculate_workhours(self):
        for entry in self.entries:
            self.Total_hours += entry['Duration']            # Sum all duration
            if entry['Productive'].strip().lower() == 'yes':
                self.Totalprod_hours += entry['Duration']     # Sum productive time
        if self.Total_hours > 0:
            self.efficiency = (self.Totalprod_hours / self.Total_hours) * 100  # Compute efficiency
        

    # Analyze how time is distributed across projects and determine break usage
    def project_analysis(self):
        project_time = defaultdict(float)      # Track total time per project
        project_prodtime = defaultdict(float)  # Track productive time per project

        for entry in self.entries:
            project = entry['Project']
            project_time[project] += entry['Duration']       # Add to total time
            if entry['Productive'].strip().lower() == 'yes':
                project_prodtime[project] += entry['Duration']  # Add to productive time

        self.project_time = dict(sorted(project_time.items()))  # Store sorted total time per project
        
        # Calculate productivity % per project (not used here, but could be printed)
        project_prodpercent = {
            project: (project_prodtime[project] / project_time[project]) * 100
            for project in project_time
        }

        # Handle break time logic
        for key in self.project_time:
            if key.lower() == 'break':
                self.break_time = self.project_time[key]

        # Calculate break ratio and categorize it
        break_ratio = (self.break_time / self.Total_hours) * 100 if self.Total_hours else 0
        if break_ratio > 25:
            self.time_break = 'high'
        elif break_ratio >= 20:
            self.time_break = 'medium'
        else:
            self.time_break = 'low'

        # Determine the project with the highest time spent
        self.most_time_project = max(self.project_time, key=self.project_time.get)

    # Evaluate goal achievement and deadline performance
    def goal_achievement(self):
        goals = 0         # Productive non-break entries
        on_time = 0       # Entries completed before deadline
        total = len(self.entries)

        for entry in self.entries:
            if entry['Project'].strip().lower() != 'break' and entry['Productive'].strip().lower() == 'yes':
                goals += 1
            if entry['Deadline'] is not None and entry['End'] <= entry['Deadline']:
                on_time += 1

        if total > 0:
            self.goals_percent = (goals / total) * 100         # % of goals achieved
            self.on_time_percent = (on_time / total) * 100     # % of deadlines met

    # Calculate time remaining for each project deadline
    def project_deadline(self):
        self.project_deadlines = {}
        for entry in self.entries:
            if entry['Deadline'] is not None:
                diff = (entry['Deadline'] - entry['End']).total_seconds()
                self.project_deadlines[entry['Project']] = str(timedelta(seconds = diff))

    # Print the full productivity report
    def generate_report(self):
        print("\n📝 PRODUCTIVITY REPORT")
        print(f"Total Time Tracked: {self.Total_hours:.2f} hrs")
        print(f"Productive Time: {self.Totalprod_hours:.2f} hrs")
        print(f"Non-Productive Time: {self.Total_hours - self.Totalprod_hours:.2f} hrs")
        print(f"Efficiency: {self.efficiency:.2f}%")
        print(f"Total Break Time: {self.break_time:.2f} hrs")
        print(f"Most Time Spent On: {self.most_time_project} ({self.project_time[self.most_time_project]:.2f} hrs)")

        print("\n💡 TIME MANAGEMENT RECOMMENDATIONS")
        print(f"Break time: {self.break_time:.2f} hrs")
        if self.time_break == 'high':
            print("- Reduce break frequency to avoid time waste.")
        elif self.time_break == 'low':
            print("- Increase break frequency to avoid burnout.")
        if self.efficiency < 60:
            print("- Improve focus by batching similar tasks or reducing distractions.")

        print("\n🚀 EFFICIENCY IMPROVEMENT STRATEGIES")
        if self.goals_percent < 60:
            print("- Try setting more achievable goals.")
        if self.on_time_percent < 60:
            print("- Work more efficiently to meet deadlines.")
        print("- Use Pomodoro (25 min work + 5 min break).")
        print("- Review your top time-consuming projects weekly.")
        print("- Allocate productive hours to priority work.")
        print("- Avoid frequent task switching.")

        print("\n⏳ TIME REMAINING ON PROJECTS")
        for key, hours_left in self.project_deadlines.items():
            print(f"{key} -- {hours_left} hrs")

# CLI (Command Line Interface) entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Time Tracking and Productivity Analyzer')  # Create CLI parser
    subparsers = parser.add_subparsers(dest='command')  # Add subcommands (load, report)

    # Subcommand: load CSV
    load_parser = subparsers.add_parser('load')         # Add 'load' command
    load_parser.add_argument('--file', required=True)   # Add --file argument

    # Subcommand: generate report
    subparsers.add_parser('report')                     # Add 'report' command

    args = parser.parse_args()                          # Parse command-line arguments
    tracker = ProductivityTracker()                     # Create an instance of the tracker

    if args.command == 'load':                          # If user runs 'load' command
        tracker.load_csv(args.file)                     # Load the specified CSV file
        print(f"CSV loaded from {args.file}")           # Confirm load
        tracker.calculate_workhours()
        tracker.project_analysis()
        tracker.goal_achievement()
        tracker.project_deadline()
        tracker.generate_report()        

    
        
        
        