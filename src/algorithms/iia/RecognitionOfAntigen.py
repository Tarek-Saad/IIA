class RecognitionOfAntigen:
    def __init__(self, learner_profile, concept_lo_mapping):
        """
        Initialize Recognition of Antigen
        :param learner_profile: Dictionary containing learning goals, prior knowledge, and learning style
        :param concept_lo_mapping: Dictionary mapping each concept to a list of possible LOs
        """
        self.learner_profile = learner_profile
        self.concept_lo_mapping = concept_lo_mapping

    def filter_los(self):
        """
        Filters candidate LOs based on antigen recognition.
        - Removes LOs that do not align with learning goals.
        - Prioritizes LOs that match the learner's learning style.
        - Ensures prerequisite concepts are satisfied.
        :return: Filtered concept-to-LO mapping.
        """
        filtered_mapping = {}

        for concept, lo_list in self.concept_lo_mapping.items():
            # 1. Ensure concept is part of learner's learning goals or prerequisites
            if concept not in self.learner_profile["learning_goals"] and concept not in self.learner_profile["prior_knowledge"]:
                continue  # Skip concepts not relevant to learner

            # 2. Filter LOs based on learning style
            matching_los = []
            for lo in lo_list:
                lo_style = lo.get("learning_style", {})  # LO's learning style
                learner_style = self.learner_profile["learning_style"]

                # Compute similarity score based on learning style dimensions
                style_match = sum(learner_style.get(dim, 0) * lo_style.get(dim, 0) for dim in learner_style)

                # Only keep LOs with some match to the learner's preferred learning style
                if style_match > 0:
                    matching_los.append(lo)

            # 3. If no LOs match, keep original list to avoid empty sets
            filtered_mapping[concept] = matching_los if matching_los else lo_list

        return filtered_mapping
