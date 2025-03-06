import random
from src.core.services.GetLOsService import GetLOService
from src.core.services.ConceptOrderService import GraphService
from src.algorithms.iia.Pop import RandomBitSequenceGenerator


class GetLOMatching:
    def __init__(self):
        pass

    def getLOMatch(self, learning_goals, knowledge_base):
        """
        Generates the matching Learning Objects (LOs) based on the learning goals and knowledge base.
        Randomly selects LOs for each concept from the list.
        """
        # Step 1: Generate concept sequence using the GraphService
        GraphServiceOBJ = GraphService()
        traversal_result = GraphServiceOBJ.proposed_traversal_algorithm(learning_goals, knowledge_base)

        # Step 2: Get the LOs associated with each concept, one by one
        GetLOServiceOBJ = GetLOService()
        concept_lo_mapping = {}

        for concept in traversal_result:
            # Get the LOs related to the current concept (passing each concept one by one)
            lo_list = GetLOServiceOBJ.get_los_related_to_concept(concept)

            concept_lo_mapping[concept] = lo_list

        # Step 3: Generate multiple random bit sequences for each concept
        conceptsNum = len(traversal_result)
        pathes = 2

        RandomBitSequenceGeneratorOBJ = RandomBitSequenceGenerator()
        random_bit_sequences = RandomBitSequenceGeneratorOBJ.generate_multiple_random_bit_sequences(
            conceptsNum, pathes)

        # Step 4: Loop through each path (bit sequence)
        selected_los = []
        chromosomes = []

        # Loop through each path of random bit sequences (each path corresponds to a different set of selections)
        for path_idx, path in enumerate(random_bit_sequences):
            # print(f"Path {path_idx + 1}: {path}")

            # Create a list for the current path to hold the selected LOs
            path_selected_los = []
            path_chromosome = []

            # Loop through the concepts and their associated LOs for the current path
            for idx, concept in enumerate(traversal_result):
                bit_sequence = path[idx]  # Get the random bit sequence for the current concept
                lo_list = concept_lo_mapping.get(concept, [])

                for lo_idx, bit in enumerate(bit_sequence):
                    if bit == 1 and lo_idx < len(lo_list):
                        path_selected_los.append(lo_list[lo_idx])
                        path_chromosome.append(1)
                    else:
                        path_chromosome.append(0)

            # Append the selected LOs and chromosome for this path to the final result
            selected_los.append(path_selected_los)
            chromosomes.append(path_chromosome)

        return {"selected_los": selected_los, "chromosomes": chromosomes , "concepts_num":conceptsNum , "pathes_num" : pathes}
