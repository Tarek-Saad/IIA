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
                RETURN lo, ID(lo) AS lo_id
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

# Example usage
lo_service = GetLOService()

concept_name = "Data Structures"
los = lo_service.get_los_related_to_concept(concept_name)

print("Learning Objects related to the concept:", los)
