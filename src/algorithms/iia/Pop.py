import random


class RandomBitSequenceGenerator:
    def __init__(self):
        pass

    def generate_random_bit_sequence_for_concepts(self, num_concepts):
        """
        Generates a bit sequence for each concept. Each concept is represented by 30 bits.
        In each 30-bit segment, only one bit is set to 1 randomly, and the rest are 0.
        Returns a list of lists where each inner list is a 30-bit sequence.
        """
        bit_sequences = []  # To hold all the 30-bit sequences

        for _ in range(num_concepts):
            # Generate a 30-bit segment where only one bit is set to 1
            segment = [0] * 30
            random_index = random.randint(0, 29)  # Randomly choose a bit to set as 1
            segment[random_index] = 1
            bit_sequences.append(segment)  # Append the 30-bit segment as a separate list

        return bit_sequences

    def generate_multiple_random_bit_sequences(self, num_concepts, num_sequences):
        """
        Generates multiple random bit sequences for a given number of concepts.
        Each sequence consists of num_concepts 30-bit segments.
        """
        sequences = []
        for _ in range(num_sequences):
            # Generate a random bit sequence for the given number of concepts
            random_bit_sequence = self.generate_random_bit_sequence_for_concepts(num_concepts)
            sequences.append(random_bit_sequence)
        return sequences


# if __name__ == "__main__":
#     population_service = RandomBitSequenceGenerator()
#
#     # Corrected way to call the method
#     result = population_service.generate_multiple_random_bit_sequences(4,2)
#
#     print(result)  # Print the result to see the generated bit sequence
