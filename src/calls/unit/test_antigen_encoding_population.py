import sys
import os

# Get the project root directory and add it to Python's module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
import random
from src.algorithms.iia.RecognitionOfAntigen import RecognitionOfAntigen
from src.algorithms.iia.AntibodyEncoding import AntibodyEncoding
from src.algorithms.iia.AntibodyPopulation import AntibodyPopulation

# ====== Step 1: Define Test Data ======
# Sample Learner Profile (Antigen)
learner_profile = {
    "learning_goals": ["Recursion", "Sorting"],
    "prior_knowledge": ["Functions"],
    "learning_style": {
        "visual": 0.8,
        "verbal": 0.2
    }
}

# Sample Concept-LO Mapping (Before Recognition of Antigen)
concept_lo_mapping = {
    "Functions": [
        {"lo_id": 1, "learning_style": {"visual": 0.7, "verbal": 0.3}},
        {"lo_id": 2, "learning_style": {"visual": 0.5, "verbal": 0.5}}
    ],
    "Recursion": [
        {"lo_id": 3, "learning_style": {"visual": 0.9, "verbal": 0.1}},
        {"lo_id": 4, "learning_style": {"visual": 0.2, "verbal": 0.8}}
    ],
    "Sorting": [
        {"lo_id": 5, "learning_style": {"visual": 0.6, "verbal": 0.4}},
        {"lo_id": 6, "learning_style": {"visual": 0.3, "verbal": 0.7}}
    ]
}

# ====== Step 2: Apply Recognition of Antigen ======
recognition = RecognitionOfAntigen(learner_profile, concept_lo_mapping)
filtered_mapping = recognition.filter_los()

print("\n===== Filtered Concept-LO Mapping (After Recognition of Antigen) =====")
for concept, los in filtered_mapping.items():
    print(f"{concept}: {[lo['lo_id'] for lo in los]}")

# ====== Step 3: Apply Antibody Encoding ======
encoding = AntibodyEncoding(filtered_mapping)

# Generate Single Chromosome (Antibody)
chromosome = encoding.encode_chromosome()

print("\n===== Generated Chromosome (Antibody) =====")
for concept, data in chromosome.items():
    print(f"{concept}: LO {data['lo_id']} -> Encoding {data['encoding']}")

# ====== Step 4: Generate Population of Antibodies ======
population_generator = AntibodyPopulation(filtered_mapping, population_size=100)
population = population_generator.generate_population()

print("\n===== Generated Population (First 3 Antibodies) =====")
for i in range(3):  # Print only first 3 antibodies for readability
    print(f"Antibody {i+1}:")
    for concept, data in population[i].items():
        print(f"  {concept}: LO {data['lo_id']} -> Encoding {data['encoding']}")
    print()
