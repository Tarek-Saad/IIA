# GraphService.py

class GraphService:
    def __init__(self):
        # Delayed import
        from src.core.repositories.GraphDB import GraphDB
        self.graph_db = GraphDB()

    def get_relevant_concepts(self, learning_goals, knowledge_base):
        relevant_concepts = set(learning_goals)
        concepts_to_check = list(learning_goals)

        with self.graph_db.get_session() as session:
            while concepts_to_check:
                current_concept = concepts_to_check.pop()

                # Find all prerequisites (including indirect ones)
                result = session.run(f"""
                MATCH (c:Concept {{name: '{current_concept}'}})<-[:PREREQUISITE]-(p)
                RETURN p.name AS prerequisite
                """)

                for record in result:
                    prereq_concept = record["prerequisite"]
                    # Add the prerequisite if it's not already in the relevant concepts or knowledge base
                    if prereq_concept not in relevant_concepts and prereq_concept not in knowledge_base:
                        relevant_concepts.add(prereq_concept)
                        concepts_to_check.append(prereq_concept)


        return relevant_concepts

    def proposed_traversal_algorithm(self, learning_goals, knowledge_base):

        relevant_concepts = set(learning_goals)  # Set of relevant concepts including learning goals
        all_concepts = []  # List to hold the final sequence of concepts
        stack = []  # Stack for DFS traversal
        visited = set()  # Set to track visited concepts to avoid reprocessing

        # Push initial concepts (learning goals) onto the stack
        for goal in learning_goals:
            stack.append(goal)

        with self.graph_db.get_session() as session:
            while stack:
                cur_concept = stack[-1]  # Look at the top of the stack (last element)

                if cur_concept not in visited:
                    # Find the prerequisites (children) of the current concept
                    result = session.run(f"""
                    MATCH (c:Concept {{name: '{cur_concept}'}})<-[:PREREQUISITE]-(p)
                    RETURN p.name AS prerequisite
                    """)

                    # Mark the current concept as visited if it has no unvisited children
                    children_visited = True
                    for record in result:
                        prereq_concept = record["prerequisite"]
                        if prereq_concept not in visited and prereq_concept not in knowledge_base:
                            children_visited = False
                            if prereq_concept not in relevant_concepts:
                                relevant_concepts.add(prereq_concept)
                            stack.append(prereq_concept)

                    # If all prerequisites (children) have been visited, process the current concept
                    if children_visited:
                        visited.add(cur_concept)
                        all_concepts.append(cur_concept)
                        stack.pop()  # Remove the current concept from the stack

                else:
                    # If the current concept is already visited, pop it from the stack
                    stack.pop()

        return all_concepts
