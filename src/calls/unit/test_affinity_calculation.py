import sys
import os
# Get the project root directory and add it to Python's module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
import numpy as np
from src.algorithms.iia.AffinityCalculation import AffinityCalculation

# ====== Step 1: Define Test Data ======

# Sample Learner Profile
learner_profile = {
    "learning_goals": ["Recursion", "Sorting"],
    "prior_knowledge": ["Functions"],
    "learning_style": {
        "visual": 0.8,
        "verbal": 0.2
    }
}

# Sample Learner Logs (Past Performance)
learner_logs = {
    "failed_los": {4: 3, 6: 2},  # LOs the learner previously failed
    "total_learners": 50  # Total learners for normalization
}

# Sample Population (3 Learning Paths for Testing)
population = [
    {
        "Functions": {"lo_id": 1, "learning_style": {"visual": 0.7, "verbal": 0.3}},
        "Recursion": {"lo_id": 3, "learning_style": {"visual": 0.9, "verbal": 0.1}},
        "Sorting": {"lo_id": 5, "learning_style": {"visual": 0.6, "verbal": 0.4}}
    },
    {
        "Functions": {"lo_id": 2, "learning_style": {"visual": 0.5, "verbal": 0.5}},
        "Recursion": {"lo_id": 4, "learning_style": {"visual": 0.2, "verbal": 0.8}},  # Failed LO
        "Sorting": {"lo_id": 6, "learning_style": {"visual": 0.3, "verbal": 0.7}}  # Failed LO
    },
    {
        "Functions": {"lo_id": 1, "learning_style": {"visual": 0.7, "verbal": 0.3}},
        "Recursion": {"lo_id": 3, "learning_style": {"visual": 0.9, "verbal": 0.1}},
        "Sorting": {"lo_id": 6, "learning_style": {"visual": 0.3, "verbal": 0.7}}  # Failed LO
    }
]

# ====== Step 2: Initialize Affinity Calculation ======
affinity_calculator = AffinityCalculation(learner_profile, learner_logs, population)

# ====== Step 3: Compute and Print Results ======

print("\n===== Learning Style Fitness (f1) =====")
for i, path in enumerate(population):
    f1 = affinity_calculator.compute_learning_style_fitness(path)
    print(f"Path {i+1}: f1 = {f1:.4f}")

print("\n===== LO Combination Penalty (f2) =====")
for i, path in enumerate(population):
    f2 = affinity_calculator.compute_lo_combination_penalty(path)
    print(f"Path {i+1}: f2 = {f2:.4f}")

print("\n===== Fitness Score (F_v) =====")
for i, path in enumerate(population):
    fitness = affinity_calculator.compute_fitness(path)
    print(f"Path {i+1}: F_v = {fitness:.4f}")

print("\n===== Affinity Score (A_v) =====")
for i, path in enumerate(population):
    affinity = affinity_calculator.compute_affinity(path)
    print(f"Path {i+1}: A_v = {affinity:.4f}")

print("\n===== Antibody Similarity (S_{v,s}) =====")
similarity_score = affinity_calculator.compute_antibody_similarity(population[0], population[1])
print(f"Similarity between Path 1 and Path 2: S_v,s = {similarity_score:.4f}")

print("\n===== Population Diversity (C_v) =====")
diversity_score = affinity_calculator.compute_population_diversity()
print(f"Population Diversity: C_v = {diversity_score:.4f}")

print("\n===== Ranked Learning Paths =====")
ranked_paths = affinity_calculator.rank_learning_paths()
for i in range(len(ranked_paths)):
    print(f"Path {i+1}: Affinity Score = {ranked_paths[i][1]:.4f}")
