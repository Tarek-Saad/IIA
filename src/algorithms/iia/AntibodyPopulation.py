import sys
import os
# Get the project root directory and add it to Python's module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
import random
from src.algorithms.iia.AntibodyEncoding import AntibodyEncoding

class AntibodyPopulation:
    def __init__(self, filtered_concept_lo_mapping, population_size=100):
        """
        Initialize Antibody Population
        :param filtered_concept_lo_mapping: Dictionary mapping each concept to a filtered list of possible LOs
        :param population_size: Number of antibodies to generate
        """
        self.filtered_concept_lo_mapping = filtered_concept_lo_mapping
        self.population_size = population_size
        self.population = []

    def generate_population(self):
        """
        Generate the initial antibody population.
        - Each antibody follows the encoding rule (one LO per concept).
        - 100 antibodies are randomly generated.
        :return: List of encoded antibodies (learning paths)
        """
        encoding = AntibodyEncoding(self.filtered_concept_lo_mapping)

        for _ in range(self.population_size):
            antibody = encoding.encode_chromosome()
            self.population.append(antibody)

        return self.population
