import sys
import os
# Get the project root directory and add it to Python's module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from src.algorithms.iia.AffinityCalculation import AffinityCalculation

# Sample Test Data
learner_email = "kareem@example.com"
learning_goals = ["Searching"]
knowledge_base = ["Introduction to Programming"]

# Initialize Affinity Calculation and Rank Learning Paths
affinity_calculator = AffinityCalculation(learner_email, learning_goals, knowledge_base)
affinity_calculator.rank_learning_paths()
