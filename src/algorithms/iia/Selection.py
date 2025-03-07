import random
import numpy as np
from collections import Counter
from src.algorithms.iia.AffinityCalculation import AffinityCalculation


class Selection:
    def __init__(self, ranked_population, affinity_concentration_data, alpha=0.5, threshold=0.5):
        """
        Initialize the Selection class.
        :param ranked_population: The population of ranked learning paths.
        :param affinity_concentration_data: Affinity and concentration values for all learning paths.
        :param alpha: Constant that determines the weight between affinity and concentration.
        :param threshold: The threshold value to determine similarity in affinity calculation.
        """
        self.ranked_population = ranked_population  # A list of tuples containing (LS, Affinity, LO, Chromosome)
        self.affinity_concentration_data = affinity_concentration_data  # Affinity and concentration data from AffinityCalculation
        self.alpha = alpha  # The alpha constant
        self.threshold = threshold  # Threshold for affinity calculation

    def calculatePv(self, affinity, concentration):
        """
        Calculate the expected reproduction rate (P_v) for a given learning path.
        :param affinity: The affinity value (A_v) for the learning path.
        :param concentration: The concentration value (C_v) for the learning path.
        :return: The expected reproduction rate (P_v).
        """
        total_affinity = sum([item[1] for item in self.ranked_population])  # Sum of all affinities
        total_concentration = sum([concentration for _, concentration in
                                   self.affinity_concentration_data])  # Corrected line to sum concentrations
        Pv = self.alpha * (affinity / total_affinity) + (1 - self.alpha) * (concentration / total_concentration)
        return Pv

    def calculateSPv(self, affinity, concentration):
        """
        Calculate the Selection Probability (SP_v) for a given learning path.
        :param affinity: The affinity value (A_v) for the learning path.
        :param concentration: The concentration value (C_v) for the learning path.
        :return: The selection probability (SP_v).
        """
        total_Pv = sum(
            [self.calculatePv(affinity, concentration) for affinity, concentration in self.affinity_concentration_data])
        SPv = self.calculatePv(affinity, concentration) / total_Pv
        return SPv

    def roulette_wheel_selection(self):
        """
        Perform roulette wheel selection based on the selection probabilities (SPv).
        Spin the wheel for the same number of paths in the population and count selections.
        :return: Dictionary with counts for each learning path, showing how many times each path was selected.
        """
        # Calculate the SPv value for each path and store it
        SPv_values = [self.calculateSPv(affinity, concentration) for affinity, concentration in
                      self.affinity_concentration_data]

        # Initialize the selection counts
        selection_counts = Counter()

        # Spin the wheel for the same number of paths in the population
        total_SPv = sum(SPv_values)

        # Spin roulette wheel for each path
        for _ in range(len(self.ranked_population)):
            random_value = random.uniform(0, total_SPv)  # Random number between 0 and the sum of SPv values

            cumulative_SPv = 0.0
            for idx, SPv in enumerate(SPv_values):
                cumulative_SPv += SPv
                if cumulative_SPv > random_value:
                    # Track the selection count for the path
                    selection_counts[idx] += 1
                    break

        # Sort the selection counts in descending order
        sorted_selection_counts = sorted(selection_counts.items(), key=lambda x: x[1], reverse=True)

        # Output the sorted results
        print("\nSelection Counts (How many times each learning path was chosen in each spin):")
        for idx, count in sorted_selection_counts:
            print(f"Path {idx + 1} selected {count} times")

        # Get the index of the highest selected path
        best_selected_path_idx = sorted_selection_counts[0][0]
        print(best_selected_path_idx)

        # Fetch all details of the best-selected path
        best_selected_path = self.ranked_population[best_selected_path_idx]

        # Print the details of the best selected path
        print("\nBest Selected Path Details:")
        print(
            f"Path {best_selected_path_idx + 1} - Affinity: {best_selected_path[1]:.4f}, Concentration: {self.affinity_concentration_data[best_selected_path_idx][1]:.4f}")
        print(f"Learning Objects: {best_selected_path[2]}")
        print(f"Chromosome: {best_selected_path[3]}")

        return sorted_selection_counts


def main():
    # Sample Test Data
    learner_email = "kareem@example.com"
    learning_goals = ["Searching"]
    knowledge_base = ["Introduction to Programming"]
    threshold = 0.5  # Example threshold value for similarity
    alpha = 0.5  # Weight constant for Pv

    # Initialize Affinity Calculation and Rank Learning Paths
    affinity_calculator = AffinityCalculation(learner_email, learning_goals, knowledge_base, threshold)
    ranked_population = affinity_calculator.rank_learning_paths()

    # Fetch affinity and concentration values
    affinity_concentration_data = affinity_calculator.get_affinity_and_concentration()

    # Now pass the output to the Selection class along with the affinity and concentration data
    selection = Selection(ranked_population, affinity_concentration_data, alpha)

    # Perform Roulette Wheel Selection and count how many times each path is selected
    selection_counts = selection.roulette_wheel_selection()

    # Output the selection counts
    print("\nSelection Counts (How many times each learning path was chosen in each spin):")
    for idx, count in selection_counts:
        print(f"Path {idx + 1} selected {count} times")


if __name__ == "__main__":
    main()
