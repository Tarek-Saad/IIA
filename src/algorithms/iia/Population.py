import random
from src.algorithms.iia.Encoding import Encoding

class Population:
    def __init__(self):
        self.encoding_service = Encoding()

    def generate_initial_population(self, concept_lo_mapping, population_size=100, total_los_count=40):
        """
        Generates an initial population of antibodies (encoded chromosomes).
        Each antibody is a possible solution represented as a chromosome of 0's and 1's.
        """
        population = []  # List to hold the population of antibodies (chromosomes)

        # Generate 'population_size' antibodies (chromosomes)
        for _ in range(population_size):
            # Randomly select one LO for each concept and encode it into a chromosome
            chromosome = self.encoding_service.encode_los_to_chromosome(concept_lo_mapping, total_los_count)
            population.append(chromosome)

        return population



# if __name__ == "__main__":
#     population_service = Population()
