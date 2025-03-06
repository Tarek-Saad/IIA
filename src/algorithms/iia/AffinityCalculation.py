import numpy as np

class AffinityCalculation:
    def __init__(self, learner_profile, learner_logs, population):
        """
        Initialize Affinity Calculation
        :param learner_profile: Dictionary containing learning goals, prior knowledge, and learning style
        :param learner_logs: Dictionary containing past interactions with learning objects (LOs)
        :param population: List of antibodies (learning paths)
        """
        self.learner_profile = learner_profile
        self.learner_logs = learner_logs  # Real-time learner performance data
        self.population = population  # Antibody population (learning paths)

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

        for concept, lo_data in learning_path.items():
            lo_style = lo_data["learning_style"]
            learner_style = self.learner_profile["learning_style"]

            # Compute absolute difference for each learning style dimension
            similarity = sum(abs(learner_style.get(dim, 0) - lo_style.get(dim, 0)) for dim in learner_style)
            style_match_score += similarity

        # Normalize by total LOs and dimensions
        f1 = style_match_score / (total_los * learning_dimensions)
        return f1

    def compute_lo_combination_penalty(self, learning_path):
        """
        Compute the second objective function (f2) - LO Combination Penalty.
        Penalizes LO combinations that have led to poor learning outcomes.
        Equation 4: f2 = (Σ R_{L_i, L_j} * N(L_i ∩ L_j)) / ((M-1) * N(L))
        """
        M = len(learning_path)
        failed_los = self.learner_logs.get("failed_los", {})

        # Ensure failed_los is a dictionary
        if not isinstance(failed_los, dict):
            failed_los = {lo_id: 1 for lo_id in failed_los}

        total_learners = self.learner_logs.get("total_learners", 1)  # Avoid division by zero

        penalty = 0
        for concept_i, lo_i in learning_path.items():
            lo_id_i = lo_i["lo_id"]

            for concept_j, lo_j in learning_path.items():
                lo_id_j = lo_j["lo_id"]
                if lo_id_i != lo_id_j and lo_id_i in failed_los and lo_id_j in failed_los:
                    # R_{L_i, L_j} is the correlation strength (assumed as 1 if both failed before)
                    correlation_strength = 1  
                    num_failed_together = failed_los.get(lo_id_i, 0) + failed_los.get(lo_id_j, 0)
                    penalty += correlation_strength * num_failed_together

        f2 = penalty / ((M - 1) * total_learners) if M > 1 else 0
        return f2

    def compute_fitness(self, learning_path):
        """
        Compute the general fitness function (F_v).
        Equation 2: F_v = Σ (w_i * f_i (U, B))
        """
        w1, w2 = 0.5, 0.5  # Assign equal weights to objectives
        f1 = self.compute_learning_style_fitness(learning_path)
        f2 = self.compute_lo_combination_penalty(learning_path)

        # Compute final fitness value
        F_v = (w1 * f1) + (w2 * f2)
        return F_v

    def compute_affinity(self, learning_path):
        """
        Compute affinity score (A_v) based on fitness (F_v).
        Equation 1: A_v = 1 / (1 + F_v)
        """
        F_v = self.compute_fitness(learning_path)
        A_v = 1 / (1 + max(0, F_v))  # Ensure non-negative fitness
        return A_v

    def compute_antibody_similarity(self, path_v, path_s):
        """
        Compute similarity between two antibodies.
        Equation 5: S_{v,s} = k_{v,s} / L
        """
        matching_count = sum(1 for concept in path_v if path_v[concept]["lo_id"] == path_s[concept]["lo_id"])
        L = len(path_v)  # Number of concepts in the path

        S_vs = matching_count / L if L > 0 else 0
        return S_vs

    def compute_population_diversity(self):
        """
        Compute population diversity (C_v).
        Equation 6: C_v = (Σ I(S_{v,s} > T)) / N
        """
        N = len(self.population)  # Total antibodies
        T = 0.5  # Threshold for similarity

        diversity_scores = []
        for v in self.population:
            similar_count = sum(1 for s in self.population if self.compute_antibody_similarity(v, s) > T)
            C_v = similar_count / N if N > 0 else 0
            diversity_scores.append(C_v)

        return np.mean(diversity_scores)  # Return average diversity score

    def rank_learning_paths(self):
        """
        Rank multiple learning paths based on their affinity score.
        """
        ranked_paths = [(path, self.compute_affinity(path)) for path in self.population]
        ranked_paths.sort(key=lambda x: x[1], reverse=True)  # Higher affinity comes first
        return ranked_paths
