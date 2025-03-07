import numpy as np
from src.algorithms.iia.getLS import getLS
from src.core.services.GetlearnersServices import LearnerServices


class AffinityCalculation:
    def __init__(self, learner_email, learning_goals, knowledge_base, threshold=0.5):
        """
        Initialize Affinity Calculation
        :param learner_email: The learner's email address for retrieving learning style
        :param learning_goals: List of concepts the learner wants to study
        :param knowledge_base: List of concepts the learner already knows
        :param threshold: The threshold for similarity to determine if two antibodies are similar
        """
        self.learner_email = learner_email
        self.learning_goals = learning_goals
        self.knowledge_base = knowledge_base
        self.learner_profile = self.get_learner_profile()
        self.population_data = self.get_population_from_getLS()
        self.ranked_population = []
        self.threshold = threshold  # Threshold value to compare similarity

    def get_learner_profile(self):
        """
        Retrieve the learner's learning style from the database.
        :return: Dictionary containing learning style preferences.
        """
        learner_service = LearnerServices()
        learner_learning_styles = learner_service.get_learner_learning_styles(self.learner_email)
        return {"learning_style": learner_learning_styles}

    def get_population_from_getLS(self):
        """
        Retrieve learning objects (LOs) and their learning styles using the getLS function.
        :return: Dictionary containing both LS and LO data.
        """
        LS_service = getLS()
        result = LS_service.LOsLS(self.learning_goals, self.knowledge_base)
        return result  # Returns {"LSs": learning styles, "LOs": learning objects, "chromosomes": chromosomes}

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
        return 1 / F_v

    def rank_learning_paths(self):
        """
        Compute affinity scores for all learning paths and rank them.
        Display ranked paths with selected LOs, Learning Styles, and Chromosomes.
        """
        LSs = self.population_data["LSs"]
        LOs = self.population_data["LOs"]
        chromosomes = self.population_data["chromosomes"]

        # Combining LS, LOs, and chromosomes into ranked population
        self.ranked_population = [
            (LS, self.compute_affinity(LS), LO, chromosome)
            for LS, LO, chromosome in zip(LSs, LOs, chromosomes)
        ]

        # Sort by affinity score
        # self.ranked_population.sort(key=lambda x: x[1], reverse=True)  # Higher affinity comes first

        print("\n===== Ranked Learning Paths =====")
        for i, (ls_data, affinity, lo_data, chromosome) in enumerate(self.ranked_population):
            print(f"\nPath {i + 1}:")
            print(f"Affinity Score: {affinity:.4f}")

            for j, (ls, lo) in enumerate(zip(ls_data, lo_data)):
                print(f"  LO {j + 1}: {lo}")  # Displays LO ID and metadata
                print(f"  LS: {ls}")  # Displays corresponding learning style

            print(f"  Chromosome: {chromosome}")  # Display the chromosome for each path

        print("\n===== self.ranked_population NEWWW =====")
        print(self.ranked_population[0][2])

        return self.ranked_population

    def calculate_forrest_affinity(self, chromosome1, chromosome2):
        """
        Calculate the Forrest's R Consecutive Matching Method for affinity between two antibodies (chromosomes).
        """
        # Count the number of consecutive matching bits between the two chromosomes
        consecutive_matching = 0
        max_consecutive = 0
        for a, b in zip(chromosome1, chromosome2):
            if a == b:
                consecutive_matching += 1
                max_consecutive = max(max_consecutive, consecutive_matching)
            else:
                consecutive_matching = 0

        # Get the number of Learning Objects (LOs) instead of chromosome length
        total_los = len(self.population_data["LOs"])

        # Calculate the affinity using the formula
        affinity = max_consecutive / total_los if total_los > 0 else 0  # Ensure we don't divide by zero
        return affinity

    def calculate_concentration(self, target_chromosome, population_chromosomes):
        """
        Calculate the concentration of antibodies for a single path.
        This is equivalent to Cv and depends on the threshold for similarity.
        """
        N = len(population_chromosomes)  # Size of the population
        total_affinity = 0

        # For each pair of antibodies, calculate the affinity with the target chromosome
        for chromosome in population_chromosomes:
            affinity_score = self.calculate_forrest_affinity(target_chromosome, chromosome)

            # If the affinity score exceeds the threshold, consider it as similar
            if affinity_score > self.threshold:
                total_affinity += 1  # Add 1 for the similarity

        # Calculate the concentration Cv (dividing by N to normalize)
        Cv = total_affinity / N if N > 0 else 0
        return Cv

    def calculate_and_show_Cv(self):
        """
        Calculate and show the Cv (concentration) value for each path.
        """
        chromosomes = [path[3] for path in self.ranked_population]  # Extracting chromosomes
        for i, target_chromosome in enumerate(chromosomes):
            Cv_value = self.calculate_concentration(target_chromosome, chromosomes)
            print(f"Path {i + 1} - Cv value: {Cv_value:.4f}")

    def get_affinity_and_concentration(self):
        """
        Get the affinity and concentration values for all ranked learning paths.
        :return: List of arrays where each array contains the affinity and concentration for a path.
        """
        results = []
        for _, affinity, _, chromosome in self.ranked_population:
            concentration = self.calculate_concentration(chromosome, [path[3] for path in self.ranked_population])
            results.append([affinity, concentration])

        print(results)
        return results


if __name__ == "__main__":
    # Sample Test Data
    learner_email = "kareem@example.com"
    learning_goals = ["Searching"]
    knowledge_base = ["Introduction to Programming"]
    threshold = 0.5  # Example threshold value for similarity

    # Initialize Affinity Calculation and Rank Learning Paths
    affinity_calculator = AffinityCalculation(learner_email, learning_goals, knowledge_base, threshold)
    print(affinity_calculator.rank_learning_paths())

    # # Calculate and display the Cv value for each path
    # affinity_calculator.calculate_and_show_Cv()
    #
    # # Get the affinity and concentration values for each ranked learning path
    affinity_concentration_list = affinity_calculator.get_affinity_and_concentration()
    # print("\nAffinity and Concentration Values:")
    # for i, (affinity, concentration) in enumerate(affinity_concentration_list):
    #     print(f"Path {i + 1}: Affinity = {affinity}, Concentration = {concentration}")
