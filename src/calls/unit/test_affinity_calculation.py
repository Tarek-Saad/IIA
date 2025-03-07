from src.algorithms.iia.AffinityCalculation import AffinityCalculation

# Sample Test Data
learner_email = "kareem@example.com"
learning_goals = ["Searching"]
knowledge_base = ["Introduction to Programming"]

# Initialize Affinity Calculation and Rank Learning Paths
affinity_calculator = AffinityCalculation(learner_email, learning_goals, knowledge_base)
affinity_calculator.rank_learning_paths()
