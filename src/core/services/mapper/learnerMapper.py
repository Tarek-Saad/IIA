from datetime import datetime
import json

class LearnerMapper:
    def __init__(self, learner_data):
        # Initialize all the fields based on the learner data tuple
        self.id = learner_data[0]
        self.name = learner_data[1]
        self.email = learner_data[2]
        self.password_hash = learner_data[3]
        self.date_of_birth = learner_data[4]
        self.registration = learner_data[5]
        self.knowledge_level = learner_data[6]
        self.learning_goals = learner_data[7]  # This should be a list, so no need for JSON parsing
        self.knowledge_base = learner_data[8]  # This should be a list, so no need for JSON parsing
        self.learning_style_active_reflective = learner_data[9]
        self.learning_style_visual_verbal = learner_data[10]
        self.learning_style_sensing_intuitive = learner_data[11]
        self.learning_style_sequential_global = learner_data[12]
        self.preferred_learning_pace = learner_data[13]
        self.engagement_score = learner_data[14]
        self.feedback_history = learner_data[15]
        self.last_active = learner_data[16]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "date_of_birth": self.date_of_birth,
            "registration": self.registration,
            "knowledge_level": self.knowledge_level,
            "learning_goals": self.learning_goals,
            "knowledge_base": self.knowledge_base,
            "LS1": self.learning_style_active_reflective,
            "LS2": self.learning_style_visual_verbal,
            "LS3": self.learning_style_sensing_intuitive,
            "LS4": self.learning_style_sequential_global,
            "preferred_learning_pace": self.preferred_learning_pace,
            "engagement_score": self.engagement_score,
            "feedback_history": self.feedback_history,
            "last_active": self.last_active
        }


def map_learners(learners_data):
    learner_objects = []

    # Ensure it's a list of learners if one learner is returned
    if learners_data:
        if isinstance(learners_data, tuple):
            learners_data = [learners_data]

        for learner in learners_data:
            learner_mapper = LearnerMapper(learner)
            learner_objects.append(learner_mapper.to_dict())
    return learner_objects



# Test the mapping
# if __name__ == "__main__":
#     LearnerServicesOBJ = LearnerServices()
#
#     email_to_search = 'tarek@example.com'
#     learner_data = LearnerServicesOBJ.get_learner_by_email(email_to_search)
#
#     mapped_learners = map_learners(learner_data)
#
#     # Print the mapped learners
#     for learner in mapped_learners:
#         print(learner['LS1'])
