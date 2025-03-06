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

    def generate_random_bit_sequence_for_concepts(self, num_concepts):
        """
        Generates a bit sequence for each concept. Each concept is represented by 30 bits.
        In each 30-bit segment, only one bit is set to 1 randomly, and the rest are 0.
        """
        bit_sequence = []
        for _ in range(num_concepts):
            # Generate a 30-bit segment where only one bit is set to 1
            segment = [0] * 30
            random_index = random.randint(0, 29)  # Randomly choose a bit to set as 1
            segment[random_index] = 1
            bit_sequence.extend(segment)  # Add this segment to the bit sequence
        return bit_sequence


if __name__ == "__main__":
    population_service = Population()

    # Test with 4 concepts and generate initial population
    random_bit_sequence = population_service.generate_random_bit_sequence_for_concepts(4)
    print("Generated Random Bit Sequence for 4 Concepts:", random_bit_sequence)

