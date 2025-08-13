# Import the unittest module for testing
import unittest

# Import datetime to create mock timestamps
from datetime import datetime

# Import the ProductivityTracker class from your main script
from Time_Tracker import ProductivityTracker  

# Define a class to group all test cases related to ProductivityTracker
class TestProductivityTracker(unittest.TestCase):

    # Test whether work hours and efficiency are calculated correctly with valid data
    def test_load_valid_data(self):
        tracker = ProductivityTracker()  # Create an instance of the tracker

        # Manually create one time entry
        tracker.entries = [
            {
                'Start': datetime(2025, 7, 21, 9, 0),     # Start time: 9:00 AM
                'End': datetime(2025, 7, 21, 11, 0),      # End time: 11:00 AM
                'Project': 'AI Assistant',               # Project name
                'Deadline': datetime(2025, 8, 1),        # Deadline date
                'Productive': 'Yes',                     # Marked as productive
                'Duration': 2.0                          # Duration in hours
            }
        ]

        tracker.calculate_workhours()  # Calculate total and productive hours

        self.assertEqual(tracker.Total_hours, 2.0)         # Should match duration
        self.assertEqual(tracker.Totalprod_hours, 2.0)     # All hours are productive
        self.assertEqual(tracker.efficiency, 100.0)        # 100% efficiency

    # Test how break time is handled and categorized
    def test_break_time_analysis(self):
        tracker = ProductivityTracker()  # Create an instance of the tracker

        # Create one break entry and one productive entry
        tracker.entries = [
            {
                'Start': datetime(2025, 7, 21, 13, 0),    # 1:00 PM
                'End': datetime(2025, 7, 21, 13, 30),     # 1:30 PM
                'Project': 'Break',                       # Marked as break
                'Deadline': None,                         # No deadline
                'Productive': 'No',                       # Not productive
                'Duration': 0.5                           # 30 minutes break
            },
            {
                'Start': datetime(2025, 7, 21, 14, 0),    # 2:00 PM
                'End': datetime(2025, 7, 21, 16, 0),      # 4:00 PM
                'Project': 'AI Assistant',
                'Deadline': datetime(2025, 8, 1),
                'Productive': 'Yes',
                'Duration': 2.0
            }
        ]

        tracker.calculate_workhours()  # Sum total and productive hours
        tracker.project_analysis()     # Analyze break and work distribution

        self.assertEqual(tracker.break_time, 0.5)          # Break time is 0.5 hrs
        self.assertEqual(tracker.time_break, 'medium')        # 0.5 / 2.5 = 20% → low

    # Test goal achievement and on-time completion percentages
    def test_goal_achievement(self):
        tracker = ProductivityTracker()  # Create an instance of the tracker

        # Two entries: one productive work and one break
        tracker.entries = [
            {
                'Start': datetime(2025, 7, 21, 10, 0),    # 10:00 AM
                'End': datetime(2025, 7, 21, 12, 0),      # 12:00 PM
                'Project': 'Game Engine',
                'Deadline': datetime(2025, 7, 22),
                'Productive': 'Yes',
                'Duration': 2.0
            },
            {
                'Start': datetime(2025, 7, 21, 12, 30),
                'End': datetime(2025, 7, 21, 13, 0),
                'Project': 'Break',
                'Deadline': None,
                'Productive': 'No',
                'Duration': 0.5
            }
        ]

        tracker.goal_achievement()  # Analyze goals met and deadline performance

        self.assertEqual(tracker.goals_percent, 50.0)      # 1 out of 2 productive goals
        self.assertEqual(tracker.on_time_percent, 50.0)    # 1 entry met deadline

# Run the unit tests when this script is executed directly
if __name__ == '__main__':
    unittest.main()