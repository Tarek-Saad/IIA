import sys
import os
# Get the project root directory and add it to Python's module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from src.algorithms.iia.RecognitionOfAntigen import RecognitionOfAntigen
from src.algorithms.iia.AntibodyEncoding import AntibodyEncoding
from src.algorithms.iia.AntibodyPopulation import AntibodyPopulation

class IIAProcessor:
    def __init__(self, learner_profile, concept_lo_mapping, population_size=100):
        """
        Initialize the IIA Processor
        :param learner_profile: Dictionary containing learning goals, prior knowledge, and learning style
        :param concept_lo_mapping: Dictionary mapping each concept to a list of possible LOs
        :param population_size: Number of antibodies to generate
        """
        self.learner_profile = learner_profile
        self.concept_lo_mapping = concept_lo_mapping
        self.population_size = population_size
        self.population = []

    def generate_population(self):
        """
        1. Apply Recognition of Antigen to filter out irrelevant LOs.
        2. Encode selected LOs into antibodies (learning paths).
        3. Generate an initial population of 100 antibodies.
        :return: List of encoded antibodies (chromosomes)
        """
        # Step 1: Recognition of Antigen - Filter LOs based on learner profile
        recognition = RecognitionOfAntigen(self.learner_profile, self.concept_lo_mapping)
        filtered_mapping = recognition.filter_los()

        # Step 2: Antibody Encoding - Convert filtered LOs into chromosomes
        antibody_population = AntibodyPopulation(filtered_mapping, self.population_size)
        
        # Step 3: Generate Population - 100 Antibodies
        self.population = antibody_population.generate_population()

        return self.population
