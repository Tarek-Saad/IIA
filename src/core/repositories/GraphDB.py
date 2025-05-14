# GraphDB.py
from neo4j import GraphDatabase
from src.config.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

class GraphDB:
    _instance = None
    _driver = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GraphDB, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Lazy initialization - only create the driver when needed
        pass

    def get_driver(self):
        # Initialize the driver only if it hasn't been initialized yet
        if GraphDB._driver is None:
            GraphDB._driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
            print("Connection pool created successfully")
        return GraphDB._driver

    def get_session(self):
        return self.get_driver().session()

    def close(self):
        """Close the database connection"""
        if GraphDB._driver is not None:
            GraphDB._driver.close()
            GraphDB._driver = None

    def test_connection(self):
        """Test the database connection"""
        try:
            with self.get_session() as session:
                result = session.run("RETURN 1 AS test")
                if result.single():
                    print("Connection is working!")
                    return True
                else:
                    print("Connection failed!")
                    return False
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False

# Only test the connection if this file is run directly
if __name__ == "__main__":
    graph_db = GraphDB()
    graph_db.test_connection()
