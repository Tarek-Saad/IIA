import random
from src.core.services.GetLOsService import GetLOService

class ConceptOrderService:
    def __init__(self):
        self.graph_service = GetLOService()  # استخدام GetLOService للحصول على LOs

    def get_random_lo_for_each_concept(self, concept_names):
        """Function to select one random Learning Object for each Concept from the provided list"""
        concept_lo_mapping = {}  # Dictionary to store concept and the selected LO

        # Iterate over each concept in the provided list of concept names
        for concept_name in concept_names:
            # Get all related LOs for the concept using the get_los_related_to_concept function
            los = self.graph_service.get_los_related_to_concept(concept_name)

            if los:  # If LOs are found for the concept
                # Randomly select one LO for the concept
                random_lo = random.choice(los)  # Select one LO randomly
                concept_lo_mapping[concept_name] = random_lo  # Add to mapping

        return concept_lo_mapping

# # إنشاء كائن من ConceptOrderService
# concept_service = ConceptOrderService()
#
# # تمرير قائمة من المفاهيم لاختيار LOs لها
# concept_names = ["Data Structures", "Graph Theory", "Algorithms", "Searching"]
#
# # استدعاء الدالة للحصول على LO عشوائي لكل مفهوم
# concept_lo_mapping = concept_service.get_random_lo_for_each_concept(concept_names)
#
# # طباعة النتيجة
# print("Concept to LO mapping:", concept_lo_mapping)