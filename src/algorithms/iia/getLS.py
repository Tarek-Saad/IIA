from src.algorithms.iia.Pop_index_LO_match import GetLOMatching
from src.core.services.ExtractFromLOs import ExtractFromLOs
from src.core.services.GetlearnersServices import LearnerServices

class getLS:
    def __init__(self):
        pass

    def LOsLS(self ,learning_goals , knowledge_base ):
        GetLOMatchingOBJ = GetLOMatching()
        result = GetLOMatchingOBJ.getLOMatch(learning_goals, knowledge_base)

        ExtractFromLOsOBJ = ExtractFromLOs()
        all_paths_learning_styles =ExtractFromLOsOBJ.extract_learning_styles_for_paths(result['selected_los'])


        return all_paths_learning_styles

    def LearnerLS(self , email):
        LearnerServicesOBJ = LearnerServices()
        learner_learning_styles = LearnerServicesOBJ.get_learner_learning_styles(email)
        return learner_learning_styles

if __name__ == "__main__":
    LS_service = getLS()

    learning_goals = ["Searching"]
    knowledge_base = ["Introduction to Programming"]
    result = LS_service.LOsLS(learning_goals, knowledge_base)

    print(result[0][0]['LS1'])  # Print the result to see the generated bit sequence
    print(result)  # Print the result to see the generated bit sequence

    email_to_search = 'kareem@example.com'
    learning_styles = LS_service.LearnerLS(email_to_search)

    print(learning_styles)

