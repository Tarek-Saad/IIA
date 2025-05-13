class GetLOService:
    def __init__(self):
        # Delayed import
        from src.core.repositories.GraphDB import GraphDB
        self.graph_db = GraphDB()

    def get_los_related_to_concept(self, concept_name):
        """Function to get all Learning Objects related to a given Concept name"""
        los = []  # List to hold the LOs related to the concept

        with self.graph_db.get_session() as session:
            result = session.run(f"""
                MATCH (c:Concept)-[:HAS_LO]->(lo:LO)
                WHERE c.name = '{concept_name}'
                RETURN lo, elementId(lo) AS lo_id
            """)

            # Iterate through the result and extract relevant information from each LO node
            for record in result:
                lo_node = record["lo"]  # The node representing the Learning Object

                # Extracting properties from the LO node to return them as an array
                lo_data = {
                    "name": lo_node["name"],
                    "difficulty": lo_node["difficulty"],
                    "learning_style_visual_verbal": lo_node["learning_style_visual_verbal"],
                    "learning_style_sequential_global": lo_node["learning_style_sequential_global"],
                    "formatt": lo_node["formatt"],
                    "learning_style_sensitive_intuitive": lo_node["learning_style_sensitive_intuitive"],
                    "sourcee": lo_node["sourcee"],
                    "learning_style_active_reflective": lo_node["learning_style_active_reflective"],
                    "lo_id": record["lo_id"]  # Adding the lo_id from the query result
                }

                los.append(lo_data)  # Add the learning object data to the list

        return los

    def get_los_related_to_concepts(self, concepts):
        """Get all Learning Objects related to the given list of concepts"""
        concept_lo_mapping = {}

        with self.graph_db.get_session() as session:
            for concept_name in concepts:
                # Generate the Cypher query dynamically for each concept
                query = f"""
                    MATCH (c:Concept)-[:WITH_LO]->(lo:LearningObject)
                    WHERE c.name = '{concept_name}'
                    RETURN c.name AS concept_name, lo, elementId(lo) AS lo_id
                """

                result = session.run(query)

                lo_list = []
                for record in result:
                    lo = record["lo"]
                    lo_list.append(lo)

                concept_lo_mapping[concept_name] = lo_list

        return concept_lo_mapping


# Example usage
lo_service = GetLOService()

# concept_name = "Data Structures"
# los = lo_service.get_los_related_to_concept(concept_name)
#
# print("Learning Objects related to the concept:", los[0])

# traversal_result = ["Data Structures", "Linked Lists", "Trees"]
# los = lo_service.get_los_related_to_concepts(traversal_result)
#
# print(los)
