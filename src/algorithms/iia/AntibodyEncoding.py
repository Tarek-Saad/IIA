import random

class AntibodyEncoding:
    def __init__(self, filtered_concept_lo_mapping):
        """
        Initialize Antibody Encoding
        :param filtered_concept_lo_mapping: Dictionary mapping each concept to a filtered list of possible LOs
        """
        self.filtered_concept_lo_mapping = filtered_concept_lo_mapping

    def encode_chromosome(self):
        """
        Generate a single antibody (learning path).
        - Each concept is assigned exactly one LO.
        - A chromosome frame is built using binary encoding.
        :return: Binary encoded chromosome representing selected LOs.
        """
        chromosome = {}

        for concept, lo_list in self.filtered_concept_lo_mapping.items():
            if not lo_list:
                continue  # Skip if no LOs are available

            selected_lo = random.choice(lo_list)  # Randomly select one LO for the concept
            chromosome[concept] = {
                "lo_id": selected_lo["lo_id"],
                "encoding": [1 if lo == selected_lo else 0 for lo in lo_list]  # Binary encoding
            }

        return chromosome
