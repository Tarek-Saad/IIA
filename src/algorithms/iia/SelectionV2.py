import random
import numpy as np
from collections import Counter
from src.algorithms.iia.AffinityCalculation import AffinityCalculation
from src.core.repositories.GraphDB import GraphDB

class Selection:
    def __init__(self, ranked_population, affinity_concentration_data, alpha=0.5, threshold=0.5):
        self.ranked_population = ranked_population
        self.affinity_concentration_data = affinity_concentration_data
        self.alpha = alpha
        self.threshold = threshold

    def calculatePv(self, affinity, concentration):
        total_affinity = sum([item[1] for item in self.ranked_population])
        total_concentration = sum([c for _, c in self.affinity_concentration_data])
        Pv = self.alpha * (affinity / total_affinity) + (1 - self.alpha) * (concentration / total_concentration)
        return Pv

    def calculateSPv(self, affinity, concentration):
        total_Pv = sum([
            self.calculatePv(affinity_val, concentration_val)
            for affinity_val, concentration_val in self.affinity_concentration_data
        ])
        SPv = self.calculatePv(affinity, concentration) / total_Pv
        return SPv

    def roulette_wheel_selection(self):
        SPv_values = [
            self.calculateSPv(affinity, concentration)
            for affinity, concentration in self.affinity_concentration_data
        ]

        selection_counts = Counter()
        total_SPv = sum(SPv_values)

        for _ in range(len(self.ranked_population)):
            random_value = random.uniform(0, total_SPv)
            cumulative_SPv = 0.0

            for idx, SPv in enumerate(SPv_values):
                cumulative_SPv += SPv
                if cumulative_SPv > random_value:
                    selection_counts[idx] += 1
                    break

        sorted_selection_counts = sorted(selection_counts.items(), key=lambda x: x[1], reverse=True)

        print("\n==================== 🟣 Selection Results ====================")
        for idx, count in sorted_selection_counts:
            print(f"🔸 Path {idx + 1} was selected {count} times.")
        print("==============================================================")

        best_selected_path_idx = sorted_selection_counts[0][0]
        best_selected_path = self.ranked_population[best_selected_path_idx]

        self.display_best_path_details(best_selected_path, best_selected_path_idx, self.affinity_concentration_data)

        return best_selected_path, best_selected_path_idx  # ✅ return both!

    def display_best_path_details(self, selected_path, path_idx, affinity_concentration_data):
        ls_data, affinity, lo_data, chromosome = selected_path
        concentration = affinity_concentration_data[path_idx][1]

        print("\nBest Selected Path Details:")
        print(f"Path {path_idx + 1} - Affinity: {affinity:.4f}, Concentration: {concentration:.4f}")

        formatted_los = []
        for lo in lo_data:
            formatted_los.append({
                "name": lo.get("name"),
                "difficulty": lo.get("difficulty"),
                "learning_style_visual_verbal": lo.get("learning_style_visual_verbal"),
                "learning_style_sequential_global": lo.get("learning_style_sequential_global"),
                "formatt": lo.get("formatt"),
                "learning_style_sensitive_intuitive": lo.get("learning_style_sensitive_intuitive"),
                "sourcee": lo.get("sourcee"),
                "learning_style_active_reflective": lo.get("learning_style_active_reflective"),
                "lo_id": lo.get("lo_id")
            })

        print(f"Learning Objects: {formatted_los}")
        print(f"Chromosome: {chromosome}")
        print("==============================================================\n")

    def get_filtered_best_path_from_result(self, selected_path, path_idx):
        """
        Return only name and lo_id of the selected path's learning objects.
        """
        lo_data = selected_path[2]
        filtered_los = [
            {"name": lo.get("name"), "lo_id": lo.get("lo_id")}
            for lo in lo_data
        ]
        return {
            "path_index": path_idx + 1,
            "learning_objects": filtered_los
        }


def main():
    learner_email = "kareem@example.com"
    learning_goals = ["Searching"]
    knowledge_base = ["Introduction to Programming"]

    threshold = 0.01
    alpha = 0.5

    affinity_calculator = AffinityCalculation(learner_email, learning_goals, knowledge_base, threshold)
    ranked_population = affinity_calculator.rank_learning_paths()
    affinity_concentration_data = affinity_calculator.get_affinity_and_concentration()

    selection = Selection(ranked_population, affinity_concentration_data, alpha)
    selected_path, selected_index = selection.roulette_wheel_selection()

    # ✅ Filtered version for app/controller
    filtered_best_path = selection.get_filtered_best_path_from_result(selected_path, selected_index)
    print("\n🧪 Filtered Best Path Output (LO Name & ID Only):")
    print(filtered_best_path)

if __name__ == "__main__":
    main()
