from src.core.services.GetLOsService import GetLOService


class Encoding:
    def __init__(self):
        pass

    def encode_los_to_chromosome(self, concept_lo_mapping):
        """
        Convert the selected Learning Objects to a chromosome encoding
        where each concept gets a 30-bit encoding.
        One of the 30 bits is 1 (the selected LO), and others are 0.
        """
        chromosome = []

        # Iterate over each concept in the mapping
        for concept_name, lo in concept_lo_mapping.items():
            # Initialize a 30-bit chromosome for each concept
            concept_chromosome = [0] * 30  # Initialize 30 bits for this concept

            # Get the lo_id for the selected LO
            lo_id = lo.get('lo_id', None)  # Assuming 'lo_id' is used to identify each LO

            if lo_id is not None:
                # Get all the related LOs for this concept
                GetLOServicee = GetLOService()
                related_los = GetLOServicee.get_los_related_to_concept(concept_name)


                # Find the LO that matches the lo_id
                for index, lo in enumerate(related_los):
                    if lo['lo_id'] == lo_id:
                        # Set the corresponding index to 1
                        concept_chromosome[index] = 1
                        break  # We only need to set one bit to 1 for the selected LO

            # Add the concept's chromosome (30 bits) to the overall chromosome
            chromosome.extend(concept_chromosome)

        return chromosome
