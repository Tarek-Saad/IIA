import numpy as np
from src.algorithms.iia.Pop_index_LO_match import GetLOMatching
from src.core.services.ExtractFromLOs import ExtractFromLOs
from src.core.services.GetlearnersServices import LearnerServices

class AffinityCalculation:
    def __init__(self, learner_email, learning_goals, knowledge_base):
        """
        Initialize Affinity Calculation
        :param learner_email: The learner's email address for retrieving learning style
        :param learning_goals: List of concepts the learner wants to study
        :param knowledge_base: List of concepts the learner already knows
        """
        self.learner_email = learner_email
        self.learning_goals = learning_goals
        self.knowledge_base = knowledge_base
        self.learner_profile = self.get_learner_profile()
        self.population = self.get_population_from_db()
        self.ranked_population = []

    def get_learner_profile(self):
        """
        Retrieve the learner's learning style from the database.
        :return: Dictionary containing learning style preferences.
        """
        learner_service = LearnerServices()
        learner_learning_styles = learner_service.get_learner_learning_styles(self.learner_email)
        return {"learning_style": learner_learning_styles}

    def get_population_from_db(self):
        """
        Retrieve learning objects (LOs) and their learning styles from the database.
        :return: List of learning paths (antibodies) with learning style metadata.
        """
        lo_matcher = GetLOMatching()
        matched_los = lo_matcher.getLOMatch(self.learning_goals, self.knowledge_base)

        lo_extractor = ExtractFromLOs()
        all_paths_learning_styles = lo_extractor.extract_learning_styles_for_paths(matched_los["selected_los"])
        return all_paths_learning_styles

    def compute_learning_style_fitness(self, learning_path):
        """
        Compute the first objective function (f1) - Learning Style Fitness.
        Measures how well the LO’s characteristics match the learner’s learning style.
        Equation 3: f1 = (1 / (M * k)) * Σ | ULS_j - LLS_{i,j} |
        """
        style_match_score = 0
        total_los = len(learning_path)
        learning_dimensions = len(self.learner_profile["learning_style"])  # k

        if total_los == 0:
            return 0  # Prevent division by zero

        for lo_data in learning_path:
            lo_style = lo_data  # Directly using LO's learning style dict
            learner_style = self.learner_profile["learning_style"]

            # Compute absolute difference for each learning style dimension
            similarity = sum(abs(learner_style.get(dim, 0) - lo_style.get(dim, 0)) for dim in learner_style)
            style_match_score += similarity

        # Normalize by total LOs and dimensions
        f1 = style_match_score / (total_los * learning_dimensions)
        return f1

    def compute_fitness(self, learning_path):
        """
        Compute the general fitness function (F_v).
        Equation 2: F_v = f1 (Since f2 is removed)
        """
        f1 = self.compute_learning_style_fitness(learning_path)
        return f1  # Since f2 is removed, F_v = f1

    def compute_affinity(self, learning_path):
        """
        Compute affinity score (A_v) based on fitness (F_v).
        Equation 1: A_v = 1 / F_v
        """
        F_v = self.compute_fitness(learning_path)
        if F_v == 0:
            return float('inf')  # Prevent division by zero; a perfect match should have very high affinity.
        return 1 / F_v  # Using the correct affinity formula

    def rank_learning_paths(self):
        """
        Compute affinity scores for all learning paths and rank them.
        """
        self.ranked_population = [(path, self.compute_affinity(path)) for path in self.population]
        self.ranked_population.sort(key=lambda x: x[1], reverse=True)  # Higher affinity comes first

        print("\n===== Ranked Learning Paths =====")
        for i, (path, affinity) in enumerate(self.ranked_population):
            print(f"Path {i+1}: Affinity Score = {affinity:.4f}")

        return self.ranked_population
