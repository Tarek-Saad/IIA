from src.core.repositories.GraphDB import GraphDB

class LOChildFetcher:
    def __init__(self):
        self.driver = GraphDB().get_driver()

    def get_ordered_sub_los_by_internal_id(self, internal_id: int):
        """
        Given a Neo4j internal LO id, fetch ordered subLOs through the THEN chain.
        Includes full debug logging.
        """
        query = """
        MATCH (lo:LO)-[:HAS]->(start:subLO)
        WHERE id(lo) = $id

        MATCH path = (start)-[:THEN*0..]->(end)
        WITH path
        ORDER BY length(path) DESC
        LIMIT 1

        WITH nodes(path) AS orderedSubLOs
        UNWIND orderedSubLOs AS subLO
        WITH COLLECT({name: subLO.name, material: subLO.material, reference: subLO.reference}) AS subLODetails
        
        RETURN subLODetails AS orderedSubLOs
        """

        try:
            with self.driver.session() as session:
                result = session.run(query, id=internal_id)
                record = result.single()

                print(f"[DEBUG] Record raw: {record}")

                if record:
                    sub_los = record.get("orderedSubLOs")
                    print(f"[DEBUG] Retrieved {len(sub_los)} subLOs" if sub_los else "[DEBUG] subLOs is empty or None")
                    return sub_los if sub_los else []
                else:
                    print(f"⚠️ No record returned for LO id {internal_id}.")
                    return []

        except Exception as e:
            print(f"❌ [Neo4j ERROR] While querying subLOs for LO id {internal_id}: {str(e)}")
            return []

if __name__ == "__main__":
    fetcher = LOChildFetcher()

    test_lo_id = 89435  # Confirmed working ID in Neo4j
    sub_los = fetcher.get_ordered_sub_los_by_internal_id(test_lo_id)

    print(f"\n📚 Ordered subLOs for LO id({test_lo_id}):")
    if sub_los:
        for i, sub in enumerate(sub_los):
            print(f"  {i + 1}. 📘 {sub.get('name', 'Unnamed')}")
    else:
        print("  ⚠️ No subLOs returned.")
