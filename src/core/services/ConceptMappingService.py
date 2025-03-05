class ConceptMappingService:
    def __init__(self):
        self.concept_lo_mapping = {}

    def set_concept_lo_mapping(self, concept_lo_mapping):
        """Set the concept to Learning Objects mapping"""
        self.concept_lo_mapping = concept_lo_mapping

    def get_concept_lo_mapping(self):
        """Get the current concept to Learning Objects mapping"""
        return self.concept_lo_mapping
