import random

class Encoding:
    def __init__(self):
        pass


    def encode_los_to_chromosome(self, concept_lo_mapping, total_los_count=40):
        """
        Convert the selected Learning Objects to a chromosome encoding
        where each concept gets a 10-bit encoding.
        One of the 10 bits is 1 (randomly selected LO), and others are 0.
        """
        # Divide the total chromosome into 10-bit segments for each concept
        chromosome = []

        # Iterate over each concept in the mapping
        for concept_name, lo in concept_lo_mapping.items():
            concept_chromosome = [0] * 10  # Initialize 10 bits for this concept

            # Randomly choose one index in this concept's 10 bits to set to 1
            random_index = random.randint(0, 9)  # Choose a random index between 0 and 9
            concept_chromosome[random_index] = 1  # Set that index to 1

            # Add the concept's chromosome (10 bits) to the overall chromosome
            chromosome.extend(concept_chromosome)

        return chromosome