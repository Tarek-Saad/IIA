# from src.algorithms.iia.Pop_index_LO_match import GetLOMatching

class ExtractFromLOs:
    def __init__(self):
        pass

    def extract_learning_styles(self, lo_data):
        learning_styles = {
            'LS1': lo_data.get('learning_style_active_reflective', None),
            'LS2': lo_data.get('learning_style_visual_verbal', None),
            'LS3': lo_data.get('learning_style_sensitive_intuitive', None),
            'LS4': lo_data.get('learning_style_sequential_global', None)
        }
        return learning_styles


    def extract_learning_styles_for_paths(self, selected_los):
        all_paths_learning_styles = []

        # Loop through each path in selected_los
        for path_idx, path in enumerate(selected_los):
            # print(f"Processing Path {path_idx + 1}:")

            path_learning_styles = []

            # Loop through each concept (LO) in the current path
            for concept_idx, lo in enumerate(path):
                # Extract learning styles for the current LO
                learning_styles = self.extract_learning_styles(lo)
                path_learning_styles.append(learning_styles)
                # print(f"Path {path_idx + 1} - Concept {concept_idx + 1} LS: {learning_styles}")

            # Add the learning styles for the current path to the final result
            all_paths_learning_styles.append(path_learning_styles)

        return all_paths_learning_styles





# if __name__ == "__main__":
#     GetLOMatching = GetLOMatching()
#     learning_goals = ["Trees"]
#     knowledge_base = ["Introduction to Programming"]
#     result = GetLOMatching.getLOMatch(learning_goals, knowledge_base)
#
#     # Create an instance of ExtractOneLO
#     extract_one_lo = ExtractFromLOs()
#
#     # Extract learning styles for all paths
#     learning_styles = extract_one_lo.extract_learning_styles_for_paths(result['selected_los'])
#
#     print("Learning Styles for all paths: ", learning_styles)
